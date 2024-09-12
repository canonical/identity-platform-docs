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

Interested in learning how to integrate your application with the Canonical Identity Platform? Check our [how-to guides](/t/how-to-guides/11911).
