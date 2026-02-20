#! /bin/bash

echo "==============================================="
echo "Running tests in PyMAPDL Testing environment..."
echo "==============================================="
echo ""

# Checkout to the specified branch if PYMAPDL_BRANCH is set
if [ -n "${PYMAPDL_BRANCH}" ]; then
  echo "PYMAPDL_BRANCH is set to '${PYMAPDL_BRANCH}'. Checking out this branch..."
  git fetch origin "${PYMAPDL_BRANCH}" > /dev/null 2>&1
  git checkout "${PYMAPDL_BRANCH}"
fi

if [[ "${USE_LOCAL_REPO}" == "true" ]]; then
    echo "Using local PyMAPDL repository for testing."
    # Uncomment if you expect changes in the dependencies.
    # python3 -m pip install '.[tests]'

else
    echo "Using cloned PyMAPDL repository for testing."
fi

echo "Using pytest arguments: ${PYTEST_ARGUMENTS}"

# shellcheck disable=SC2086
xvfb-run pytest ${PYTEST_ARGUMENTS}
