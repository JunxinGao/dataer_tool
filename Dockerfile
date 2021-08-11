FROM fastai/codespaces
RUN apt-get update && apt-get install -y htop unzip screen openssh-server sudo
 # !!! not permit root  login !!!
RUN sed -i "s/#PermitRootLogin.*/PermitRootLogin no/g" /etc/ssh/sshd_config \
    && mkdir /run/sshd \
    && echo "root:dind" | chpasswd
