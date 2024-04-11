The OpenFGA charmed Operator provides integrations to the Canonical Observability Stack.

In this reference we will provide a technical description of the alert rules, and the dashboards the OpenFGA operator passes to the components of the COS. We will also showcase the Metrics we use to provide observability features.

> See more: [Charmhub | OpenFGA > Integrations > `metrics-endpoint`,  `grafana-dashboard`](https://charmhub.io/openfga/integrations)



**Contents:**
* [Metrics](#heading--0000)
  * [up](#heading--0001)
    * [Description](#heading--0002)
    * [Source Component](#heading--0003)
    * [Intended use](#heading--0004)
    * [Observed by](#heading--0005)
  * [level](#heading--0006)
    * [Description](#heading--0007)
    * [Source Component](#heading--0008)
    * [Usage](#heading--0009)
    * [Observed by](#heading--0010)
* [Alert rules](#heading--0011)
  * [OpenFGAHighSeverityLog](#heading--0012)
    * [Description](#heading--0013)
    * [Data Source](#heading--0014)
  * [OpenFGAUnavailable-multiple](#heading--0015)
    * [Description](#heading--0016)
    * [Observed failure](#heading--0017)
    * [Severity](#heading--0018)
  * [OpenFGAUnavailable-all](#heading--0019)
    * [Description](#heading--0020)
    * [Observed failure](#heading--0021)
    * [Severity](#heading--0022)
* [Dashboards](#heading--0023)
  * [OpenFGA High Severity Log Entries](#heading--0024)
    * [Description](#heading--0025)
    * [Associated Alerts](#heading--0026)
  * [OpenFGA Unit Availability](#heading--0027)
    * [Description](#heading--0028)
    * [Associated Alerts](#heading--0029)

<a href="#heading--0000"><h2 id="heading--0000">Metrics</h2></a>

<a href="#heading--0001"><h3 id="heading--0001">up</h3></a>
<a href="#heading--0002"><h4 id="heading--0002">Description</h4></a>

When this counter equals one, that means the instance the metric was scraped from is available to the Prometheus deployment. If the counter equals zero, or the metric is not present, then the application is inaccessible to the Prometheus deployment.

<a href="#heading--0003"><h4 id="heading--0003">Source Component</h4></a>

Prometheus

<a href="#heading--0004"><h4 id="heading--0004">Intended use</h4></a>

This metric signals whether a unit is unavailable. By specifying the label juju_unit this metric tells you whether the unit is available to the Prometheus component or not. Example: ```up{juju_unit="openfga-k8s/0"}```

<a href="#heading--0005"><h4 id="heading--0005">Observed by</h4></a>
- **Alert Rules**: Rules in group OpenFGAUnavailable
- **Dashboard**: OpenFGA Unit Availability

<a href="#heading--0006"><h3 id="heading--0006">level</h3></a>

<a href="#heading--0007"><h4 id="heading--0007">Description</h4></a>

All OpenFGA logs have a level, to indicate the seriousness of an event. OpenFGA logs (and json formatted logs in general) can be filtered by log levels. 

<a href="#heading--0008"><h4 id="heading--0008">Source Component</h4></a>

Loki

<a href="#heading--0009"><h4 id="heading--0009">Usage</h4></a>

Use the LogQL’s abilities to enumerate log entries that match a regex template, and to parse json logs and populate fields such as level. Example: ```{juju_charm="openfga"} | json | level =~ `error` ```

<a href="#heading--0010"><h4 id="heading--0010">Observed by</h4></a>

- **Alert Rules**: Rules in group OpenFGAHighSeverityLog
- **Dashboard Visualisation**: OpenFGA High Severity Log Entries



<a href="#heading--0011"><h2 id="heading--0011">Alert rules</h2></a>

<a href="#heading--0012"><h3 id="heading--0012">OpenFGAHighSeverityLog</h3></a>
<a href="#heading--0013"><h4 id="heading--0013">Description</h4></a>

Alerts in this alert group are fired based on how many log entries with the log level of error, critical, or fatal have been created in the last five minutes.

<a href="#heading--0014"><h4 id="heading--0014">Data Source</h4></a>

Loki


<a href="#heading--0015"><h3 id="heading--0015">OpenFGAUnavailable-multiple</h3></a>

<a href="#heading--0016"><h4 id="heading--0016">Description</h4></a>
More than one unit in a multi-unit deployment is inactive.

<a href="#heading--0017"><h4 id="heading--0017">Observed failure</h4></a>

Multiple operator instances have encountered an issue from which they can not recover within a minute. Without other alerts suggesting otherwise, the alert also suggests that there is at least one healthy unit in the deployment.

<a href="#heading--0018"><h4 id="heading--0018">Severity</h4></a>

Error, because while the service is still available, there is now potential for a critical scenario.

<a href="#heading--0019"><h3 id="heading--0019">OpenFGAUnavailable-all</h3></a>

<a href="#heading--0020"><h4 id="heading--0020">Description</h4></a>

No unit in the deployment is active.

<a href="#heading--0021"><h4 id="heading--0021">Observed failure</h4></a>

None of the units in the deployment are active. The service is inaccessible.

<a href="#heading--0022"><h4 id="heading--0022">Severity</h4></a>

Fatal. The service has failed, and can not recover without human intervention.

<a href="#heading--0023"><h2 id="heading--0023">Dashboards</h2></a>

<a href="#heading--0024"><h3 id="heading--0024">OpenFGA High Severity Log Entries</h3></a>

<a href="#heading--0025"><h4 id="heading--0025">Description</h4></a>

Visualization for the number of log entries with levels error or above within 5 minutes spans.

<a href="#heading--0026"><h4 id="heading--0026">Associated Alerts</h4></a>

Alert rules in alert group **OpenFGAHighSeverityLog**.

<a href="#heading--0027"><h3 id="heading--0027">OpenFGA Unit Availability</h3></a>

<a href="#heading--0028"><h4 id="heading--0028">Description</h4></a>

Visualization displaying the availability of OpenFGA units. 

<a href="#heading--0029"><h4 id="heading--0029">Associated Alerts</h4></a>
Alert rules in alert group **OpenFGAUnavailable**.


