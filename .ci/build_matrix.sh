#!/bin/bash

# **** REMEMBER *****
# Remember to update the env var ``LATEST_VERSION`` in ci.yml
#

# List of versions
versions=(
    # if added more "latest", change "$LATEST"
    'v25.2-ubuntu-cicd'
    'v25.2.0'
    'v25.1-ubuntu-cicd'
    'v25.1.0'
    'v24.2-ubuntu-cicd'
    'v24.2.0'
)

# Run only ubuntu jobs
ONLY_UBUNTU="${ONLY_UBUNTU:-false}"

# On remote
ON_REMOTE="${ON_REMOTE:-false}"

## Start
JSON="{\"include\":["
counter=0

# Loop through each version
for version in "${versions[@]}"; do

    # 1 based counter
    ((counter++))

    # checking version config
    if [[ "$version" == *"ubuntu"* ]]; then
        ON_UBUNTU=true;
    else
        ON_UBUNTU=false;
    fi

    # Printing
    echo "Processing $counter"
    echo "  - Version: $version"
    echo "  - Ubuntu: $ON_UBUNTU"

    # Skipping if on Ubuntu only
    if [[ "$ON_UBUNTU" != "true" && "$ONLY_UBUNTU" == "true" ]]; then
        echo "Skipping non-ubuntu versions"
        echo ""
        continue
    fi

    # Generating json
    JSONline="{\"mapdl-version\": \"$version\"},"
    echo "ADDED line: $JSONline"

    # checks that the line is not repeated before adding it.
    if [[ "$JSON" != *"$JSONline"* ]]; then
        JSON="$JSON$JSONline"
    fi
    echo ""

done

# Remove last "," and add closing brackets
if [[ $JSON == *, ]]; then
    JSON="${JSON%?}"
fi
JSON="$JSON]}"
echo "$JSON"

# Set output
# shellcheck disable=SC2086
echo "matrix=${JSON}" >> $GITHUB_OUTPUT
