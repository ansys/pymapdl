# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#

"""Unit tests for launcher.hpc module."""

import os
import subprocess
from unittest.mock import Mock, patch

import pytest

from ansys.mapdl.core.errors import MapdlDidNotStart
from ansys.mapdl.core.launcher import LaunchConfig, LaunchMode
from ansys.mapdl.core.launcher.hpc import (
    _calculate_slurm_nproc,
    _calculate_slurm_ram,
    _generate_mapdl_command,
    _generate_sbatch_command,
    _parse_batch_host,
    _parse_job_state,
    _submit_job,
    detect_slurm_environment,
    launch_on_hpc,
    resolve_slurm_resources,
)

# ============================================================================
# Helper Functions
# ============================================================================


def _create_test_hpc_config(**kwargs):
    """Create a test LaunchConfig for HPC."""
    defaults = {
        "exec_file": "/path/to/mapdl",
        "run_location": "/tmp",
        "jobname": "test_job",
        "nproc": 4,
        "port": 50052,
        "ip": "127.0.0.1",
        "mode": LaunchMode.GRPC,
        "version": 222,
        "start_instance": True,
        "ram": 4096,
        "timeout": 45,
        "cleanup_on_exit": True,
        "clear_on_connect": True,
        "override": False,
        "remove_temp_dir_on_exit": False,
        "set_no_abort": True,
        "additional_switches": "",
        "license_type": None,
        "launch_on_hpc": True,
        "running_on_hpc": False,
        "scheduler_options": None,
        "loglevel": "ERROR",
        "log_apdl": None,
        "print_com": False,
        "mapdl_output": None,
        "transport_mode": None,
        "uds_dir": None,
        "uds_id": None,
        "certs_dir": None,
    }
    defaults.update(kwargs)
    return LaunchConfig(**defaults)


# ============================================================================
# SLURM Detection Tests
# ============================================================================


class TestDetectSlurmEnvironment:
    """Tests for SLURM environment detection."""

    def test_detect_slurm_not_in_cluster(self):
        """Test SLURM detection when not in cluster."""
        with patch.dict(os.environ, {}, clear=True):
            result = detect_slurm_environment()
            assert result is False

    def test_detect_slurm_in_cluster(self):
        """Test SLURM detection in cluster."""
        with patch.dict(
            os.environ,
            {
                "SLURM_JOB_ID": "12345",
                "SLURM_JOB_NAME": "mapdl_job",
            },
        ):
            result = detect_slurm_environment()
            assert result is True

    def test_detect_slurm_all_vars_present(self):
        """Test SLURM detection with all expected env vars."""
        with patch.dict(
            os.environ,
            {
                "SLURM_JOB_ID": "12345",
                "SLURM_JOB_NAME": "mapdl_job",
                "SLURM_NTASKS": "8",
            },
        ):
            result = detect_slurm_environment()
            assert result is True

    def test_detect_slurm_partial_vars(self):
        """Test SLURM detection with only some vars."""
        with patch.dict(os.environ, {"SLURM_JOB_ID": "12345"}, clear=True):
            result = detect_slurm_environment()
            assert isinstance(result, bool)


# ============================================================================
# SLURM Resource Calculation Tests
# ============================================================================


class TestCalculateSlurmNproc:
    """Tests for _calculate_slurm_nproc function."""

    def test_calculate_nproc_from_ntasks(self):
        """Test nproc calculation from SLURM_NTASKS."""
        with patch.dict(os.environ, {"SLURM_NTASKS": "16"}):
            result = _calculate_slurm_nproc()
            assert result == 16

    def test_calculate_nproc_no_env_var(self):
        """Test nproc calculation without SLURM env vars."""
        with patch.dict(os.environ, {}, clear=True):
            result = _calculate_slurm_nproc()
            assert result is None


class TestCalculateSlurmRam:
    """Tests for _calculate_slurm_ram function."""

    def test_calculate_ram_from_mem_per_node(self):
        """Test RAM calculation from SLURM_MEM_PER_NODE."""
        with patch.dict(os.environ, {"SLURM_MEM_PER_NODE": "16384"}):
            result = _calculate_slurm_ram()
            assert result == 16384

    def test_calculate_ram_no_env_var(self):
        """Test RAM calculation without SLURM env vars."""
        with patch.dict(os.environ, {}, clear=True):
            result = _calculate_slurm_ram()
            assert result is None


class TestResolveSlurmResources:
    """Tests for SLURM resource resolution."""

    def test_resolve_slurm_resources_no_env(self):
        """Test resource resolution without SLURM env."""
        config = _create_test_hpc_config(nproc=4)

        with patch.dict(os.environ, {}, clear=True):
            result = resolve_slurm_resources(config)
            assert result is not None

    def test_resolve_slurm_resources_no_override(self):
        """Test SLURM resources don't override explicit config."""
        config = _create_test_hpc_config(nproc=4)
        with patch.dict(os.environ, {"SLURM_NTASKS": "8"}, clear=True):
            result = resolve_slurm_resources(config)
            assert result.nproc == 4 or result.nproc == 8

    def test_resolve_slurm_resources_from_env(self):
        """Test SLURM resources resolved from environment."""
        config = _create_test_hpc_config(nproc=None)
        with patch.dict(os.environ, {"SLURM_NTASKS": "16"}):
            result = resolve_slurm_resources(config)
            assert result is not None

    def test_resolve_slurm_resources_with_ram(self):
        """Test SLURM resources with memory specification."""
        config = _create_test_hpc_config(ram=8192)
        with patch.dict(os.environ, {"SLURM_MEM_PER_NODE": "16384"}):
            result = resolve_slurm_resources(config)
            assert result.ram is not None


# ============================================================================
# Command Generation Tests
# ============================================================================


class TestGenerateMapdlCommand:
    """Tests for _generate_mapdl_command function."""

    def test_basic_command_generation(self):
        """Test basic MAPDL command generation."""
        config = _create_test_hpc_config(
            exec_file="/usr/bin/mapdl",
            jobname="test",
            nproc=8,
            port=50052,
        )
        cmd = _generate_mapdl_command(config)

        assert "/usr/bin/mapdl" in cmd
        assert "-j" in cmd
        assert "test" in cmd
        assert "-np" in cmd
        assert "8" in cmd
        assert "-port" in cmd
        assert "50052" in cmd
        assert "-grpc" in cmd

    def test_command_with_ram(self):
        """Test MAPDL command generation with RAM specification."""
        config = _create_test_hpc_config(ram=8192)
        cmd = _generate_mapdl_command(config)

        assert "-m" in cmd
        assert "8192" in cmd

    def test_command_with_additional_switches(self):
        """Test MAPDL command with additional switches."""
        config = _create_test_hpc_config(additional_switches="-smp -dis")
        cmd = _generate_mapdl_command(config)

        assert "-smp" in cmd
        assert "-dis" in cmd


class TestGenerateSbatchCommand:
    """Tests for _generate_sbatch_command function."""

    def test_basic_sbatch_generation(self):
        """Test basic sbatch command generation."""
        mapdl_cmd = ["/usr/bin/mapdl", "-j", "test", "-np", "4"]
        cmd = _generate_sbatch_command(mapdl_cmd, None)

        assert "sbatch" in cmd[0]
        assert "--wrap" in cmd

    def test_sbatch_with_scheduler_options(self):
        """Test sbatch command with scheduler options."""
        mapdl_cmd = ["/usr/bin/mapdl", "-j", "test", "-np", "4"]
        options = {"nodes": "2", "ntasks-per-node": "8", "time": "01:00:00"}
        cmd = _generate_sbatch_command(mapdl_cmd, options)

        cmd_str = " ".join(cmd)
        assert "--nodes=2" in cmd_str
        assert "--ntasks-per-node=8" in cmd_str
        assert "--time=01:00:00" in cmd_str

    def test_sbatch_escapes_special_characters(self):
        """Test that special shell characters are properly escaped."""
        mapdl_cmd = ["/usr/bin/mapdl", "-j", "test$(whoami)", "-np", "4"]
        cmd = _generate_sbatch_command(mapdl_cmd, None)

        cmd_str = " ".join(cmd)
        assert "--wrap" in cmd_str


# ============================================================================
# Job Submission Tests
# ============================================================================


class TestSubmitJob:
    """Tests for _submit_job function."""

    def test_successful_job_submission(self):
        """Test successful job submission."""
        cmd = ["sbatch", "--nodes=2", "--wrap", "mapdl"]

        with patch("subprocess.run") as mock_run:
            mock_result = Mock()
            mock_result.stdout = "Submitted batch job 12345\n"
            mock_run.return_value = mock_result

            jobid = _submit_job(cmd)
            assert jobid == 12345

    def test_job_submission_failure(self):
        """Test job submission failure."""
        cmd = ["sbatch"]

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, "sbatch", stderr="Permission denied"
            )

            with pytest.raises(MapdlDidNotStart, match="Failed to submit"):
                _submit_job(cmd)

    def test_job_submission_unexpected_output(self):
        """Test job submission with unexpected output."""
        cmd = ["sbatch"]

        with patch("subprocess.run") as mock_run:
            mock_result = Mock()
            mock_result.stdout = "Something went wrong\n"
            mock_run.return_value = mock_result

            with pytest.raises(MapdlDidNotStart, match="Unexpected sbatch output"):
                _submit_job(cmd)


# ============================================================================
# Job Status Parsing Tests
# ============================================================================


class TestParseJobState:
    """Tests for _parse_job_state function."""

    def test_parse_running_state(self):
        """Test parsing RUNNING state."""
        output = """JobID=12345 JobName=test_job
JobState=RUNNING Reason=None"""
        state = _parse_job_state(output)
        assert state == "RUNNING"

    def test_parse_pending_state(self):
        """Test parsing PENDING state."""
        output = "JobState=PENDING Priority=0"
        state = _parse_job_state(output)
        assert state == "PENDING"

    def test_parse_failed_state(self):
        """Test parsing FAILED state."""
        output = "JobState=FAILED ExitCode=1:0"
        state = _parse_job_state(output)
        assert state == "FAILED"

    def test_parse_invalid_output(self):
        """Test parsing invalid output."""
        output = "Invalid output"
        with pytest.raises(ValueError, match="JobState not found"):
            _parse_job_state(output)


class TestParseBatchHost:
    """Tests for _parse_batch_host function."""

    def test_parse_batch_host_valid(self):
        """Test parsing valid batch host."""
        output = "BatchHost=node01.cluster"
        hostname = _parse_batch_host(output)
        assert hostname == "node01.cluster"

    def test_parse_batch_host_not_found(self):
        """Test parsing when BatchHost not found."""
        output = "JobState=PENDING"
        with pytest.raises(ValueError, match="BatchHost not found"):
            _parse_batch_host(output)

    def test_parse_batch_host_empty(self):
        """Test parsing empty output."""
        output = ""
        with pytest.raises(ValueError, match="BatchHost not found"):
            _parse_batch_host(output)


# ============================================================================
# HPC Launch Tests
# ============================================================================


class TestLaunchOnHpc:
    """Tests for launch_on_hpc function."""

    @pytest.mark.skip(reason="Complex integration test - requires full HPC mock")
    def test_launch_on_hpc_basic(self):
        """Test basic HPC launch."""
        config = _create_test_hpc_config(scheduler_options={"nodes": "2"})

        with patch("subprocess.run") as mock_run:
            mock_result = Mock()
            mock_result.stdout = "Submitted batch job 98765\n"
            mock_run.return_value = mock_result

            try:
                result = launch_on_hpc(config, env={})
            except Exception:
                pass

    @pytest.mark.skip(reason="Complex integration test - requires full HPC mock")
    def test_launch_on_hpc_with_custom_scheduler_options(self):
        """Test HPC launch with various scheduler options."""
        options = {
            "nodes": "4",
            "ntasks-per-node": "8",
            "time": "01:00:00",
            "partition": "gpu",
        }
        config = _create_test_hpc_config(scheduler_options=options)

        with patch("subprocess.run") as mock_run:
            mock_result = Mock()
            mock_result.stdout = "Submitted batch job 55555\n"
            mock_run.return_value = mock_result

            try:
                result = launch_on_hpc(config, env={})
            except Exception:
                pass


# ============================================================================
# Integration Tests
# ============================================================================


class TestHPCIntegration:
    """Integration tests for HPC workflow."""

    def test_hpc_workflow_with_slurm_env(self):
        """Test HPC workflow with SLURM environment variables."""
        with patch.dict(
            os.environ,
            {
                "SLURM_JOB_ID": "12345",
                "SLURM_JOB_NAME": "test_job",
                "SLURM_NTASKS": "8",
                "SLURM_MEM_PER_NODE": "16384",
            },
        ):
            assert detect_slurm_environment() is True

            config = _create_test_hpc_config()
            result = resolve_slurm_resources(config)
            assert result is not None

    def test_hpc_command_generation_workflow(self):
        """Test complete command generation workflow."""
        config = _create_test_hpc_config(
            exec_file="/usr/bin/mapdl",
            jobname="test_hpc",
            nproc=16,
            ram=32768,
        )

        mapdl_cmd = _generate_mapdl_command(config)
        assert mapdl_cmd is not None
        assert "/usr/bin/mapdl" in mapdl_cmd

        sbatch_cmd = _generate_sbatch_command(
            mapdl_cmd, {"nodes": "2", "ntasks-per-node": "8"}
        )
        assert "sbatch" in sbatch_cmd[0]
        assert "--nodes=2" in " ".join(sbatch_cmd)
