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
    
    extended_testing="${{ github.event_name == 'schedule' || ( github.event_name == 'workflow_dispatch' && inputs.run_all_tests ) || ( github.event_name == 'push' && contains(github.ref, 'refs/tags') ) }}"

    auth_user=${{ steps.is_organization_member.outputs.result == 'false' }}

    echo "Processing"
    echo "  - Version: $version"
    echo "  - extended_testing: $extended_testing"
    echo "  - auth_user: $auth_user"

    # Add build to the matrix only if it is not already included
    JSONline="{\"mapdl-version\": \"$version\", \"extended_testing\": \"$extended_testing\",  \"auth_user\": \"$auth_user\"},"

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