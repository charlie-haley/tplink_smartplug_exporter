# tplink_smartplug_exporter
Prometheus Exporter for TP-Link Smart Plugs

## Installation

### Docker
```
 docker run -d \
    -e HS1X_HOSTS='192.168.1.156:9999,192.168.1.159:9999' \
    --network host \
    --name tplink_smartplug_exporter \
    chhaley/tplink_smartplug_exporter
```
