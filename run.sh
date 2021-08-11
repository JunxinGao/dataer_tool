#!/bin/bash
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"

USER_NAME=${USER_NAME:-user}
USER_UID=${USER_UID:-1001}
USER_GID=${USER_GID:-1001}
USER_PW=${USER_PW:-${USER_NAME}}
JUPYTER_PW=${USER_PW:-${USER_NAME}}
WORK_HOME=${WORK_HOME:-"/home/${USER_NAME}"}
SUDO_GROUP=${SUDO_GROUP:-sudo}

if id -u ${USER_NAME} > /dev/null 2>&1; then
    echo "user: ${USER_NAME} exist"
else
    useradd ${USER_NAME} -s /bin/bash -d ${WORK_HOME} -u ${USER_UID} -m
    echo "user: ${USER_NAME} added"
fi

echo "${USER_NAME}:${USER_PW}" | chpasswd && usermod ${USER_NAME} -aG ${SUDO_GROUP}

sed -i "s/#%wheel/%wheel/g" /etc/sudoers
sed -i "s/# %wheel/%wheel/g" /etc/sudoers
sed -i "s/#%sudo/%sudo/g" /etc/sudoers
sed -i "s/# %sudo/%sudo/g" /etc/sudoers

if [ -d ${WORK_HOME} ]; then
    chown ${USER_UID}:${USER_GID} ${WORK_HOME}
fi

if [ ! -d /run/sshd ]; then
    mkdir /run/sshd
fi

/usr/sbin/sshd -D &

echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"

echo "$USER_NAME : starting jupyter..."

JUPYTER_PW=`python3 -c "from notebook.auth import passwd; print(passwd('$JUPYTER_PW'))"`

su $USER_NAME -c "pip install -e . && jupyter notebook --allow-root --no-browser --ip=0.0.0.0 --port=8080 --NotebookApp.token='' --NotebookApp.password='$JUPYTER_PW'"
