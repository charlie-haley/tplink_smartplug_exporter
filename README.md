# tplink_smartplug_exporter
Prometheus Exporter for TP-Link Smart Plugs

## Installation

The exporter listens on port `9784` by default.

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
If you want to use the ServiceMonitor (which is enabled by default) you'll need to have [prometheus-operator](https://github.com/prometheus-operator/prometheus-operator) deployed to your cluster, see [values](charts/tplink-smartplug-exporter/values.yaml) to disable it if you'd like use ingress instead.


## Metrics
Name     | Description
---------|-------------------------------------------------------------------------
current_ma | Current being used in milliamps
voltage_mv  | Voltage being used in millivolts
power_mw  | Watts being used in milliwatts
total_wh | Total watt-hours
