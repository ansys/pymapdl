#! /bin/bash

echo "==============================================="
echo "Running tests in PyMAPDL Testing environment..."
echo "==============================================="
echo ""

# Mark all directories as safe for git to handle mounted volumes owned by a
# different host user (common when running the container as root).
git config --global --add safe.directory '*' 2>/dev/null || true

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

    # overwrite the branch name with the one from the local repository if it exists
    if [ -d ".git" ]; then
        LOCAL_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
        if [ -n "${LOCAL_BRANCH}" ]; then
            echo "Overriding PYMAPDL_BRANCH with local repository branch: ${LOCAL_BRANCH}"
            export PYMAPDL_BRANCH="${LOCAL_BRANCH}"
        fi
    fi
else
    echo "Using cloned PyMAPDL repository for testing."
    if [ -d "${VENV_PATH}" ]; then
        echo "Existing virtual environment found at ${VENV_PATH}. Activating it."
    else
        echo "No existing virtual environment found at ${VENV_PATH}. Creating a new one."
        uv venv "${VENV_PATH}"
    fi
    # shellcheck disable=SC1091
    source "${VENV_PATH}/bin/activate"
fi

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
if [ -z "${CURRENT_BRANCH}" ]; then
  echo "WARNING: Could not determine current branch (git worktree or non-git directory). Skipping branch checkout."
else
  echo "Current branch: ${CURRENT_BRANCH}"
fi

# Checkout to the specified branch if PYMAPDL_BRANCH is set
if [ -n "${PYMAPDL_BRANCH}" ]; then
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

export PYTEST_ARGUMENTS=" --ignore_image_cache --image_cache_dir=/tmp/empty_dir ${PYTEST_ARGUMENTS}"

echo "Using pytest arguments: ${PYTEST_ARGUMENTS}"

# Add timing information for debugging startup delays
echo "Starting pytest at: $(date +%H:%M:%S)"

# Install the package in editable mode. Test dependencies are pre-installed in
# the image layer so uv only needs to install/update the delta (typically just
# the editable link for the project itself, making this near-instant).
uv pip install --python "${VENV_PATH}" -e ".[tests]"

# shellcheck disable=SC2086
time xvfb-run -a "${VENV_PATH}/bin/pytest" tests \
  --basetemp=/tmp/pytest-tmp \
  -vv \
  ${PYTEST_ARGUMENTS}

PYTEST_EXIT=$?
echo "Pytest finished at: $(date +%H:%M:%S)"
exit $PYTEST_EXIT
