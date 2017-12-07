FROM centos/httpd-24-centos7
#FROM httpd
#COPY webconf /opt/app-root/src
#WORKDIR /opt/app-root/src
#RUN yum -y update; yum clean all; yum -y install python-pip; yum clean all

USER root
RUN yum -y update; yum clean all
RUN yum -y install yum-utils; yum -y groupinstall development; yum -y install https://centos7.iuscommunity.org/ius-release.rpm
#RUN yum -y install epel-release
#RUN yum -y install python-pip; yum clean all
#RUN pip install -r requirements.txt
RUN yum -y install python36u; yum -y install python36u-pip; yum -y install python36u-devel

COPY webconf /opt/app-root/src
WORKDIR /opt/app-root/src

RUN pip3.6 install -r requirements.txt
RUN echo 'Listen 127.0.0.1:8080\n\
ServerName TestServer:80\n\
DocumentRoot "/var/www/site"' > /etc/httpd/conf.d/httpd.conf

#RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip
#RUN pip3 install -r requirements.txt
#  && ../patch_bootstrap3_datetime.sh
EXPOSE 8000
CMD ["gunicorn", "-b :8000", "webconf.wsgi"]

