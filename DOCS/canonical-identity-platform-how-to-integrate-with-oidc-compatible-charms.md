The Identity Platform provides seamless integration with your OIDC compatible charms using the power of juju relations. We are going to assume that:
1. You have deployed the [identity platform bundle](link to tutorial).
2. You have deployed an OIDC compatible charmed application.

To integrate you need to run:

```
juju integrate hydra application
```

Use ```juju status``` to inspect the progress of the integration. After the applications have settled down, you should be able to log in to your application using the Identity Platform

A full list of the charms supporting this relation can be found [here](https://charmhub.io/hydra/integrations), under the *oauth* integration.
Further information about this relation can be found [here](https://github.com/canonical/charm-relation-interfaces/tree/main/interfaces/oauth/v0).

# Navigation
[details=Navigation]
|Level|Path|Navlink|
|--|--|--|
| 1 | overview | [Home]() |
| 1 | tutorials | [Tutorial]() |
| 2 | tutorials/e2e-tutorial | [Getting started with the Canonical Identity Platform]() |
| 1 | how-to | [How-to guides]() |
| 2 | how-to/integrate-external-identity-provider | [Integrate with external identity providers]() |
| 2 | how-to/integrate-oidc-compatible-charms | [Integrate with OIDC compatible charms ]() |
| 2 | how-to/integrate-cos | [Integrate with Canonical Observability Stack]() |
| 1 | explanation | [Explanation]() |
| 2 | explanation/what-is-oidc | [What is an OIDC compatible application?]() |
| 1 | reference | [Reference]() |
| 2 | reference/bundles | Bundles |
| 3 | reference/bundles/identity-platform | [Identity Platform](https://charmhub.io/identity-platform) |
| 3 | reference/bundles/architecture | [Architecture]() |
| 3 | reference/bundles/login-flow | [Login flow]() |
| 2 | reference/observability | Observability setup |
| 3 | reference/observability/metrics | [Metrics]() |
| 3 | reference/observability/alert-rules | [Alert rules]() |
| 3 | reference/observability/dashboards | [Dashboards]() |
| 2 | reference/kubernetes-charms | Kubernetes Charms |
| 3 | reference/kubernetes-charms/hydra | [Hydra](https://charmhub.io/hydra) |
| 3 | reference/kubernetes-charms/kratos | [Kratos](https://charmhub.io/kratos) |
| 3 | reference/kubernetes-charms/kratos-external-idp-integrator | [Kratos External IdP Integrator](https://charmhub.io/kratos-external-idp-integrator) |
| 3 | reference/kubernetes-charms/idp-ui | [Identity Platform Login UI](https://charmhub.io/identity-platform-login-ui-operator) |
[/details]