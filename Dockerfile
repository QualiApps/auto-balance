#Consul template + HAProxy

FROM fedora:21

MAINTAINER Yury Kavaliou <Yury_Kavaliou@epam.com>

RUN yum install -y haproxy \
    tar

ADD https://github.com/hashicorp/consul-template/releases/download/v0.9.0/consul-template_0.9.0_linux_amd64.tar.gz /tmp/consul-template.tar.gz
RUN tar -xf /tmp/consul-template.tar.gz \
    && mv consul-template_0.9.0_linux_amd64/consul-template /bin/consul-template \
    && chmod a+x /bin/consul-template

COPY ./files/start_lb.sh /usr/local/sbin/start_lb.sh
COPY ./files/hp_reinit.sh /usr/local/sbin/hp_reinit.sh
COPY ./files/haproxy.ctmpl /etc/haproxy/haproxy.ctmpl
COPY ./files/haproxy.cfg /ets/haproxy/haproxy.cfg

RUN chmod u+x /usr/local/sbin/start_lb.sh \
    /usr/local/sbin/hp_reinit.sh

ENTRYPOINT [ "/bin/bash", "/usr/local/sbin/start_lb.sh" ]
