Consul-template + HAProxy
==============
It provides automatic configuration of HAProxy with Consul template.

Depends on: Consul cluster

Installation
--------------

1. Install [Docker](https://www.docker.com)

2. Download automated build from public Docker Hub Registry: `docker pull qapps/auto-balance`
(alternatively, you can build an image from Dockerfile: `docker build -t="qapps/auto-balance" github.com/qualiapps/auto-balance`)

Running
-----------------

`docker run -d -P -v /sys/fs/cgroup:/home/cgroup -v /:/home/disk -h $(hostname) -e "NODE_NAME=$(hostname)" -e "NODE_IP=$(hostname -i)" --link rabbitmq:rmq --name sensuClient qapps/sensu-client`

`rabbitmq` - your rabbit container name

###Add new access for any app