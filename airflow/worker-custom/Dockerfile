# airflow-docker-worker:2.0.1

FROM apache/airflow:2.0.1

USER root
RUN set -eux; \
    apt-get update; \
    apt-get install -y gosu; \
    rm -rf /var/lib/apt/lists/*; \
    # verify that the binary works
    gosu nobody true
COPY worker-entrypoint.sh /custom-boot/worker-entrypoint.sh
# ENTRYPOINT [ "/bin/bash"]
ENTRYPOINT [ "/bin/bash", "/custom-boot/worker-entrypoint.sh" ]