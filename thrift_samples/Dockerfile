ARG BASE_IMAGE=jupyter/base-notebook
FROM ${BASE_IMAGE}  AS base

LABEL maintainer="sanderegg"
EXPOSE 8888

# ----------------------------------------------------------------
# Add a python2 kernel in the notebook
# Create a Python 2.x environment using conda including at least the ipython kernel
# and the kernda utility. Add any additional packages you want available for use
# in a Python 2 notebook to the first line here (e.g., pandas, matplotlib, etc.)
RUN conda create --quiet --yes -p $CONDA_DIR/envs/python2 python=2.7 ipython ipykernel kernda && \
    conda clean -tipsy
USER root
# Create a global kernelspec in the image and modify it so that it properly activates
# the python2 conda environment.
RUN $CONDA_DIR/envs/python2/bin/python -m ipykernel install && \
$CONDA_DIR/envs/python2/bin/kernda -o -y /usr/local/share/jupyter/kernels/python2/kernel.json
USER $NB_USER

# healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "python3", "/docker/healthcheck.py" ]
#

ENV NOTEBOOK_URL="notebooks/thrift_stuff.ipynb"

FROM base AS development
VOLUME /home/$NB_USER/docker
VOLUME /home/$NB_USER/notebooks
VOLUME /home/$NB_USER/thrift
ENV DEBUG=1
CMD [ "/bin/bash", "docker/boot.sh" ]

FROM base AS production
# prepare for booting
COPY --chown=jovyan:users /docker /home/$NB_USER/docker
# install simcore packages
COPY --chown=jovyan:users /notebooks /home/$NB_USER/notebooks
COPY --chown=jovyan:users /thrift /home/$NB_USER/thrift
# copy the default notebook
RUN pip install /home/${NB_USER}/thrift/thrift/lib/py

ENTRYPOINT [ "/bin/bash", "docker/boot.sh" ]