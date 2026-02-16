const core = require('@actions/core');
const exec = require('@actions/exec');

async function cleanup() {
  try {
    // Get instance names - stored as JSON array in state
    const instanceNamesJson = core.getState('instance-names');

    if (!instanceNamesJson) {
      console.log('No instance names found in state, skipping cleanup');
      return;
    }

    let instanceNames = [];
    try {
      instanceNames = JSON.parse(instanceNamesJson);
    } catch (error) {
      console.log('Failed to parse instance names from state');
      return;
    }

    if (!Array.isArray(instanceNames) || instanceNames.length === 0) {
      console.log('No instances to cleanup');
      return;
    }

    core.startGroup('Cleanup MAPDL containers');
    console.log(`Cleaning up ${instanceNames.length} container(s)`);

    for (const instanceName of instanceNames) {
      console.log(`\nProcessing container: ${instanceName}`);

      // Stop the container
      try {
        await exec.exec('docker', ['stop', instanceName], {
          ignoreReturnCode: true
        });
        console.log(`✅ Container ${instanceName} stopped`);
      } catch (error) {
        console.log(`ℹ️  Container ${instanceName} was not running or already stopped`);
      }

      // Remove the container
      try {
        await exec.exec('docker', ['rm', instanceName], {
          ignoreReturnCode: true
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
