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

### Helm
```
helm repo add charlie-haley https://charlie-haley.github.io/tplink_smartplug_exporter/
helm repo update
helm install tplink-smartplug-exporter charlie-haley/tplink-smartplug-exporter --set "hs1xHosts={"192.168.1.156:9999","192.168.1.159:9999"}" -n monitoring
```