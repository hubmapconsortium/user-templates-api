# Parent image
FROM hubmap/api-base-image:1.0.0

LABEL description="HuBMAP User Templates API Service"

WORKDIR /code
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /tmp/

RUN echo $'[nginx-mainline]\n\
name=nginx mainline repo\n\
baseurl=http://nginx.org/packages/mainline/centos/$releasever/$basearch/\n\
gpgcheck=1\n\
enabled=0\n\
gpgkey=https://nginx.org/keys/nginx_signing.key\n\
module_hotfixes=true\n'\
>> /etc/yum.repos.d/nginx.repo

# Reduce the number of layers in image by minimizing the number of separate RUN commands
# 1 - Install the prerequisites
# 2 - By default, the repository for stable nginx packages is used. We would like to use mainline nginx packages
# 3 - Install nginx (using the custom yum repo specified earlier)
# 4 - Remove the default nginx config file
# 5 - Overwrite the nginx.conf with ours to run nginx as non-root
# 6 - Remove the nginx directory copied from host machine (nginx/conf.d gets mounted to the container)
# 7 - Upgrade pip (the one installed in base image may be old) and install flask app dependencies (pip3 also works)
# 8 - Make the start script executable
# 9 - Clean all yum cache
RUN yum install -y yum-utils && \
    yum-config-manager --enable nginx-mainline && \
    yum install -y nginx && \
    rm /etc/nginx/conf.d/default.conf && \
    pip install --upgrade pip -r /tmp/requirements.txt && \
    yum clean all

# The EXPOSE instruction informs Docker that the container listens on the specified network ports at runtime.
# EXPOSE does not make the ports of the container accessible to the host.
# Here 5000 is for the uwsgi socket, 8080 for nginx
EXPOSE 5001
