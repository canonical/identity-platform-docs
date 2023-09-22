The below diagram describes the high level architecture of the Canonical Identity Platform and its dependencies:

![Alt text]( https://raw.githubusercontent.com/canonical/canonical-identity-platform-docs/main/Diagram_sources/arch-diagram.png "Canonical Identity Platform Architecture")

The Canonical Identity Platform is an identity broker: it connects identity providers (Microsoft Azure Active Directory, Okta, Google, GitHub, ...) with multiple service providers (Grafana, Kafka, and/or other charmed workloads).

The charmed operators that make up Canonical Identity Platform are available as an [identity-platform](https://charmhub.io/identity-platform) bundle.

It consists of several components:
- [Charmed Hydra](https://github.com/canonical/hydra-operator) - an OAuth 2.0 and OpenID Connect server
- [Charmed Kratos](https://github.com/canonical/kratos-operator) - an identity and user management system
- [Charmed Kratos External IDP Integrator](https://github.com/canonical/kratos-external-idp-integrator) - a helper for integrating Charmed Kratos with external identity providers
- [Charmed Identity Platform Login UI](https://github.com/canonical/identity-platform-login-ui-operator) - a user interface
- [Charmed PostgreSQL](https://github.com/canonical/postgresql-k8s-operator) - a database provider for Kratos and Hydra
- [Charmed Traefik](https://github.com/canonical/traefik-k8s-operator) - two instances of ingress operator for public and admin APIs.

The Canonical Identity Platform benefits from charm relation interfaces and juju config to simplify the experience of propagating SSO configuration across multiple applications. There are 2 main integration points:

- `oauth` relation interface, which allows to integrate OIDC-compatible charms with the OAuth Server. When used, Charmed Ory Hydra registers an OAuth client for your charmed application and manages it throughout its lifecycle. You can also integrate non-charmed, but OIDC-compatible workloads with Charmed Hydra’s [actions](https://charmhub.io/hydra/actions).

- Charmed Kratos External IDP Integrator, which updates the configuration of the identity server (Charmed Kratos) with the external identity provider setup that is defined via juju config. You can define multiple identity providers by deploying more Integrator charm instances.

Interested in learning how to integrate your application with the Canonical Identity Platform? Check our [how-to guides](TODO-how-to-page).

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