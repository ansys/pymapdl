# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set environment variables
ARG VERSION
ARG USERNAME=mapdl
ARG USER_UID=1000
ARG LICENSE_SERVER

ENV USER_GID=$USER_UID
ENV ANSYS_VERSION=$VERSION
ENV LICENSE_SERVER=$LICENSE_SERVER
ENV AWP_ROOT241=/ansys_inc
ENV WORKING_DIRECTORY=/jobs
ENV HOME=/home/$USERNAME
ENV ON_DOCKER=TRUE
ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

# Update package list
RUN apt-get update

# Install necessary packages
RUN apt-get install -y \
    libbrotli1 \
    libbsd0 \
    libexpat1 \
    libfontconfig1 \
    libfreetype6 \
    libglib2.0-0 \
    libice6 \
    libmd0 \
    libpng16-16 \
    libsm6 \
    libx11-6 \
    libx11-xcb1 \
    libxau6 \
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
    libxcb1 \
    libxdmcp6 \
    libxext6 \
    libxkbcommon-x11-0 \
    libxkbcommon0 \
    software-properties-common\
    && add-apt-repository -y ppa:zeehio/libxp \
    && apt-get update \
    && apt-get install -y libxp6

# Create the necessary directory
RUN mkdir -p /ansys_inc && \
    echo "Directory created."

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Add a working directory and make it accessible to any user
RUN mkdir -p /home/$USERNAME/$WORKING_DIRECTORY \
    && chown -R $USERNAME:$USERNAME /home/$USERNAME/$WORKING_DIRECTORY \
    && chmod a+rwx /home/$USERNAME/$WORKING_DIRECTORY

# Copy distribution files to /tmp
COPY distributions/*.tgz /tmp/
RUN apt-get install -y tar \
    && cd /tmp \
    && for file in *.tgz; do tar -xzf "$file" -C /ansys_inc; done \
    && rm -rf /tmp/*

# install the product
RUN /ansys_inc/INSTALL -silent -install_dir /ansys_inc -licserverinfo $LICENSE_SERVER -mechapdl

# LABELS
LABEL description="MAPDL on Ubuntu"
LABEL email="pyansys.core@ansys.com"

# OCI LABELS
LABEL org.opencontainers.image.documentation="https://mapdl.docs.pyansys.com"

# Cleaning up unnecessary files
RUN rm -rf /tmp/

# Adding alias to ansys executable
RUN printf '#!/bin/bash\n/ansys_inc/v$ANSYS_VERSION/ansys/bin/mapdl "$@"' > /usr/bin/ansys && \
    chmod +x /usr/bin/ansys
RUN printf '#!/bin/bash\n/ansys_inc/v$ANSYS_VERSION/ansys/bin/mapdl -grpc "$@"' > /usr/bin/ansysgrpc && \
    chmod +x /usr/bin/ansysgrpc

# Setting user
USER $USERNAME
WORKDIR /home/$USERNAME/$WORKING_DIRECTORY

# Setting entrypoint
EXPOSE 50052
ENTRYPOINT [ "bash", "-c", "/ansys_inc/v${ANSYS_VERSION}/ansys/bin/mapdl -grpc -dir ${WORKING_DIRECTORY}"]
