#!/bin/bash

export OMPI_ALLOW_RUN_AS_ROOT=1
export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

if [ -z "${VERSION}" ]; then
    echo "VERSION environment variable is not set. Please set it to the desired Ansys version."
    exit 1
fi

RUN_DPF_SERVER=${RUN_DPF_SERVER:-false}

if [ "${ANSYS_DPF_ACCEPT_LA}" = "Y" ]; then
    RUN_DPF_SERVER=true
fi


echo "RUN_DPF_SERVER: $RUN_DPF_SERVER"

if [ "$RUN_DPF_SERVER" = "true" ]; then
    echo "Starting DPF server..."
    export DPF_DEFAULT_GRPC_MODE="insecure"
    if "/ansys_inc/v${VERSION}/aisol/bin/linx64/Ans.Dpf.Grpc.sh" --port "${DPF_PORT_INTERNAL}" --address '0.0.0.0' > log_dpf.log 2>&1 &
    then
        sleep 2  # Give DPF server time to start
        echo "DPF server started."
    else
        echo "Failed to start DPF server"
        exit 1
    fi
fi

if [[ $MAPDL_IMAGE == *"cicd"* ]]; then
    echo "Using OpenMPI for CICD version"
    export MPI="-mpi openmpi"
else
    echo "Using default MPI version"
    export MPI=""
fi

echo "Starting MAPDL..."
echo "Using executable path: ${EXEC_PATH}"

CMD=$(cat <<-_EOT_
${EXEC_PATH} -grpc -dir /jobs -${DISTRIBUTED_MODE} ${MPI} -transport insecure -allowremote true -np 2 -db -6000 -m -6000
_EOT_
)

echo "Running command:"
echo "${CMD}"
exec ${CMD}
