import * as core from '@actions/core';
import * as exec from '@actions/exec';
import fs from 'fs';
import path from 'path';

function showLogFile(instanceName, showTail) {
  const logFile = path.join(process.env.GITHUB_WORKSPACE || process.cwd(), `${instanceName}.log`);

  core.startGroup(`MAPDL Log: ${instanceName}`);
  try {
    if (fs.existsSync(logFile)) {
      console.log(fs.readFileSync(logFile, 'utf8'));
    } else {
      console.log(`Log file not found: ${logFile}`);
    }
  } catch (err) {
    console.log(`Could not read log file: ${err.message}`);
  }
  core.endGroup();

  if (showTail) {
    try {
      if (fs.existsSync(logFile)) {
        const lines = fs.readFileSync(logFile, 'utf8').split('\n');
        const tail = lines.slice(-50).join('\n');
        console.log(`\n⚠️ Last 50 lines of ${instanceName}.log:`);
        console.log(tail);
      }
    } catch (err) {
      console.log(`Could not read log file tail: ${err.message}`);
    }
  }
}

async function cleanup() {
  try {
    // Get instance names - stored as JSON array in state
    const instanceNamesJson = core.getState('instance-names');
    const debug = JSON.parse(core.getState('debug') || 'false');
    const mainCompleted = core.getState('main-completed') === 'true';

    if (!instanceNamesJson) {
      core.error('No instance names found in state, skipping cleanup');
      return;
    }

    let instanceNames = [];
    try {
      instanceNames = JSON.parse(instanceNamesJson);
    } catch (error) {
      core.error('Failed to parse instance names from state');
      return;
    }

    if (!Array.isArray(instanceNames) || instanceNames.length === 0) {
      core.error('No instances to cleanup');
      return;
    }

    // Show log files before cleanup
    for (const instanceName of instanceNames) {
      showLogFile(instanceName, !mainCompleted);
    }

    core.startGroup('Cleanup MAPDL containers');
    console.log(`Cleaning up ${instanceNames.length} container(s)`);

    for (const instanceName of instanceNames) {
      console.log(`\nProcessing container: ${instanceName}`);

      // Stop the container
      try {
        await exec.exec('docker', ['stop', instanceName], {
          ignoreReturnCode: true,
          silent: !debug // Only show output if debug is true
        });
        console.log(`✅ Container ${instanceName} stopped`);
      } catch (error) {
        console.log(`ℹ️  Container ${instanceName} was not running or already stopped`);
      }

      // Remove the container
      try {
        await exec.exec('docker', ['rm', instanceName], {
          ignoreReturnCode: true,
          silent: !debug // Only show output if debug is true
        });
        console.log(`✅ Container ${instanceName} removed`);
      } catch (error) {
        console.log(`ℹ️  Container ${instanceName} was already removed`);
      }
    }

    core.endGroup();

  } catch (error) {
    // Don't fail the workflow if cleanup fails
    console.error(`Cleanup warning: ${error.message}`);
  }
}

cleanup();
