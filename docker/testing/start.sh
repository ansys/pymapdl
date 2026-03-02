#! /bin/bash

echo "==============================================="
echo "Running tests in PyMAPDL Testing environment..."
echo "==============================================="
echo ""

# Mark all directories as safe for git to handle mounted volumes owned by a
# different host user (common when running the container as root).
git config --global --add safe.directory '*'

# Prevent writing .pyc files to the mounted volume.
export PYTHONDONTWRITEBYTECODE=1

# Redirect uv cache to a container-local path so it never writes to the
# mounted volume (overrides any default ~/.cache/uv or in-tree location).
export UV_CACHE_DIR="/tmp/uv-cache"

# Use container-local venv to avoid Docker volume mount performance issues
VENV_PATH="/tmp/.venv_container"

if [[ "${USE_LOCAL_REPO}" == "true" ]]; then
    echo "Using local PyMAPDL repository for testing."
    # Uncomment if you expect changes in the dependencies.
    # python3 -m pip install '.[tests]'
    if [ -d "${VENV_PATH}" ]; then
        echo "Existing virtual environment found at ${VENV_PATH}. Activating it."
    else
        echo "No existing virtual environment found at ${VENV_PATH}. Creating a new one."
        uv venv "${VENV_PATH}"
    fi
    # shellcheck disable=SC1091
    source "${VENV_PATH}/bin/activate"

else
    echo "Using cloned PyMAPDL repository for testing."
    uv venv "${VENV_PATH}"
    # shellcheck disable=SC1091
    source "${VENV_PATH}/bin/activate"
fi

# Checkout to the specified branch if PYMAPDL_BRANCH is set
if [ -n "${PYMAPDL_BRANCH}" ]; then
  CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
  if [ "${CURRENT_BRANCH}" != "${PYMAPDL_BRANCH}" ]; then
    echo "PYMAPDL_BRANCH is set to '${PYMAPDL_BRANCH}'. Current branch: '${CURRENT_BRANCH}'. Checking out..."
    # Use shallow fetch to reduce git overhead
    git fetch --depth 1 origin "${PYMAPDL_BRANCH}"
    git checkout "${PYMAPDL_BRANCH}"
  else
    echo "Already on branch '${PYMAPDL_BRANCH}'. Skipping checkout."
  fi
fi


if [ ! -d "tests" ]; then
  echo "Error: 'tests' directory does not exist."
  exit 1
fi

echo "Using pytest arguments: ${PYTEST_ARGUMENTS}"

# Add timing information for debugging startup delays
echo "Starting pytest at: $(date +%H:%M:%S)"

# Install the package with its test extras into the container-local venv.
# This is done separately from `uv run` to avoid `--no-project` suppressing
# the `--extra` flag (they are mutually exclusive in uv).
# The uv.lock file is intentionally not updated (--frozen) to avoid writing
# to the mounted volume.
uv pip install --python "${VENV_PATH}" -e ".[tests]"

# Removed --no-cache flag to enable package caching for better performance
# Disable problematic plugins that cause I/O overhead:
# -p no:cacheprovider  = disable pytest cache (saves ~10-20s on mounted volumes)
# --basetemp           = redirect all pytest tmp_path/tmpdir writes to /tmp
# shellcheck disable=SC2086
time xvfb-run -a "${VENV_PATH}/bin/pytest" tests \
  -p no:cacheprovider \
  --basetemp=/tmp/pytest-tmp \
  -vv \
  ${PYTEST_ARGUMENTS}

echo "Pytest finished at: $(date +%H:%M:%S)"
