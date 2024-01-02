FROM ghcr.io/ansys/mapdl:v24.1-ubuntu-student

USER root

# General libraries
ENV DEBIAN_FRONTEND=noninteractive

# Installing libs for testing and docs
RUN apt-get -qq update && apt install -qq -y zip pandoc libgl1-mesa-glx xvfb texlive-latex-extra latexmk graphviz texlive-xetex && \
    apt-get -qq clean  && rm -rf /var/lib/apt/lists/*

# Setting up locales
RUN apt-get install -y --no-install-recommends locales && \
    locale-gen 'en_US.UTF-8' && \
    update-locale LC_ALL='en_US.UTF-8' && \
    sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen && \
    echo -e '\nexport LANG=en_US.UTF-8\nexport LANGUAGE=en_US:en\nexport LC_ALL=en_US.UTF-8' >> ~/.bashrc && \
    apt-get -qq clean  && rm -rf /var/lib/apt/lists/*

# Installing Python environment
RUN python3.10 -m venv ./.venv && \
    . ./.venv/bin/activate && \
    pip install pre-commit && \
    pip install ansys-mapdl-core && \
    pip install -r .devcontainer/codespaces-docs/requirements.txt && \
    echo -e '\nsource ./.venv/bin/activate' >> ~/.bashrc

USER mapdl
