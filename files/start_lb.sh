#!/bin/bash

PIDFILE="/var/run/haproxy.pid"
CONFIG_FILE=${HAPROXY}/haproxy.cfg

haproxy -f "$CONFIG_FILE" -p "$PIDFILE" -D -st $(cat $PIDFILE)

/usr/local/bin/consul-template -consul ${CONSUL_ADDR:-consul}:${CONSUL_PORT:-8500} \
    -template "/etc/haproxy/haproxy.ctmpl:/etc/haproxy/haproxy.cfg:/hp_reinit.sh" \
    -log-level debug