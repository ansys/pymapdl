const core = require('@actions/core');
const exec = require('@actions/exec');
const path = require('path');

async function run() {
  try {
    // Get inputs
    const mapdlVersion = core.getInput('mapdl-version');
    const mapdlImage = core.getInput('mapdl-image');
    const licenseServer = core.getInput('license-server', { required: true });
    const instanceName = core.getInput('instance-name') || 'MAPDL_0';
    const isDebug = process.env.RUNNER_DEBUG === '1' || core.isDebug();
    const DEBUG = core.getInput('debug') === 'true' || isDebug;

    // Validate inputs
    if (!mapdlVersion && !mapdlImage) {
      throw new Error('Either mapdl-version or mapdl-image must be provided');
    }

    // Check if using official Ansys registry
    const isOfficialRegistry = mapdlImage &&
      (mapdlImage.startsWith('ghcr.io/ansys/mapdl') || mapdlImage.startsWith('ansys/mapdl'));

    // If custom image (not official registry), mapdl-version must be provided
    if (mapdlImage && !isOfficialRegistry && !mapdlVersion) {
      throw new Error('mapdl-version must be provided when using a custom image (not from ghcr.io/ansys/mapdl or ansys/mapdl)');
    }

    // Determine the full image reference and version number
    let fullImageRef;
    let versionNumber;

    if (mapdlImage && isOfficialRegistry) {
      // Extract version number from official registry image tag (e.g., v25.1.0 -> 25.1)
      const tagMatch = mapdlImage.match(/v?(\d+)\.(\d+)(?:\.\d+)?/);

      if (tagMatch) {
        versionNumber = `${tagMatch[1]}.${tagMatch[2]}`;
        // Validate version format (XX.Y)
        if (!/^\d{2}\.\d$/.test(versionNumber) && !/^\d{2,}\.\d{1,}$/.test(versionNumber)) {
          throw new Error(`Invalid version format extracted from image: ${versionNumber}. Expected format: XX.Y`);
        }
        // Map to standard image reference
        fullImageRef = `ghcr.io/ansys/mapdl:v${versionNumber}-ubuntu-cicd`;
      } else {
        throw new Error('Could not extract version from official Ansys MAPDL image tag');
      }
    } else if (mapdlImage && !isOfficialRegistry) {
      // Custom image with mapdl-version provided
      fullImageRef = mapdlImage;
      // Validate version format (XX.Y)
      if (!/^\d{2}\.\d$/.test(mapdlVersion) && !/^\d{2,}\.\d{1,}$/.test(mapdlVersion)) {
        throw new Error(`Invalid mapdl-version format: ${mapdlVersion}. Expected format: XX.Y`);
      }
      versionNumber = mapdlVersion;
    } else {
      // User provided version number (e.g., 25.2)
      // Validate version format (XX.Y)
      if (!/^\d{2}\.\d$/.test(mapdlVersion) && !/^\d{2,}\.\d{1,}$/.test(mapdlVersion)) {
        throw new Error(`Invalid mapdl-version format: ${mapdlVersion}. Expected format: XX.Y`);
      }
      // Default to ubuntu-cicd variant
      fullImageRef = `ghcr.io/ansys/mapdl:v${mapdlVersion}-ubuntu-cicd`;
      versionNumber = mapdlVersion;
    }

    // Ensure versionNumber is set
    if (!versionNumber) {
      throw new Error('Failed to determine MAPDL version number');
    }

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
    core.saveState('debug', JSON.stringify(DEBUG));

    core.debug('Configuration:');
    core.debug(`  MAPDL Version: ${versionNumber}`);
    core.debug(`  MAPDL Image: ${fullImageRef}`);
    core.debug(`  Instance Name: ${instanceName}`);
    core.debug(`  PyMAPDL Port: ${pymapdlPort}`);
    core.debug(`  Transport: ${transport}`);
    core.debug(`  --`);
    core.debug(`  Enable DPF Server: ${enableDpfServer}`);
    core.debug(`  DPF Port: ${dpfPort}`);
    core.debug(`  --`);
    core.debug(`  Distributed Mode: ${distributedMode}`);
    core.debug(`  Number of Processors: ${numProcessors}`);
    core.debug(`  MPI Type: ${mpiType}`);
    core.debug(`  Working Directory: ${workingDirectory}`);
    core.debug(`  Memory (MB): ${memoryMb}`);
    core.debug(`  Memory DB (MB): ${memoryDbMb}`);
    core.debug(`  Memory Workspace (MB): ${memoryWorkspaceMb}`);

    // Set environment variables for the bash script
    process.env.MAPDL_VERSION = versionNumber;
    process.env.MAPDL_IMAGE = fullImageRef;
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
    process.env.TIMEOUT = timeout.toString();
    process.env.DEBUG = DEBUG ? 'true' : 'false';

    // Run the launch script (from parent directory when compiled to dist/)
    core.startGroup('Launch MAPDL Docker Container');
    const scriptPath = path.join(__dirname, '..', 'start-mapdl.sh');
    await exec.exec('bash', [scriptPath]);

    // Get container ID
    let psOutput = '';
    await exec.exec('docker', ['ps', '-aqf', `name=^/${instanceName}$`], {
      listeners: {
        stdout: (data) => {
          psOutput += data.toString();
        }
      }
    });
    const containerId = psOutput
      .split('\n')
      .map(line => line.trim())
      .find(line => line.length > 0) || '';

    core.endGroup();

    // Set outputs
    core.setOutput('container-id', containerId);
    core.setOutput('container-name', instanceName);
    core.setOutput('pymapdl-port', pymapdlPort);
    core.setOutput('dpf-port', dpfPort);
    core.setOutput('pymapdl-db-port', pymapdlDbPort);
    versionNumber = versionNumber.replace('.', '');
    core.setOutput('mapdl-version-number', versionNumber);
    core.setOutput('log-file', `${instanceName}.log`);

    core.startGroup('Container Information');
    console.log(`Container ID: ${containerId}`);
    console.log(`Container Name: ${instanceName}`);
    console.log(`MAPDL Version Number: ${versionNumber}`);
    core.endGroup();

    // Wait for services if requested
    if (wait === 'true') {
      core.startGroup('Waiting for MAPDL services to be ready');
      const waitScriptPath = path.join(__dirname, '..', 'wait-services.sh');
      await exec.exec('bash', [waitScriptPath], {silent: !DEBUG});
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
