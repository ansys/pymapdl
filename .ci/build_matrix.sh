# List of versions
versions=(
    'latest-ubuntu'
    'latest-ubuntu-student'
    'v24.2.0'
    'v24.2-ubuntu'
    'v24.2-ubuntu-student'
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

MINIMAL_VERSIONS=2
LATEST=2 # for 'latest-ubuntu' and 'latest-ubuntu-student'
CUTOUT=$(($LATEST+$MINIMAL_VERSIONS*3)) # do not process more than the $CUTOUT versions in above file

counter=0
# Loop through each version
for version in "${versions[@]}"; do
    
    # 1 based counter
    ((counter++))

    if [[ "$version" == *"ubuntu"* ]]; then
        ON_UBUNTU=true;
    else 
        ON_UBUNTU=false;
    fi

    if [[ "$version" == *"student"* ]]; then
        ON_STUDENT=true;
    else 
        ON_STUDENT=false;
    fi

    echo "Processing $counter"
    echo "  - Version: $version"
    echo "  - extended_testing: $extended_testing"
    echo "  - auth_user: $auth_user"
    echo "  - Student: $ON_STUDENT"
    echo "  - Ubuntu: $ON_UBUNTU"

    if [[ "$auth_user" == "true" ]]; then
        if [[ "$extended_testing" == "true" ]]; then
            # runs everything 
            add_line="true";
        else
            # Runs only "latest" and last two versions.
            # Last 6 registries in list above.
            if [[ $counter -le $CUTOUT ]]; then
                add_line="true";
            else
                add_line="false";
            fi
        fi
    else
        if [[ $ON_STUDENT == "true" &&  $counter -le $CUTOUT ]]; then
            add_line="true";
        else
            add_line="false";
        fi
    fi

    if [[ "$add_line" == "true" ]]; then
        JSONline="{\"mapdl-version\": \"$version\"},"

        echo "ADDED line: $JSONline"

        # checks that the line is not repeated before adding it.
        if [[ "$JSON" != *"$JSONline"* ]]; then
            JSON="$JSON$JSONline"
        fi
    else
        echo "NOT added line"
    fi
    echo ""
    
done

# Remove last "," and add closing brackets
if [[ $JSON == *, ]]; then
    JSON="${JSON%?}"
fi
JSON="$JSON]}"
echo $JSON

# Set output
echo "matrix=$( echo "$JSON" )" >> $GITHUB_OUTPUT