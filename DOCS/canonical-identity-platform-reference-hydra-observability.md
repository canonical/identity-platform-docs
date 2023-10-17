The Hydra charmed Operator of the IAM Platform provides integrations to the Canonical Observability Stack.

In this reference we will provide a technical description of the alert rules, and the dashboards the Hydra operator passes to the components of the COS. We will also showcase the Metrics we use to provide observability features.

> See more: [Charmhub | Hydra > Integrations > `metrics-endpoint`,  `grafana-dashboard`](https://charmhub.io/hydra/integrations)

## Metrics

### up
#### Description

When this counter equals one, that means the instance the metric was scraped from is available to the Prometheus deployment. If the counter equals zero, or the metric is not present, then the application is inaccessible to the Prometheus deployment.

#### Source Component

Prometheus

#### Intended use

This metric signals whether a unit is unavailable. By specifying the label juju_unit this metric tells you whether the unit is available to the Prometheus component or not. Example: ```up{juju_unit="hydra/0"}```

#### Observed by
- **Alert Rules**: Rules in group HydraUnavailable
- **Dashboard**: Hydra Unit Availability

### level

#### Description

All Hydra logs have a level, to indicate the seriousness of an event. Hydra logs (and json formatted logs in general) can be filtered by log levels. 

#### Source Component

Loki

#### Usage

Use the LogQL’s abilities to enumerate log entries that match a regex template, and to parse json logs and populate fields such as level. Example: ```{juju_charm="hydra"} | json | level =~ `error` ```

#### Observed by

- **Alert Rules**: Rules in group HydraHighSeverityLog
- **Dashboard Visualisation**: Hydra High Severity Log Entries

## Alert rules

### HydraHighSeverityLog
#### Description

Alerts in this alert group are fired based on how many log entries with the log level of error, critical, or fatal have been created in the last five minutes.

#### Data Source

Loki

### LowFrequencyHighSeverityLog

#### Description

This alert is fired if the number of interested logs created in the last five minutes is at least one, but no more than one hundred. 

#### Observed failure

The alert does not necessitate a component failure, but could corroborate it. 

#### Severity

Warning. Without other alerts firing, it can be assumed that the deployment does not need human intervention yet. 

### HighFrequencyHighSeverityLog

#### Description

This alert is fired if the number of interested logs created in the last five minutes is more than one hundred. 

#### Observed failure

This alert could indicate that some application function is inaccessible due to missing external, or internal dependencies, or misconfiguration. The alert can also indicate that the application is being frequently restarted by the Pebble service because of application errors.
*Note*: This alert can also indicate problems with the client.

#### Severity

Error. Without other alerts firing, it can be assumed that the deployment is not in imminent danger of loss of service. 

### HydraUnavailable

#### Description

Alerts in this alert group observe the up metric of individual Hydra deployment units. In this context, a unit not being available by Prometheus is treated as being inactive. Alerts are fired when units are inactive for at least one minute.

#### Data Source

Prometheus

### HydraUnavailable-one

#### Description

One unit in a multi-unit deployment is inactive.

#### Observed failure

An operator instance has encountered an issue from which it can not recover within a minute. The alert also suggests that there are more than one healthy unit in the deployment.

#### Severity
Warning, because the service itself is still available for the foreseeable future.

### HydraUnavailable-multiple

#### Description
More than one unit in a multi-unit deployment is inactive.

#### Observed failure

Multiple operator instances have encountered an issue from which they can not recover within a minute. Without other alerts suggesting otherwise, the alert also suggests that there is at least one healthy unit in the deployment.

#### Severity

Error, because while the service is still available, there is now potential for a critical scenario.

### HydraUnavailable-all-except-one

#### Description

All but one unit in a multi-unit deployment is inactive.

#### Observed failure

Multiple operator instances have encountered an issue from which they can not recover within a minute. The next such error will result in loss of service.

#### Severity

Critical. The service is one error away from being inaccessible.

### HydraUnavailable-all

#### Description

No unit in the deployment is active.

#### Observed failure

None of the units in the deployment are active. The service is inaccessible.

#### Severity

Fatal. The service has failed, and can not recover without human intervention.

## Dashboards

### Hydra High Severity Log Entries

#### Description

Visualization for the number of log entries with levels error or above within 5 minutes spans.

#### Associated Alerts

Alert rules in alert group **HydraHighSeverityLog**.

### Hydra Unit Availability

#### Description

Visualization displaying the availability of Hydra units. 

#### Associated Alerts
Alert rules in alert group **HydraUnavailable**.

## Related documentation
A dedicated [How-To](/t/11911) is available detailing the process of deploying and integrating the IAM Platform bundle and the Canonical Observability Stack bundle.
