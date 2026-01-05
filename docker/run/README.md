# Docker Run Configurations

This directory contains Docker Compose files for running MAPDL, DPF, and license server containers.

## Contents

- **`docker-compose.yml`**: Main Docker Compose configuration for running MAPDL and DPF services

## Usage

### Running MAPDL with External License Server

```bash
# Set required environment variables
export ANSYSLMD_LICENSE_FILE=1055@mylicenseserver
export DOCKER_IMAGE=myregistry.com/myimage:mytag
export DPF_DOCKER_IMAGE=myregistry.com/mydpfimage:mydpftag  # optional

# Start MAPDL service
docker compose up -d mapdl

# Start MAPDL with DPF
docker compose up -d mapdl dpf

# Or use profiles
docker compose --profile mapdl-dpf up -d
```

## Available Services

### docker-compose.yml

- **`mapdl`**: MAPDL instance with gRPC server (ports 50052, 50055)
- **`dpf`**: DPF (Data Processing Framework) server (port 50056)
- **`mapdl-local`**: Development container with PyMAPDL workspace mounted

## Available Profiles

- `mapdl` - Run MAPDL only
- `mapdl-dpf` - Run MAPDL with DPF
- `local` - Run MAPDL in local development mode
- `local-dpf` - Run MAPDL in local development mode with DPF
- `dpf` - Run DPF only

## Environment Variables

- `ANSYSLMD_LICENSE_FILE`: License server location (e.g., `1055@mylicenseserver`)
- `DOCKER_IMAGE`: MAPDL Docker image path
- `DPF_DOCKER_IMAGE`: DPF Docker image path (optional)
- `AWP_ROOT`: Environment variable name for MAPDL installation (default: `AWP_ROOT251`)
- `AWP_ROOT_VALUE`: Path to MAPDL installation inside container (default: `/ansys_inc`)
- `DOCKER_USER`: Username inside the container (default: `mapdl`)

## Requirements

- Docker and Docker Compose installed
- MAPDL Docker image
- Valid Ansys license or access to a license server
- (Optional) DPF Docker image for data processing capabilities
