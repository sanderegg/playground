# syntax=docker/dockerfile:1
# 
# base python image with generic settings
#
ARG PYTHON_VERSION="3.10.10"
FROM python:${PYTHON_VERSION}-slim-buster as base

# prevent debian from auto-removing apt packages in docker containers: [https://vsupalov.com/buildkit-cache-mount-dockerfile/]
RUN rm -f /etc/apt/apt.conf.d/docker-clean && \
    echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Sets utf-8 encoding for Python et al
ENV LANG=C.UTF-8

# server port
EXPOSE 8000
# if used debugging port
EXPOSE 3000

# Creates a non-root user with an explicit UID
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
ENV SC_USER_NAME=scu
RUN adduser \
    -u 5678 \
    --disabled-password \
    --gecos "" \
    --home /home/${SC_USER_NAME} \
    ${SC_USER_NAME}

# Define the python virtual environment in the home folder
ENV VIRTUAL_ENV=/home/${SC_USER_NAME}/.venv

# Ensures that the python and pip executables used in the image will be
# those from our virtualenv.
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"


FROM base as runtime-dependencies
#
# install dependencies needed at runtime for both dev/prod images
#

# install docker
RUN --mount=type=cache,target=/var/cache/apt,mode=0755,sharing=private \
    --mount=type=cache,target=/var/lib/apt,mode=0755,sharing=private \
    set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    # only the cli is needed and we remove the unnecessary stuff again
    docker-ce-cli \
    && apt-get remove -y\
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    && apt-get clean -y


# define entrypoint command
ENTRYPOINT ["/bin/sh", "app/docker/boot.sh"]

FROM runtime-dependencies as python-build
#
# install/build python packages that will be moved to production to reduce final image footprint
#

# python virtualenv is used here such that installed
# packages may be moved to production image easily by copying the venv
RUN python -m venv "${VIRTUAL_ENV}"

# update pip
RUN --mount=type=cache,mode=0755,target=/root/.cache/pip \
    pip install --upgrade  \
    pip~=23.1  \
    wheel \
    setuptools

# Install package
RUN --mount=type=bind,source=requirements.txt,target=requirements.txt,rw \
    --mount=type=cache,mode=0755,target=/root/.cache/pip \
    python -m pip install -r requirements.txt


FROM runtime-dependencies as production
#
# smallest footprint image to run in production
#


# copy sources
WORKDIR /home/${SC_USER_NAME}
COPY --chown=${SC_USER_NAME}:${SC_USER_NAME} ./services/app /home/${SC_USER_NAME}/app



# Copies pre-installed virtualenv and packages from build stage
COPY --chown=${SC_USER_NAME}:${SC_USER_NAME} --from=python-build  ${VIRTUAL_ENV} ${VIRTUAL_ENV}

RUN  chown -R ${SC_USER_NAME} /home/${SC_USER_NAME}/app

USER ${SC_USER_NAME}

ENV SC_BOOT_MODE=production
ENV SC_BUILD_TARGET=production
ENV PYTHONOPTIMIZE=TRUE

FROM python-build as development
#
# development image for local runs, src files shall be mounted
#
WORKDIR /devel
ENV SC_BOOT_MODE=development
ENV SC_BUILD_TARGET=development