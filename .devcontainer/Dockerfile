# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.140.1/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version: 3, 3.8, 3.7, 3.6
ARG VARIANT="3.8"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# Update args in docker-compose.yaml to set the UID/GID of the "vscode" user.
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN if [ "$USER_GID" != "1000" ] || [ "$USER_UID" != "1000" ]; \
        then groupmod --gid $USER_GID vscode && usermod --uid $USER_UID --gid $USER_GID vscode; \
    fi

# [Option] Install Node.js
ARG INSTALL_NODE="true"
ARG NODE_VERSION="lts/*"
RUN if [ "${INSTALL_NODE}" = "true" ]; \
        then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; \
    fi

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends \
#     <your-package-list-here> \
#     && rm -rf /var/lib/apt/lists/*

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# COPY requirements-dev.txt /tmp/pip-tmp/requirements.txt
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#     && rm -rf /tmp/pip-tmp

COPY .devcontainer/.zshrc /home/vscode/.zshrc
ARG ZSH_CUSTOM=/home/vscode/.oh-my-zsh/custom

RUN git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
RUN sed -i 's/%~/%2~/g' $ZSH_CUSTOM/themes/codespaces.zsh-theme
