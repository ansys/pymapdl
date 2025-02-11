# Inputs
# - ANSYS_VERSION
# - OS

OS="${OS:-Linux}"
ANSYS_VERSION="${ANSYS_VERSION:-221}"
ANSYS_VERSION_WITH_POINT="${ANSYS_VERSION:0:2}.${ANSYS_VERSION:2}"
GITHUB_TOKEN="${GITHUB_TOKEN:?Error: MY_VAR is not set or empty}"

echo "OS: $OS"
echo "Ansys version: $ANSYS_VERSION"
echo "Ansys version (number): $ANSYS_VERSION_WITH_POINT"

if [[ "$OS" == "Linux" ]]; then
    BranchName="linux_release-$ANSYS_VERSION_WITH_POINT"
    DIRECTORY="$(pwd)"
    SERVER=$DIRECTORY/dpf-standalone
    DIR="/aisol/bin/linx64"
    executable="./Ans.Dpf.Grpc.sh"

else # Windows
    BranchName="win_release-$ANSYS_VERSION_WITH_POINT"
    DIRECTORY="$(pwd)"
    SERVER=$DIRECTORY/dpf-standalone
    DIR="\aisol\bin\winx64"
    executable="./Ans.Dpf.Grpc.bat"

fi

echo "SERVER: $SERVER"
echo "BranchName: $BranchName"

git clone --branch $BranchName --single-branch https://$GITHUB_TOKEN@github.com/ansys-dpf/dpf-standalone
echo "AWP_ROOT$ANSYS_VERSION=$SERVER" >> $GITHUB_OUTPUT

# Setting up the files
cd $SERVER
cd */*/*
echo "Current directory: $(pwd)"
echo "Files in the directory: $(ls)"

cd $DIR
echo "Current directory: $(pwd)"
echo "Files in the directory: $(ls)"

if [[ "$OS" == "Linux" ]]; then
    echo "Setting files permissions"
    chmod 755 Ans.Dpf.Grpc.sh
    chmod 755 Ans.Dpf.Grpc.exe
fi

echo "Starting server"
$executable --address 127.0.0.1 > logdpf.txt &

echo "Server started"
sleep 2
echo "File output: $(cat logdpf.txt)"
