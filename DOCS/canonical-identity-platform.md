# Canonical Identity Platform

Composable identity provider and identity broker system based on [Juju](http://juju.is).

The Canonical Identity Platform is the simplest way to add single sign on (SSO) for charmed workloads and centralized authentication, authorisation and access governance controls.

The Canonical Identity Platform uses best of breed open source software to provide:
- The ability to configure SSO with third party, OIDC compliant identity providers (e.g. Azure AD, Google, Okta, etc.)
- A standard compliant compliant OAuth/OIDC server 
- User and client management functionalities
- A relationship based access control (ReBAC) backend
- A login UI and error pages

While primarily designed for charmed workloads the Canonical Identity Platform can also be used to protect traditional Kubernetes and Virtual Machine based applications.

## In this documentation

| | |
|-|-|
| [Tutorial](/tutorial-url)</br>  Get started - a hands-on introduction for new users deploying the Identity Platform.</br> | [How-to guides](/guide-url) </br> Step-by-step guides covering key operations and common tasks |
| [Explanation](/explanation-url) </br> Concepts - discussion and clarification of key topics                   |  [Reference](/reference-url) </br> Technical information - specifications, APIs, architecture    |

## Project and community

The Canonical Identity Platform is a member of the Ubuntu family. It’s an open source project that warmly welcomes community projects, contributions, suggestions, fixes and constructive feedback.

- [Code of conduct](https://ubuntu.com/community/code-of-conduct)
- [Join the Discourse community forum](https://discourse.charmhub.io/tag/identity)
- [Join the Mattermost community chat](https://chat.charmhub.io/charmhub/channels/iam-platform)
- [Contribute on GitHub](https://github.com/canonical/iam-bundle)
- View our roadmap

Thinking about using the Canonical Identity Platform for your next project? [Get in touch with the team!](https://chat.charmhub.io/charmhub/channels/iam-platform)

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