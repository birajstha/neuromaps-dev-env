# ===========================
# Connectome Workbench v2.1.0 + neuromaps
# ===========================
FROM ubuntu:20.04

LABEL Author="Biraj Shrestha" \
      Version="v2.1.0" \
      Description="Docker container with Connectome Workbench v2.1.0 + neuromaps"

# ---------------------------
# Install dependencies
# ---------------------------
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    wget unzip python3 python3-pip python3-setuptools \
    python3-wheel git curl build-essential \
    libgl1-mesa-glx libglu1-mesa libxext6 libxrender1 libxtst6 \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------
# Install Connectome Workbench v2.1.0
# ---------------------------
RUN mkdir -p /opt && cd /opt && \
    wget -q https://www.humanconnectome.org/storage/app/media/workbench/workbench-linux64-v2.1.0.zip && \
    unzip workbench-linux64-v2.1.0.zip && \
    mv workbench workbench-v2.1.0 && \
    rm workbench-linux64-v2.1.0.zip

# ---------------------------
# Install neuromaps
# ---------------------------
RUN cd /opt && \
    git clone https://github.com/netneurolab/neuromaps.git && \
    cd neuromaps && python3 -m pip install .

# ---------------------------
# Create app directories
# ---------------------------
RUN mkdir -p /app/data /app/scripts

# ---------------------------
# Environment variables
# ---------------------------
ENV PATH="/opt/workbench-v2.1.0/bin_linux64:${PATH}" \
    PATH="/opt/neuromaps:${PATH}" \
    PYTHONPATH="/opt/neuromaps:${PYTHONPATH}"

# ---------------------------
# Default run command
# ---------------------------
CMD ["/bin/bash"]
