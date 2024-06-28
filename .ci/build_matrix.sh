# List of versions
versions=(
    'v22.2.1'
    'v22.2-ubuntu'
    'v23.1.0'
    'v23.1-ubuntu'
    'v23.2.0'
    'v23.2-ubuntu'
    'v24.1.0'
    'v24.1-ubuntu'
    'v24.1-ubuntu-student'
    'v24.2.0'
    'latest-ubuntu'
    'latest-ubuntu-student'
)

JSON="{\"include\":["

# Loop through each version
for version in "${versions[@]}"; do
    echo "Processing version: $version"
    # echo "::add-matrix name=app::%changed_path%"
    # Place your command here
    # For example, you can pull Docker images
    # docker pull myimage:$version



    # Add build to the matrix only if it is not already included
    JSONline="{\"mapdl-version\": \"$version\", \"extended_testing\": \"false\"},"
    if [[ "$JSON" != *"$JSONline"* ]]; then
        JSON="$JSON$JSONline"
    fi


    # Set output
    echo "matrix=$( echo "$JSON" )" >> $GITHUB_OUTPUT
    
done

# Remove last "," and add closing brackets
if [[ $JSON == *, ]]; then
    JSON="${JSON%?}"
fi
JSON="$JSON]}"
echo $JSON

# Set output
echo "matrix=$( echo "$JSON" )" >> $GITHUB_OUTPUT