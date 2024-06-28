# List of versions
versions=(
    'latest-ubuntu'
    'latest-ubuntu-student'
    'v24.2.0'
    'v24.1.0'
    'v24.1-ubuntu'
    'v24.1-ubuntu-student'
    'v23.2.0'
    'v23.2-ubuntu'
    'v23.1.0'
    'v23.1-ubuntu'
    'v22.2.1'
    'v22.2-ubuntu'
)

JSON="{\"include\":["

counter=0
# Loop through each version
for version in "${versions[@]}"; do
    
    # 1 based counter
    ((counter++))

    if [[ "${{ matrix.mapdl-version }}" == *"ubuntu"* ]]; then
        export ON_UBUNTU=true;
    else 
        export ON_UBUNTU=false;
    fi

    if [[ "${{ matrix.mapdl-version }}" == *"student"* ]]; then
        export ON_STUDENT=true;
    else 
        export ON_STUDENT=false;
    fi

    echo "Processing $counter"
    echo "  - Version: $version"
    echo "  - extended_testing: $extended_testing"
    echo "  - auth_user: $auth_user"
    echo "  - Student: $ON_STUDENT"
    echo "  - Ubuntu: $ON_UBUNTU"
    echo ""

    if [[ $auth_user == "true"]]; then
        if [[ $extended_testing == "true" ]]; then
            # runs everything 
            add_line="true"
        else
            # Runs only "latest" and last two versions.
            # Last 6 registries in list above.
            if [[ $counter -le 6 ]]; then
                add_line="true"
            else
                add_line="false"
            fi
        fi
    else
        if [[ $ON_STUDENT == "true" ]]; then
            add_line="true"
        else
            add_line="false"
    fi;

    if [["$add_line" == "true" ]]; then
        JSONline="{\"mapdl-version\": \"$version\"},"

        echo "ADDED line: $JSONline"

        # checks that the line is not repeated before adding it.
        if [[ "$JSON" != *"$JSONline"* ]]; then
            JSON="$JSON$JSONline"
        fi
    else
        echo "NOT added line"
    fi
    
done

# Remove last "," and add closing brackets
if [[ $JSON == *, ]]; then
    JSON="${JSON%?}"
fi
JSON="$JSON]}"
echo $JSON

# Set output
echo "matrix=$( echo "$JSON" )" >> $GITHUB_OUTPUT