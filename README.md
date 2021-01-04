# tplink_smartplug_exporter
Prometheus Exporter for TP-Link Smart Plugs

## Installation

### Docker
Replace HS1X_HOSTS with a comma seperated list of your devices. (e.g "192.168.1.55:9999, 192.168.1.124:9999")
```
 docker run -d \
 -e HS1X_HOSTS='192.168.1.55:9999' \
 --network host \
 --name tplink_smartplug_exporter \
 chhaley/tplink_smartplug_exporter
```
