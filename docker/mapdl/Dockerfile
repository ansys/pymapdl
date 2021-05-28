FROM centos:7

LABEL description="Trimmed MAPDL RC2 v212"
MAINTAINER Alex Kaszynski "alexander.kaszynski@ansys.com"

RUN yum install \
    openssl \
    openssh-clients \
    mesa-libGL \
    mesa-libGLU \
    motif \
    libgfortran \
    -y && \
    yum clean all && \
    rm -rf /var/cache/yum

RUN mkdir -p /ansys_inc
COPY v212 /ansys_inc/v212

EXPOSE 50052
ENTRYPOINT ["/ansys_inc/v212/ansys/bin/mapdl", "-grpc"]
