
#################################
FROM ubuntu:22.04 as BUILDER
#################################
# Builder stage.
# Used to download and install the MAPDL
# To be built using:
#
# $ TAG=builder
# $ docker build -t $TAG --build-arg VERSION=251 --target BUILDER .

#################################
# ARGUMENTS
# ---------
# In case you want to build a specific version
ARG VERSION

#################################
# Download MAPDL
# --------------
# This stage is highly dependent on your environment.
# Do you have the MAPDL installer in a directory?
# Then...
COPY /path/to/MAPDL/installer_files /MAPDL

# Or do you have a MAPDL installer in a remote server?
# Then...
RUN wget http://your.server.com/path/to/MAPDL_${VERSION} -O /MAPDL

#################################
# Install MAPDL dependencies
# --------------------------
#
RUN apt-get update && \
    apt-get install -y \
      curl  \
      libgl1 \
      libglu1 \
      libgomp1 \
      libxcb-icccm4 \
      libxcb-image0 \
      libxcb-keysyms1 \
      libxcb-randr0 \
      libxcb-render-util0 \
      libxcb-render0 \
      libxcb-shape0 \
      libxcb-shm0 \
      libxcb-sync1 \
      libxcb-util1 \
      libxcb-xfixes0 \
      libxcb-xinerama0 \
      libxcb-xkb1 \
      libxi6 \
      libxkbcommon-x11-0 \
      libxkbcommon0 \
      libxm4 \
      openssh-client \
    && apt install -y software-properties-common \
    && add-apt-repository -y ppa:zeehio/libxp \
    && apt-get update \
    && apt-get install -y libxp6 \
    && rm -rf .dockerignore \
      && rm -rf Dockerfile \
      && rm -rf *.log \
      apt-get clean && rm -rf /var/lib/apt/lists/*

#################################
# Installing MAPDL
# ----------------
#
RUN mkdir -p /ansys_inc && \
      chmod +x ./MAPDL/linx64/INSTALL && \
      sh ./MAPDL/linx64/INSTALL \
        -install_dir /ansys_inc \
        -nochecks -mechapdl -ansyscust -silent && \
      rm -rf /MAPDL


#################################
FROM ubuntu:22.04 as FINAL
#################################
# This is the final stage with the MAPDL installed, and the runtime
# dependencies. It also include some convenience features like:
#
# - Adding a user
# - Adding a working directory
# - Adding an alias to the ansys executable
# - Adding a license server (optional)
# - Adding locale (optional)
#
# To be built using:
#
# $ TAG='mapdl:latest'
# $ docker build -t $TAG --build-arg VERSION=251 --target FINAL .

#################################
# Arguments
# ---------
#
ARG VERSION

# Optional arguments
ARG USERNAME=mapdl
ARG USER_UID=1000
ARG USER_GID=$USER_UID

#################################
# Environment variables
# ---------------------
# Storing version in a env var
ENV ANSYS_VERSION=$VERSION

# Location env var
ENV AWP_ROOT${VERSION}=/ansys_inc/v${VERSION}

# Setting home directory
ENV HOME=/home/$USERNAME

# Setting working directory
ENV WORKING_DIRECTORY=jobs

# License server
# (Optional)
# ENV LICENSE_SERVER=111.222.333.444
# ENV ANSYSLMD_LICENSE_FILE=1055@$LICENSE_SERVER

# OpenMPI env vars
# Uncomment if you want to use OpenMPI with root user
# ENV OMPI_ALLOW_RUN_AS_ROOT=1
# ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

# Setting other env vars
## For MAPDL awareness
ENV ON_DOCKER=TRUE
ENV DEBIAN_FRONTEND=noninteractive

#################################
# Labels
# ------
#
# LABELS
LABEL description="MAPDL on Ubuntu"
LABEL email="pyansys.core@ansys.com"

# OCI LABELS
LABEL org.opencontainers.image.documentation="https://mapdl.docs.pyansys.com"

#################################
# Installing dependencies
# -----------------------
# Update packages before packing and
# installing dependencies
RUN apt-get update && \
    apt-get install -y \
        libgomp1 \
        libgl1 \
        libglu1 \
        libxm4 \
        libxi6 \
        openssh-client \

# libxp.so missing. This is a workaround
#https://bugs.launchpad.net/ubuntu/+source/libxp/+bug/1517884
RUN apt install -y software-properties-common \
    && add-apt-repository -y ppa:zeehio/libxp \
    && apt-get update \
    && apt-get install -y libxp6

#################################
# Installing locale
# -----------------
# Adding locales to avoid locale warnings.
# Depending on your environment, you might not need it
# or need to change the locale to your preferred one.
RUN apt-get install -y locales && \
    locale-gen 'en_US.UTF-8' && \
    update-locale LC_ALL='en_US.UTF-8' && \
    sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen && \
    echo -e '\nexport LANG=en_US.UTF-8\nexport LANGUAGE=en_US:en\nexport LC_ALL=en_US.UTF-8' >> ~/.bashrc

#################################
# Cleaning
# --------
# Removing unnecessary files and apt cache
RUN rm -rf .dockerignore \
    && rm -rf Dockerfile \
    && rm -rf *.log \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \

#################################
# User configuration
# ------------------
# Add username, create the working directory and make it accessible to any user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    mkdir -p /home/$USERNAME/$WORKING_DIRECTORY \
    && \
    chown -R $USERNAME:$USERNAME /home/$USERNAME/$WORKING_DIRECTORY \
    && \
    chmod a+rwx /home/$USERNAME/$WORKING_DIRECTORY

USER $USERNAME
WORKDIR /home/$USERNAME/$WORKING_DIRECTORY

#################################
# Adding MAPDL alias
# ------------------
# (Optional) Adding alias to ansys executable (for convenience)
# This allows you to run MAPDL using the command "ansys" or "ansysgrpc"
# instead of the full path.
RUN echo 'alias ansys="/ansys_inc/v$ANSYS_VERSION/ansys/bin/mapdl"' >> ~/.bashrc && \
    printf '#!/bin/bash\n/ansys_inc/v$ANSYS_VERSION/ansys/bin/mapdl "$@"' > /usr/bin/ansys && \
    chmod +x /usr/bin/ansys && \
    printf '#!/bin/bash\n/ansys_inc/v$ANSYS_VERSION/ansys/bin/mapdl -grpc "$@"' > /usr/bin/ansysgrpc && \
    chmod +x /usr/bin/ansysgrpc

#################################
# Setting entrypoint and ports
# ----------------------------
#
EXPOSE 50052
ENTRYPOINT [ "bash", "-c", "/ansys_inc/v${ANSYS_VERSION}/ansys/bin/mapdl -grpc -dir ${WORKING_DIRECTORY}"]
