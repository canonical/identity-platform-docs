The Login Flow begins when a user is trying to access an application (which we'll interchangeably refer to as an OAuth client). The application initially executes its own logic for checking whether the user is already logged in (has a valid session cookie). If no valid session is found, the application presents the user with an authentication page, where the Sign In with Canonical Identity button is present.

Clicking that button starts the (simplified) login flow described below:. 

![Alt text](url "description")

[details=Diagram]

![Alt text](url "description")

[/details]

The flow begins with a call to Hydra’s public API: the OAuth client sends an authorization request, which is validated by Hydra. If the application client id and secret were found valid, Hydra will initially chack if there are valid sessions.

If none are present, Hydra creates a CSRF challenge and redirects the user to Identity Platform Login UI. The Login UI handles the login challenge and initiates a self-service login flow in Charmed Kratos. The components exchange flow details and show the user a list of configured identity providers to complete the authentication challenge (e.g. Azure AD, Google, GitHub, …).

When the user chooses an identity provider, Kratos creates a continuity parameter and redirects the browser to the external system with 422 status in order to complete the login.

If the authentication with the external identity provider was successful, Kratos issues a session cookie along with a login verifier parameter, which is sent over to Hydra.

Hydra accepts the login request if the parameters match. The consent is implicit, meaning that the OAuth server skips the consent screen as the client is trusted. It then transmits the session cookie and authorization code to the OAuth client.

Finally, the OAuth client exchanges the authorization code for an access token, an id token, and possibly a refresh token, depending on the client’s scope. The browser gets forwarded to the OAuth client’s redirect URL, which calls `/userinfo` endpoint to retrieve the current session’s user details, finally allowing the user to access the requested resource.

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