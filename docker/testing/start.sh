#! /bin/bash

echo "==============================================="
echo "Running tests in PyMAPDL Testing environment..."
echo "==============================================="
echo ""

if [[ "${USE_LOCAL_REPO}" == "true" ]]; then
    echo "Using local PyMAPDL repository for testing."
    # Uncomment if you expect changes in the dependencies.
    # python3 -m pip install '.[tests]'
    if [ -d ".venv_container" ]; then
        echo "Existing virtual environment found at .venv_container. Activating it."
    else
        echo "No existing virtual environment found at .venv_container. Creating a new one."
        uv venv .venv_container
    fi
    source .venv_container/bin/activate

else
    echo "Using cloned PyMAPDL repository for testing."
    uv venv .venv
    source .venv/bin/activate
fi

# Checkout to the specified branch if PYMAPDL_BRANCH is set
if [ -n "${PYMAPDL_BRANCH}" ]; then
  echo "PYMAPDL_BRANCH is set to '${PYMAPDL_BRANCH}'. Checking out this branch..."
  git fetch origin "${PYMAPDL_BRANCH}" > /dev/null 2>&1
  git checkout "${PYMAPDL_BRANCH}"
fi


if [ ! -d "tests" ]; then
  echo "Error: 'tests' directory does not exist."
  exit 1
fi

echo "Using pytest arguments: ${PYTEST_ARGUMENTS}"

# shellcheck disable=SC2086
xvfb-run -a uv run --active --no-cache --extra tests pytest tests -k "test_big_component" ${PYTEST_ARGUMENTS}
