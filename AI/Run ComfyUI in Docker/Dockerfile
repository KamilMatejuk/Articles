ARG UBUNTU_VERSION=22.04
ARG CUDA_VERSION=12.4.1
ARG BASE_CUDA_DEV_CONTAINER=nvidia/cuda:${CUDA_VERSION}-devel-ubuntu${UBUNTU_VERSION}
ARG BASE_CUDA_RUN_CONTAINER=nvidia/cuda:${CUDA_VERSION}-runtime-ubuntu${UBUNTU_VERSION}
FROM ${BASE_CUDA_DEV_CONTAINER} AS build

ARG UID=1000
ARG GID=1000

RUN apt-get update \
    && apt-get install -y git python3 python3-pip python3-wheel \
    && apt autoremove -y \
    && apt clean -y \
    && rm -rf /tmp/* /var/tmp/* \
    && find /var/cache/apt/archives /var/lib/apt/lists -not -name lock -type f -delete \
    && find /var/cache -type f -delete

# RUN apt-get install -y --no-install-recommends libgl1 libglx-mesa0 libglib2.0-0 fonts-dejavu-core fontconfig

RUN groupadd --gid ${GID} appuser && useradd --uid ${UID} --gid ${GID} --create-home --shell /bin/bash appuser

USER $UID:$GID
ENV PATH=/home/appuser/.local/bin:$PATH

WORKDIR /app

RUN git clone https://github.com/comfyanonymous/ComfyUI.git
WORKDIR /app/ComfyUI

# Torch compiled for correct cuda (e.g. CUDA 12.4.1 -> cu124)
RUN CUDA_SHORT=$(echo $CUDA_VERSION | cut -d. -f1,2 | tr -d '.') \
    && pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu${CUDA_SHORT}

RUN pip install --no-cache-dir -r requirements.txt

# Manager
ARG MANAGER=/app/ComfyUI/user/__manager
RUN mkdir -p ${MANAGER} && \
    echo -e "[default]"                                                                      >  ${MANAGER}/config.ini && \
    echo -e "use_uv = False"                                                                 >> ${MANAGER}/config.ini && \
    echo -e "file_logging = False"                                                           >> ${MANAGER}/config.ini && \
    echo -e "db_mode = cache"                                                                >> ${MANAGER}/config.ini && \
    echo -e "database_url = sqlite://///app/ComfyUI/user/default/ComfyUI-Manager/manager.db" >> ${MANAGER}/config.ini && \
    chown -R ${UID}:${GID} ${MANAGER}
RUN pip install -r manager_requirements.txt && pip install matrix-nio

# Custom nodes
ARG CUSTOM_NODES=/app/ComfyUI/custom_nodes
RUN git clone --depth 1 https://github.com/cubiq/ComfyUI_essentials.git ${CUSTOM_NODES}/ComfyUI_essentials && \
    git clone --depth 1 https://github.com/crystian/ComfyUI-Crystools.git ${CUSTOM_NODES}/ComfyUI-Crystools && \
    git clone --depth 1 https://github.com/rgthree/rgthree-comfy.git ${CUSTOM_NODES}/rgthree-comfy && \
    git clone --depth 1 https://github.com/kijai/ComfyUI-KJNodes.git ${CUSTOM_NODES}/ComfyUI-KJNodes && \
    git clone --depth 1 https://github.com/ssitu/ComfyUI_UltimateSDUpscale.git ${CUSTOM_NODES}/ComfyUI_UltimateSDUpscale && \
    chown -R ${UID}:${GID} ${CUSTOM_NODES} && \
    for dir in /app/ComfyUI/custom_nodes/*/; do python3 -m pip install -r $dir/requirements.txt; done

EXPOSE 8188
CMD ["python3", "main.py", "--enable-manager", "--listen", "0.0.0.0"]
