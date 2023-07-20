#!/bin/sh
set -o errexit
set -o nounset

IFS=$(printf '\n\t')

msg_prefix="INFO: [$(basename "$0")] "

print_info() {
  # ANSI escape code for yellow color
  YELLOW='\033[33m'
  # ANSI escape code to reset color to default
  RESET='\033[0m'

  # Concatenate the YELLOW code, the log message, and the RESET code to reset color
  printf "${YELLOW}${msg_prefix}: %s${RESET}\n" "$1"
}

check_docker_access() {
  # Run the "docker version" command inside command substitution
  if docker_version_output=$(docker version 2>/dev/null); then
    echo "yes"
  else
    echo "no"
  fi
}



print_info "Booting in ${SC_BOOT_MODE} mode ..."
print_info "User :$(id)"
print_info "Workdir : $(pwd)"
print_info ""
print_info "docker engine access...$(check_docker_access)"

#
# DEVELOPMENT MODE
#
# - prints environ info
# - installs requirements in mounted volume
#
if [ "${SC_BUILD_TARGET}" = "development" ]; then
  print_info "Environment :"
  printenv | sed 's/=/: /' | sed 's/^/    /' | sort
  print_info "Python :"
  python --version | sed 's/^/    /'
  command -v python | sed 's/^/    /'

  # cd services/autoscaling || exit 1
  # pip --quiet --no-cache-dir install -r requirements/dev.txt
  # cd - || exit 1
  print_info "PIP :"
  pip --no-cache list | sed 's/^/    /'
fi

#
# RUNNING application
#

APP_LOG_LEVEL=${API_SERVER_LOGLEVEL:-${LOG_LEVEL:-${LOGLEVEL:-INFO}}}
SERVER_LOG_LEVEL=$(echo "${APP_LOG_LEVEL}" | tr '[:upper:]' '[:lower:]')
print_info "Log-level app/server: $APP_LOG_LEVEL/$SERVER_LOG_LEVEL"

if [ "${SC_BOOT_MODE}" = "development" ]; then
  print_info $(ls -tlah)
  exec uvicorn app.src.app:app \
      --host 0.0.0.0 \
      --reload \
      --log-level ${SERVER_LOG_LEVEL}
else
  exec uvicorn app.src.app:app \
    --host 0.0.0.0 \
    --log-level "${SERVER_LOG_LEVEL}"
fi
