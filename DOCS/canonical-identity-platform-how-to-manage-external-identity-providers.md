The Identity Platform bundle is an Identity broker, this means that it relies on external identity providers to authenticate users and manage user attributes. This documentation explains how to integrate with external providers. 

## Integrate with External Provider

The component of the Identity Platform responsible for integrating with Identity Providers is [Kratos](http://charmhub.io/kratos). There 2 actions needed to integrate with an Identity Provider:
1. Register a client in the Identity Provider
2. Provide the client credentials to Kratos

### Register the client

In this section we are going to register an oAuth2 client that Kratos can use to authenticate users. If you already have registered a client you can just skip to the next section.

Each external Identity Provider has a different flow for registering a client. A list with instructions for some of the most common Providers can be seen below, if you can’t find your Provider below please refer to their documentation. 

You will need to provide the client’s *redirect_uri* to the provider, which is the URL to which the user will be redirected to after they log in. You don’t need to provide it on registration time though.

You can either calculate the URI yourself or get it after you provide the client credentials to Kratos as we will see in the next section.

The *redirect_uri* will be:

```https://<kratos-public-url>/<provider-id>```

To get the kratos-public-url you can run: 

```juju run traefik-public/0 show-proxied-endpoints  | yq '.proxied-endpoints' | jq '.kratos.url'```

The *provider-id* can be anything you want, you will provide to Kratos in the next step. Every provider that is registered with Kratos needs to have a different *provider-id*, if you don’t provide a *provider-id*, one will be auto-generated.

After registering the provider you need to have the following information: *client_id*, *client_secret*.

#### Azure AD 

To create a confidential client in Azure AD follow the instructions found in the [Microsoft documentation](https://learn.microsoft.com/en-us/azure/healthcare-apis/register-application#register-a-new-application).

Once the client is registered, you have to create a secret by following the instructions found in the [Microsoft documentation](https://learn.microsoft.com/en-us/azure/healthcare-apis/register-application#certificates--secrets). Make sure to save the *client_secret*. And keep it confidential.

You then need to find and copy the *tenant_id* by following these [instructions](https://learn.microsoft.com/en-us/azure/active-directory/fundamentals/how-to-find-tenant).

#### Google

To create a confidential client in Google follow the instructions found in the [Google documentation](https://developers.google.com/identity/protocols/oauth2#1.-obtain-oauth-2.0-credentials-from-the-dynamic_data.setvar.console_name-.).

### Provide the Client Credentials to Kratos

Now that we have registered a client we need to provide the client credentials to Kratos. For this we are going to use an integrator charm, the purpose of this charm is to provide configuration to Kratos.

First we need to deploy the charm and integrate it with kratos by running:

```
juju deploy kratos-external-idp-integrator
juju integrate kratos kratos-external-idp-integrator
```

Then we need to configure the integrator charm. Depending on the provider that we use, a different set of configurations is needed. A list of instructions for some of the most common providers can be seen below. Please refer to the [integrator charm](https://charmhub.io/kratos-external-idp-integrator) and the [Kratos documentation](https://www.ory.sh/docs/kratos/social-signin/overview) for further details.

Once you have configured the provider you will be able to choose to login in with that provider in the platform’s login page.

#### Azure AD

If your provider is Azure AD the following configuration is needed:

```
juju config kratos-external-idp-integrator \
  provider=microsoft \
  client_id=<client_id> \
  client_secret=<client_secret> \
  microsoft_tenant_id=<tenant_id>
```

#### Google

If your provider is Google the following configuration is needed:

```
juju config kratos-external-idp-integrator \
  provider=google \
  client_id=<client_id> \
  client_secret=<client_secret>
```

### Choose Provider ID

You can now also choose a *provider-id*, if you wish to, by running:

```
juju config kratos-external-idp-integrator provider_id=<provider-id> 
```

### Get the redirect_uri

You can run ```juju status``` to inspect the status of the charm. Once the charm becomes active, you can get the *redirect_uri* of the client by running:

```
juju run kratos-external-idp-integrator/0 get-redirect-uri
```

## Remove External Provider

To remove an external provider from Kratos all you need to is remove the relation to the integrator by running:

```
juju remove-integration kratos kratos-external-idp-integrator
```

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