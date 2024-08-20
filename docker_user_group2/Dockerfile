# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN rm -f /etc/apt/apt.conf.d/docker-clean && \
    echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
RUN  --mount=type=cache,target=/var/cache/apt,mode=0755,sharing=private \
    --mount=type=cache,target=/var/lib/apt,mode=0755,sharing=private \
    set -eux \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    iputils-ping \
    curl \
    gosu \
    && apt-get clean -y \
    # verify that the binary works
    && gosu nobody true

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
ENV SC_USER_ID=5678 \
    SC_USER_NAME=scu \
    SC_BUILD_TARGET=base \
    SC_BOOT_MODE=default

RUN adduser \
    --uid ${SC_USER_ID} \
    --disabled-password \
    --gecos "" \
    --shell /bin/sh \
    --home /home/${SC_USER_NAME} \
    ${SC_USER_NAME}
RUN chown -R ${SC_USER_NAME} /app

# to fit with docker-compose
ENV SIDECAR_COMP_SERVICES_SHARED_FOLDER=/shared_computational_data
# USER appuser
ENTRYPOINT [ "/bin/sh", "/app/dask-entrypoint.sh" ]
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
