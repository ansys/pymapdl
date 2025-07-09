
if [ -z "${VERSION}" ]; then
    echo "VERSION environment variable is not set. Please set it to the desired Ansys version."
    exit 1
fi


RUN_DPF_SERVER=false
if [ -z "${ANSYS_DPF_ACCEPT_LA}" ]; then
    if [ "${ANSYS_DPF_ACCEPT_LA}" == "Y" ]; then
        RUN_DPF_SERVER=true
    fi
fi

echo "RUN_DPF_SERVER: $RUN_DPF_SERVER"

if [ "$RUN_DPF_SERVER" = true ]; then
    echo "Setting DPF Debug directory..."
    export DATAPROCESSING_DEBUG=${HOME}/dpf_logs/
    mkdir -p "$DATAPROCESSING_DEBUG"

    echo "Starting DPF server..."
    /ansys_inc/v${VERSION}/aisol/bin/linx64/Ans.Dpf.Grpc.sh --port ${DPF_PORT_INTERNAL} > log_dpf.log &
    echo "DPF server started."
fi

echo "Starting MAPDL..."
${EXEC_PATH} -grpc -dir /jobs -${DISTRIBUTED_MODE} -np 2 -db -5000 -m -5000 -