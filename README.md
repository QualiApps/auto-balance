Consul-template + HAProxy
==============
It provides automatic configuration of HAProxy with Consul template.

Depends on: Consul cluster

Installation
--------------

1. Install [Docker](https://www.docker.com)

2. Download automated build from public Docker Hub Registry: `docker pull qapps/auto-balance`
(alternatively, you can build an image from Dockerfile: `docker build -t="qapps/auto-balance" github.com/qualiapps/auto-balance`)

**Running**

`docker run -d -P --name haproxy qapps/auto-balance`

**additional options:**

- `-e "CONSUL_ADDR=ip"`: ip - consul IP address or DNS name. Default: consul

- `-e "CONSUL_PORT=port"`: port - consul port: Default: 8500

- `-p 1883:1883 -p 15672:15672`: two port exposed (1883, 15672)


###Register a new app in HAProxy

You need to add a new key and subkeys into the Consul key/value storage.

**Example:**

- add a new app key to the key **service/haproxy/listen** (service/haproxy/listen/**app_key**);

- then you need to add subkeys to your app_key with values:

    - key: `bind`, value (*:80) `required`

    - key: `balance`, value (roundrobin, leastconn) Default: roundrobin

    - key: `mode`, value (http, tcp) Default: http

    - key: `service`, value (your service name in the Consul, may be with tag) `required`