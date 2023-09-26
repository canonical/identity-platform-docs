This document shows how to integrate the different components of the [Canonical Identity platform]() with the [Canonical Observability Stack](https://charmhub.io/topics/canonical-observability-stack) to enable the preconfigured dashboard and alerting rules.

The Canonical Observability Stack ([COS-Lite](https://charmhub.io/topics/canonical-observability-stack)) is a Juju bundle that includes a series of open source observability applications and related automation. For the complete list of components in the COS, read the [Component List](https://charmhub.io/topics/canonical-observability-stack/editions/lite).

## Prerequisites

- A running [COS-Lite](https://charmhub.io/topics/canonical-observability-stack) bundle. You can follow the [Getting started on MicroK8s](https://charmhub.io/topics/canonical-observability-stack/tutorials/install-microk8s) tutorial to get you started. Make sure to follow the section **Deploy the COS Lite** bundle with overlays sections.
- A running Canonical Identity Platform bundle. Please refer to the [tutorial](/t/11916).

It is generally recommended to keep the observability stack separate from any observed applications to separate failure domains. This document assumes that the Identity Platform and the COS bundles are deployed to different models.

# Integration approaches

There are 2 possible  integration approaches depending on your networking / deployment setup setup:

1. If you are able to send metrics and logs directly to the observability platform components follow the **Integrate the Identity Platform charms with COS-Lite** section
2. If you prefer using a telemetry collector component follow the **Integrate the Identity Platform charms with COS-Lite through Grafana-Agent** section

## Integrate the Identity Platform charms with COS-Lite 
### Grafana integration 
Assuming you deployed the COS-Lite bundle in model cos-model with user admin, use the following commands to integrate the Identity applications by means of an application offer.

```
juju integrate kratos admin/cos-model.grafana-dashboards
juju integrate hydra admin/cos-model.grafana-dashboards
juju integrate identity-platform-login-ui-operator admin/cos-model.grafana-dashboards
juju integrate traefik-admin admin/cos-model.grafana-dashboards
juju integrate traefik-public admin/cos-model.grafana-dashboards
```

### Loki integration 
Assuming you deployed the COS-Lite bundle in model cos-model with user admin, use the following commands to integrate the Identity applications by means of an application offer.
```
juju integrate kratos admin/cos-model.loki-logging
juju integrate hydra admin/cos-model.loki-logging
juju integrate identity-platform-login-ui-operator admin/cos-model.loki-logging
juju integrate traefik-admin admin/cos-model.loki-logging
juju integrate traefik-public admin/cos-model.loki-logging
```

### Prometheus integration 
Assuming you deployed the COS-Lite bundle in model cos-model with user admin, use the following commands to integrate the Identity applications by means of an application offer.
```
juju integrate kratos admin/cos-model.prometheus-scrape
juju integrate hydra admin/cos-model.prometheus-scrape
juju integrate identity-platform-login-ui-operator admin/cos-model.prometheus-scrape
juju integrate traefik-admin admin/cos-model.prometheus-scrape
juju integrate traefik-public admin/cos-model.prometheus-scrape
```

## Integrate the Identity Platform charms with COS-Lite through Grafana-Agent

You first need to deploy the [Grafana-Agent](https://charmhub.io/grafana-agent-k8s) operator, which is a telemetry collector used to aggregate and push information to the COS-lite bundle

To deploy Grafana-Agent run:
```
juju deploy grafana-agent-k8s --channel edge --trust
```

### Forward Prometheus metrics
Integrate Grafana-Agent with the Identity Stack Components by running the following commands:
```
juju integrate grafana-agent-k8s kratos:metrics-endpoint
juju integrate grafana-agent-k8s hydra:metrics-endpoint
juju integrate grafana-agent-k8s identity-platform-login-ui-operator:metrics-endpoint
juju integrate grafana-agent-k8s traefik-admin:metrics-endpoint
juju integrate grafana-agent-k8s traefik-public:metrics-endpoint
```

### Forward Loki metrics
Integrate Grafana-Agent with the Identity Stack Components by running the following commands:
```
juju integrate grafana-agent-k8s kratos:logging
juju integrate grafana-agent-k8s hydra:logging
juju integrate grafana-agent-k8s identity-platform-login-ui-operator:logging
juju integrate grafana-agent-k8s traefik-admin:logging
juju integrate grafana-agent-k8s traefik-public:logging
```

### Integrate Grafana-Agent with COS-Lite
Assuming you deployed the COS-Lite bundle in model cos-model with user admin, use this command to integrate the Grafana-Agent with Prometheus by means of an application offer.
```
juju integrate grafana-agent-k8s admin/cos-model.prometheus-receive-remote-write
```

Assuming you deployed the COS-Lite bundle in model cos-model with user admin, use this command to integrate the Grafana-Agent with Loki by means of an application offer.
```
juju integrate grafana-agent-k8s admin/cos-model.loki-logging
```

# Access the dashboards
You can get the Grafana IP address with the [juju status](https://juju.is/docs/juju/status) command. The default port for the Grafana HTTP server is 3000.

The default credentials are:
```
**Username**: admin 
**Password** you can get the password with the juju action [get-admin-password](https://charmhub.io/grafana-k8s/actions).
```

Once in, you will see a vertical menu bar on the left side of the page. You will find the available alerts by clicking on the Alerting menu. You will find the available dashboards by clicking on the Dashboards menu

You can find a technical description of the observability setup in the related [reference section](/t/11915) of the docs.
