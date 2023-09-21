The Kratos charmed Operator of the IAM Platform provides integrations to the Canonical Observability Stack.

In this reference we will provide a technical description of the alert rules, and the dashboards the Kratos operator passes to the components of the COS. We will also showcase the Metrics we use to provide observability features.


## Metrics

### up
#### Description

When this counter equals one, that means the instance the metric was scraped from is available to the Prometheus deployment. If the counter equals zero, or the metric is not present, then the application is inaccessible to the Prometheus deployment.

#### Source Component

Prometheus

#### Intended use

This metric signals whether a unit is unavailable. By specifying the label juju_unit this metric tells you whether the unit is available to the Prometheus component or not. Example: ```up{juju_unit="kratos/0"}```

#### Observed by
- **Alert Rules**: Rules in group KratosUnavailable
- **Dashboard**: Kratos Unit Availability

### level

#### Description

All Kratos logs have a level, to indicate the seriousness of an event. Kratos logs (and json formatted logs in general) can be filtered by log levels. 

#### Source Component

Loki

#### Usage

Use the LogQL’s abilities to enumerate log entries that match a regex template, and to parse json logs and populate fields such as level. Example: ```{juju_charm="kratos"} | json | level =~ `error` ```

#### Observed by

- **Alert Rules**: Rules in group KratosHighSeverityLog
- **Dashboard Visualisation**: Kratos High Severity Log Entries

## Alert rules

### KratosHighSeverityLog
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

### KratosUnavailable

#### Description

Alerts in this alert group observe the up metric of individual Kratos deployment units. In this context, a unit not being available by Prometheus is treated as being inactive. Alerts are fired when units are inactive for at least one minute.

#### Data Source

Prometheus

### KratosUnavailable-one

#### Description

One unit in a multi-unit deployment is inactive.

#### Observed failure

An operator instance has encountered an issue from which it can not recover within a minute. The alert also suggests that there are more than one healthy unit in the deployment.

#### Severity
Warning, because the service itself is still available for the foreseeable future.

### KratosUnavailable-multiple

#### Description
More than one unit in a multi-unit deployment is inactive.

#### Observed failure

Multiple operator instances have encountered an issue from which they can not recover within a minute. Without other alerts suggesting otherwise, the alert also suggests that there is at least one healthy unit in the deployment.

#### Severity

Error, because while the service is still available, there is now potential for a critical scenario.

### KratosUnavailable-all-except-one

#### Description

All but one unit in a multi-unit deployment is inactive.

#### Observed failure

Multiple operator instances have encountered an issue from which they can not recover within a minute. The next such error will result in loss of service.

#### Severity

Critical. The service is one error away from being inaccessible.

### KratosUnavailable-all

#### Description

No unit in the deployment is active.

#### Observed failure

None of the units in the deployment are active. The service is inaccessible.

#### Severity

Fatal. The service has failed, and can not recover without human intervention.

## Dashboards

### Kratos High Severity Log Entries

#### Description

Visualization for the number of log entries with levels error or above within 5 minutes spans.

#### Associated Alerts

Alert rules in alert group **KratosHighSeverityLog**.

### Kratos Unit Availability

#### Description

Visualization displaying the availability of Kratos units. 

#### Associated Alerts
Alert rules in alert group **KratosUnavailable**.

## Related documentation
A dedicated [How-To](/t/11911) is available detailing the process of deploying and integrating the IAM Platform bundle and the Canonical Observability Stack bundle.

# Navigation
[details=Navigation]
|Level|Path|Navlink|
|--|--|--|
| 1 | overview | [Home](/t/11825) |
| 1 | tutorials | [Tutorial](/t/11917) |
| 2 | tutorials/e2e-tutorial | [Getting started with the Canonical Identity Platform](/t/11916) |
| 1 | how-to | [How-to guides](/t/11911) |
| 2 | how-to/integrate-external-identity-provider | [Integrate with external identity providers](/t/11910) |
| 2 | how-to/integrate-oidc-compatible-charms | [Integrate with OIDC compatible charms ](/t/11909) |
| 2 | how-to/integrate-cos | [Integrate with Canonical Observability Stack](/t/11908) |
| 2 | how-to/ory-database-migration | [Perform Database Migration with Identity Platform Components](/t/11912) |
| 1 | explanation | [Explanation](/t/11907) |
| 2 | explanation/what-is-oidc | What is an OIDC compatible application? |
| 1 | reference | [Reference](/t/11915) |
| 2 | reference/bundles | Bundles |
| 3 | reference/bundles/identity-platform | [Identity Platform](https://charmhub.io/identity-platform) |
| 3 | reference/bundles/architecture | [Architecture](/t/11913) |
| 3 | reference/bundles/login-flow | [Login flow](/t/11914) |
| 2 | reference/observability | Observability setup |
| 3 | reference/observability/kratos-observability | [Kratos Observability](/t/11931) |
| 3 | reference/observability/hydra-observability | [Hydra Observability](/t/11930) |
| 3 | reference/observability/identity-platform-login-ui-observability | [Identity Platform Login UI Observability](/t/11932) |
| 2 | reference/kubernetes-charms | Kubernetes Charms |
| 3 | reference/kubernetes-charms/hydra | [Hydra](https://charmhub.io/hydra) |
| 3 | reference/kubernetes-charms/kratos | [Kratos](https://charmhub.io/kratos) |
| 3 | reference/kubernetes-charms/kratos-external-idp-integrator | [Kratos External IdP Integrator](https://charmhub.io/kratos-external-idp-integrator) |
| 3 | reference/kubernetes-charms/idp-ui | [Identity Platform Login UI](https://charmhub.io/identity-platform-login-ui-operator) |
[/details]