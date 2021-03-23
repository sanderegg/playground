#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail

IFS=$(printf '\n\t')

INFO="INFO: [$(basename "$0")] "
WARNING="WARNING: [$(basename "$0")] "
ERROR="ERROR: [$(basename "$0")] "

# This entrypoint script:
#
# - Executes *inside* of the container upon start as --user [default root]
# - Notice that the container *starts* as --user [default root] but
#   *runs* as non-root user [scu]
#
echo "$INFO" "custom entrypoint..."
echo   User    :"$(id "$(whoami)")"
echo   Workdir :"$(pwd)"


function create_system_user_if_missing() {
    # This is needed in case of OpenShift-compatible container execution. In case of OpenShift random
    # User id is used when starting the image, however group 0 is kept as the user group. Our production
    # Image is OpenShift compatible, so all permissions on all folders are set so that 0 group can exercise
    # the same privileges as the default "airflow" user, this code checks if the user is already
    # present in /etc/passwd and will create the system user dynamically, including setting its
    # HOME directory to the /home/airflow so that (for example) the ${HOME}/.local folder where airflow is
    # Installed can be automatically added to PYTHONPATH
    if ! id "${AIRFLOW_UID}" &> /dev/null; then
      THE_USER_NAME="default"
      if [[ -w /etc/passwd ]]; then
        echo "${THE_USER_NAME}:x:${AIRFLOW_UID}:0:${THE_USER_NAME} user:${AIRFLOW_USER_HOME_DIR}:/sbin/nologin" \
            >> /etc/passwd
      fi
    #   export HOME="${AIRFLOW_USER_HOME_DIR}"
    fi
}

create_system_user_if_missing
echo   airflow User name/id    :"$(id "${AIRFLOW_UID}")"/${AIRFLOW_UID}
THE_USER_NAME="$(id "${AIRFLOW_UID}")"
# Appends docker group if socket is mounted
DOCKER_MOUNT=/var/run/docker.sock
if stat $DOCKER_MOUNT > /dev/null 2>&1
then
    echo "$INFO detected docker socket is mounted, adding user to group..."
    GROUPID=$(stat --format=%g $DOCKER_MOUNT)
    GROUPNAME=scdocker

    if ! addgroup --gid "$GROUPID" $GROUPNAME > /dev/null 2>&1
    then
        echo "$WARNING docker group with $GROUPID already exists, getting group name..."
        # if group already exists in container, then reuse name
        GROUPNAME=$(getent group "${GROUPID}" | cut --delimiter=: --fields=1)
        echo "$WARNING docker group with $GROUPID has name $GROUPNAME"
    fi
    adduser "${THE_USER_NAME}" "$GROUPNAME"
fi


echo "$INFO Starting $* ..."
echo "  ${THE_USER_NAME} rights    : $(id "${THE_USER_NAME}")"
echo "  local dir : $(ls -al)"
exec gosu "${AIRFLOW_UID}" "/entrypoint" "$@"
