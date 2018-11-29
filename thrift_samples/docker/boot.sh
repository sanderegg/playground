#!/bin/bash

if test "${DEBUG}" = "1"
then
    pip install /home/${NB_USER}/thrift/thrift/lib/py
fi

jupyter trust ${NOTEBOOK_URL}
start-notebook.sh \
    --NotebookApp.notebook_dir=/home/${NB_USER}/notebooks \
    --NotebookApp.token='' #\
    --NotebookApp.default_url=${NOTEBOOK_URL} #uncomment this to start the notebook right away in that mode
    
