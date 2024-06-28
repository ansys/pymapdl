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



LATEST=2 # for 'latest-ubuntu' and 'latest-ubuntu-student'

# Do not process more than the $CUTOUT versions in above list
UTH_USER_LIMIT_VERSIONS=3
AUTH_USER_LIMIT=$(($LATEST+$UTH_USER_LIMIT_VERSIONS*3)) 

# Students licenses only last a year, hence $LIMIT_VERSIONS cannot be more than 2.
NON_AUTH_USER_LIMIT_VERSIONS=2 # Must be 2
NON_AUTH_USER_LIMIT=$(($LATEST+$NON_AUTH_USER_LIMIT_VERSIONS*3))

LIMIT_VERSIONS="${LIMIT_VERSIONS:-0}"
HARD_LIMIT_VERSION=$(($LATEST+$LIMIT_VERSIONS*3))

## Started
JSON="{\"include\":["

counter=0
# Loop through each version
for version in "${versions[@]}"; do
    
    # 1 based counter
    ((counter++))

    # Checking hardlimit
    if [[ $LIMIT_VERSIONS -ne 0 && $counter -gt $HARD_LIMIT_VERSION ]]; then
        echo "Reached limit."
        break
    fi

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
            # Last 6 entries in the list above.
            if [[ $counter -le $AUTH_USER_LIMIT ]]; then
                add_line="true";
            else
                add_line="false";
            fi
        fi
    else
        if [[ $ON_STUDENT == "true" &&  $counter -le $NON_AUTH_USER_LIMIT ]]; then
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