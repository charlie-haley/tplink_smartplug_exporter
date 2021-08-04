# tplink_smartplug_exporter
![docker-publish](https://github.com/charlie-haley/tplink_smartplug_exporter/actions/workflows/docker-publish.yml/badge.svg)

Prometheus Exporter for TP-Link Smart Plugs

## Installation

The exporter listens on port `9784` by default.

### Docker
```
 docker run -d \
    -e HS1X_HOSTS='192.168.1.156:9999,192.168.1.159:9999' \
    -p 9784:9784 \
    --name tplink_smartplug_exporter \
    chhaley/tplink_smartplug_exporter
```

### Helm
```
helm repo add charlie-haley http://charts.charliehaley.dev
helm repo update
helm install tplink-smartplug-exporter charlie-haley/tplink-smartplug-exporter --set "hs1xHosts={"192.168.1.156:9999","192.168.1.159:9999"}" -n monitoring
```
If you want to use the ServiceMonitor (which is enabled by default) you'll need to have [prometheus-operator](https://github.com/prometheus-operator/prometheus-operator) deployed to your cluster, see [values](https://github.com/charlie-haley/private-charts/blob/main/charts/tplink-smartplug-exporter/values.yaml) to disable it if you'd like use ingress instead.

[You can find the chart repo here](https://github.com/charlie-haley/private-charts), if you'd like to contribute. 

## Metrics
Name     | Description                             | Labels
------------|--------------------------------------|------
current_ma  | Current being used in milliamps      | host
voltage_mv  | Voltage being used in millivolts     | host
power_mw    | Watts being used in milliwatts       | host
total_wh    | Total watt-hours                     | host
