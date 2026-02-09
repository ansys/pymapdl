const core = require('@actions/core');
const exec = require('@actions/exec');
const path = require('path');

async function run() {
  try {
    // Get inputs
    const mapdlVersion = core.getInput('mapdl-version', { required: true });
    const licenseServer = core.getInput('license-server', { required: true });
    const mapdlImage = core.getInput('mapdl-image') || 'ghcr.io/ansys/mapdl';
    const instanceName = core.getInput('instance-name') || 'MAPDL_0';
    const pymapdlPort = core.getInput('pymapdl-port') || '50052';
    const pymapdlDbPort = core.getInput('pymapdl-db-port') || '50055';
    const dpfPort = core.getInput('dpf-port') || '50056';
    const enableDpfServer = core.getInput('enable-dpf-server') || 'false';
    const distributedMode = core.getInput('distributed-mode') || 'smp';
    const numProcessors = core.getInput('num-processors') || '2';
    const mpiType = core.getInput('mpi-type') || 'openmpi';
    const workingDirectory = core.getInput('working-directory') || '/jobs';
    const memoryMb = core.getInput('memory-mb') || '6656';
    const memorySwapMb = core.getInput('memory-swap-mb') || '16896';
    const memoryDbMb = core.getInput('memory-db-mb') || '6000';
    const memoryWorkspaceMb = core.getInput('memory-workspace-mb') || '6000';
    const transport = core.getInput('transport') || 'insecure';
    const studentVersion = core.getInput('student-version') || 'auto';
    const timeout = parseInt(core.getInput('timeout') || '60');
    const wait = core.getInput('wait') || 'true';

    // Save instance name for cleanup - maintain array of instances
    let instanceNames = [];
    const existingNames = core.getState('instance-names');
    if (existingNames) {
      try {
        instanceNames = JSON.parse(existingNames);
      } catch (error) {
        instanceNames = [];
      }
    }
    instanceNames.push(instanceName);
    core.saveState('instance-names', JSON.stringify(instanceNames));

    core.startGroup('Launch MAPDL Docker Container');
    console.log('Configuration:');
    console.log(`  MAPDL Version: ${mapdlVersion}`);
    console.log(`  MAPDL Image: ${mapdlImage}`);
    console.log(`  Instance Name: ${instanceName}`);
    console.log(`  PyMAPDL Port: ${pymapdlPort}`);
    console.log(`  DPF Port: ${dpfPort}`);
    console.log(`  Distributed Mode: ${distributedMode}`);
    console.log(`  Number of Processors: ${numProcessors}`);
    core.endGroup();

    // Set environment variables for the bash script
    process.env.MAPDL_VERSION = mapdlVersion;
    process.env.MAPDL_IMAGE = mapdlImage;
    process.env.INSTANCE_NAME = instanceName;
    process.env.LICENSE_SERVER = licenseServer;
    process.env.PYMAPDL_PORT = pymapdlPort;
    process.env.PYMAPDL_DB_PORT = pymapdlDbPort;
    process.env.DPF_PORT = dpfPort;
    process.env.ENABLE_DPF_SERVER = enableDpfServer;
    process.env.DISTRIBUTED_MODE = distributedMode;
    process.env.NUM_PROCESSORS = numProcessors;
    process.env.MPI_TYPE = mpiType;
    process.env.WORKING_DIRECTORY = workingDirectory;
    process.env.MEMORY_MB = memoryMb;
    process.env.MEMORY_SWAP_MB = memorySwapMb;
    process.env.MEMORY_DB_MB = memoryDbMb;
    process.env.MEMORY_WORKSPACE_MB = memoryWorkspaceMb;
    process.env.TRANSPORT = transport;
    process.env.STUDENT_VERSION = studentVersion;
    process.env.TIMEOUT = timeout.toString();

    // Run the launch script
    const scriptPath = path.join(__dirname, 'start-mapdl.sh');
    await exec.exec('bash', [scriptPath]);

    // Get container ID
    let containerId = '';
    await exec.exec('docker', ['ps', '-aqf', `name=${instanceName}`], {
      listeners: {
        stdout: (data) => {
          containerId = data.toString().trim();
        }
      }
    });

    // Extract version number
    const major = mapdlVersion.substring(1, 3);
    const minor = mapdlVersion.substring(4, 5);
    const version = `${major}${minor}`;

    // Set outputs
    core.setOutput('container-id', containerId);
    core.setOutput('container-name', instanceName);
    core.setOutput('pymapdl-port', pymapdlPort);
    core.setOutput('dpf-port', dpfPort);
    core.setOutput('pymapdl-db-port', pymapdlDbPort);
    core.setOutput('mapdl-version-number', version);
    core.setOutput('log-file', `${instanceName}.log`);

    core.startGroup('Container Information');
    console.log(`Container ID: ${containerId}`);
    console.log(`Container Name: ${instanceName}`);
    console.log(`MAPDL Version Number: ${version}`);
    core.endGroup();

    // Wait for services if requested
    if (wait === 'true') {
      core.startGroup('Waiting for MAPDL services to be ready');
      const waitScriptPath = path.join(__dirname, 'wait-services.sh');
      await exec.exec('bash', [waitScriptPath]);
      core.endGroup();
      console.log('✅ MAPDL instance is ready!');
    } else {
      console.log('⏭️  Skipping service readiness check (wait=false)');
      console.log('ℹ️  User is responsible for checking service availability');
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
