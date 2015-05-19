#!/usr/bin/python

import consul
import syslog
import os
import subprocess


class PreInit(object):
    """
    This class to put scheme into the Consul key/value store for HAProxy and Consul template.
    @param env CONSUL_SERVICE_NAME - the dns name of consul service. Default: consul

    @param env FEED_MQTT_NAME - the dns name of rabbitmq service. Default: mqtt.feed
    @param env FEED_MQTT_PORT - the port of mqtt protocol. Default: 1883

    @param env FEED_UI_NAME - the dns name of rabbitmq service. Default: ui.feed
    @param env FEED_UI_PORT - the port of rabbitmq UI. Default: 15672

    @param env UI_NAME - the dns name of Kibana UI. Default: ui
    @param env UI_PORT - Default: 5601

    @param env MONITORING_UI_NAME - the dns name of sensu server UI. Default: ui.monitoring
    @param env MONITORING_UI_PORT - Default: 3000
    """
    consul_service = os.environ.get("CONSUL_SERVICE_NAME", "192.168.56.100")  # consul
    ha_main_key = "service/haproxy/"
    ha_key = ha_main_key + "listen/mqtt/balance"
    kv_data = {
        ha_main_key: [
            {"maxconn": 512},
            {"mode": "http"},
            {"timeouts/": [
                {"check": 3000},
                {"client": 10000},
                {"connect": 5000},
                {"server": 10000},
            ]},
            {"listen/mqtt/": [
                {"balance": "roundrobin"},
                {"bind": ":".join(("*", os.environ.get("FEED_MQTT_PORT", "1883")))},
                {"mode": "tcp"},
                {"service": os.environ.get("FEED_MQTT_NAME", "mqtt.feed")},
            ]},
            {"listen/feed/": [
                {"balance": "roundrobin"},
                {"bind": ":".join(("*", os.environ.get("FEED_UI_PORT", "15672")))},
                {"mode": "http"},
                {"service": os.environ.get("FEED_UI_NAME", "ui.feed")},
            ]},
            {"listen/kibana/": [
                {"balance": "roundrobin"},
                {"bind": ":".join(("*", os.environ.get("UI_PORT", "5601")))},
                {"mode": "http"},
                {"service": os.environ.get("UI_NAME", "ui")},
            ]},
            {"listen/uchiwa/": [
                {"balance": "roundrobin"},
                {"bind": ":".join(("*", os.environ.get("MONITORING_UI_PORT", "3000")))},
                {"mode": "http"},
                {"service": os.environ.get("MONITORING_UI_NAME", "ui.monitoring")},
            ]},
        ],
    }

    def __init__(self):
        self.init_script = "/usr/local/sbin/start_lb.sh"
        self.consul_cluster_client = None
        self.run()

    def run(self):
        self.consul_cluster_client = consul.Consul(self.consul_service)  # consul service name (dns works)
        self._init_ha_kv()
        self.run_service()

    def run_service(self, args=[]):
        """runs service"""
        try:
            subprocess.call([self.init_script] + args)
        except Exception as e:
            syslog.syslog(syslog.LOG_ERR, "HA KV Pre-init:run_service Error: " + e.__str__())

    def _init_ha_kv(self):
        """posts kv to the consul storage"""
        try:
            ha_kv = self.consul_cluster_client.kv.get(self.ha_key)[1]
            if not ha_kv:
                for item in self.kv_data[self.ha_main_key]:
                    key = item.keys()[0]
                    value = item[key]
                    if isinstance(value, list):
                        for sub_item in value:
                            sub_key = sub_item.keys()[0]
                            sub_value = sub_item[sub_key]
                            self._put_data(key + sub_key, sub_value)
                    else:
                        self._put_data(key, value)
            else:
                syslog.syslog(syslog.LOG_INFO,
                              "HA KV Pre-init: HAProxy key/value " + self.ha_main_key + " already exists.")
        except Exception as e:
            syslog.syslog(syslog.LOG_ERR, "HA KV Pre-init:_init_ha_kv Error: " + e.__str__())

    def _put_data(self, key, value):
        return self.consul_cluster_client.kv.put(self.ha_main_key + key, str(value), cas=0)


if __name__ == "__main__":
    f = PreInit()