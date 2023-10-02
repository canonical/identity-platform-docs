The Canonical Identity Platform is a composable identity broker based on open source products from [Ory](https://www.ory.sh/open-source/), [Postgres](https://www.postgresql.org/) and [Traefik Labs](https://traefik.io/).

> See more: [Charmhub | Identity Plaform](https://charmhub.io/identity-platform)

The core components of the Canonical Identity Platform are grouped in a Juju Bundle. In this tutorial you will deploy the Identity Platform juju Bundle and use it to provide SSO to an OIDC compatible Charmed application.

# Requirements

This tutorial assumes you have
- A Juju controller (v3.1+) bootstrapped on a MicroK8s cluster that is ready to use. See, e.g., Charm SDK | Tutorial > Set up Juju.
- An Azure AD tenant and a user with sufficient permissions to provision a client application.
- A registered client in Azure AD, you need to know the client_id, client_secret and tenant ID. See [Microsoft | Register a new application](https://learn.microsoft.com/en-us/azure/healthcare-apis/register-application#register-a-new-application), [Microsoft | Register a new application > Certificates & Secrets](https://learn.microsoft.com/en-us/azure/healthcare-apis/register-application#certificates--secrets) and [Microsoft | How to find your Microsoft Entra tenant ID](https://learn.microsoft.com/en-us/azure/active-directory/fundamentals/how-to-find-tenant) for further instructions.

# Deploy the Identity Platform bundle

For the Identity Platform bundle deployment to go smoothly, make sure the metallb MicroK8s addon is enabled.

```
microk8s enable metallb:10.64.140.43-10.64.140.49
```

Create a dedicated model for the Identity Platform bundle. To do that, run:

```
juju add-model iam
```

To deploy the Identity Platform bundle, run:

```
juju deploy identity-platform --trust --channel beta
```

The Juju controller will now fetch the Identity Platform bundle from Charmhub and begin deploying it on the MicroK8s cloud.
This process will take several minutes, depending on your hardware and network speed. It will install the following charmed applications:
- [Charmed Postgresql](https://charmhub.io/postgresql) - the SQL database of choice
- [Charmed Ory Hydra](https://charmhub.io/hydra) - the solution Oauth/OIDC server
- [Charmed Ory Kratos](https://charmhub.io/kratos) - the user management and authentication component
- [Charmed Traefik](https://charmhub.io/traefik-k8s) - which will be used for ingress
- [Login UI operator](https://github.com/canonical/identity-platform-login-ui-operator) - a middleware which routes calls between the different services and serves the login/error pages

The bundle will also deploy a the following helper charms:
- [Kratos External IdP Integrator](https://charmhub.io/kratos-external-idp-integrator) - an integrator charm that will be used later in this tutorial to configure an external identity provider
- [Self Signed Certificates](https://charmhub.io/self-signed-certificates), for managing the TLS certificates that our ingress will use

You can track the progress by running:

```
juju status --watch 1s
```

This command displays the status of the installation and information about the model, like IP addresses, ports, versions etc.

When ```juju status``` displays the following output it means that the bundle is ready:

```
Model  Controller          Cloud/Region        Version  SLA          Timestamp
iam    microk8s-localhost  microk8s/localhost  3.1.5    unsupported  14:21:47+03:00

App                                  Version  Status   Scale  Charm                                Channel      Rev  Address         Exposed  Message
hydra                                v2.1.1   active       1  hydra                                latest/edge  267  10.152.183.98   no
identity-platform-login-ui-operator           active       1  identity-platform-login-ui-operator  latest/edge   74  10.152.183.56   no
kratos                               v1.0.0   active       1  kratos                               latest/edge  383  10.152.183.207  no
kratos-external-idp-integrator                waiting      1  kratos-external-idp-integrator       latest/edge  182  10.152.183.18   no       installing agent
postgresql-k8s                       14.7     active       1  postgresql-k8s                       14/stable     73  10.152.183.46   no       Primary
self-signed-certificates                      active       1  self-signed-certificates             edge          30  10.152.183.189  no
traefik-admin                        2.10.4   active       1  traefik-k8s                          latest/edge  149  10.64.140.45    no
traefik-public                       2.10.4   active       1  traefik-k8s                          latest/edge  149  10.64.140.44    no

Unit                                    Workload  Agent  Address      Ports  Message
hydra/0*                                active    idle   10.1.184.6
identity-platform-login-ui-operator/0*  active    idle   10.1.184.38
kratos-external-idp-integrator/0*       blocked   idle   10.1.184.63         Invalid configuration: Missing required configuration 'issuer_url' for provider 'generic'
kratos/0*                               active    idle   10.1.184.44
postgresql-k8s/0*                       active    idle   10.1.184.28         Primary
self-signed-certificates/0*             active    idle   10.1.184.22
traefik-admin/0*                        active    idle   10.1.184.45
traefik-public/0*                       active    idle   10.1.184.5
```

The *kratos-external-idp-integrator* is in a blocked state. In the next step we will configure it with an identity provider so our Identity Platform becomes fully operational.

# Connect the Canonical Identity Platform with an external Identity Provider

In this tutorial we are going to connect the Identity Platform with Azure AD. Make sure that you have registered a client on Azure AD and you know the client_id, client_secret and tenant_id.

First, we need to inform Azure AD of our deployment’s redirect_uri. Get the kratos base URL

```
juju run traefik-public/0 show-proxied-endpoints | yq '.proxied-endpoints' | jq '.kratos.url'
```

The redirect_uri should be: *<kratos-base-url>/self-service/methods/oidc/callback/microsoft*. Use this to configure your client on Azure AD.

> See more: [Microsoft | Redirect URI](https://learn.microsoft.com/en-us/azure/active-directory/develop/reply-url)

Now use the Azure client credentials to configure the Kratos external IDP integrator charm:


```
juju config kratos-external-idp-integrator \
  provider=microsoft \
  provider_id=microsoft \
  client_id=<client_id> \
  client_secret=<client_secret> \
  microsoft_tenant_id=<tenant_id>
```

> See more: [Charmhub | Kratos External Idp Integrator](https://charmhub.io/kratos-external-idp-integrator)

After a while the kratos-external-idp-integrator status will change to active, this means that Azure AD has been added as a Kratos sign in provider. Congratulations, your deployment now uses Azure AD as your external identity provider.

# Use Identity Platform to provide SSO

Now that our Identity Broker is ready we can use it to provide SSO to an application, for this purpose we are going to use Grafana. To deploy [Charmed Grafana](https://charmhub.io/grafana-k8s), run:

```
juju deploy grafana-k8s
```

This command deploys Charmed Grafana in the same model as the Identity Platform bundle.

The newly deployed Grafana requires ingress in order to properly integrate with the Identity Platform. We can use the existing Traefik instance, that was deployed together with the bundle, to get that.
You can integrate Charmed Grafana with Traefik by running:

```
juju integrate grafana-k8s:ingress traefik-public
```

Now, you can connect Grafana with the bundle. To do this we need to integrate Grafana with the bundle’s OIDC server, Hydra:

```
juju integrate grafana-k8s:oauth hydra
```

This command registers Grafana as an OIDC client in Hydra and configures Grafana to use the Canonical Identity Platform as an authentication provider. Once all applications are ready we can try to login in to Grafana through Azure AD.

# Validate the SSO integration

You can access the Grafana dashboard on the URL *http://<traefik_public_ip>/iam-grafana*. You can get the traefik_public_ip by running the following command:

```
juju status --format json | yq '.applications.traefik-public.address'
```

Upon navigating to the URL you will be presented with the following login screen:

![Alt]( https://raw.githubusercontent.com/canonical/canonical-identity-platform-docs/main/Diagram_sources/deploy_iam_bundle_1.png "Grafana Login UI")

Click on *Sign in with external identity provider* and, after you trust the self-signed TLS cert, you will be redirected to the login page where you can select to authenticate with Azure AD:

![Alt]( https://raw.githubusercontent.com/canonical/canonical-identity-platform-docs/main/Diagram_sources/deploy_iam_bundle_2.png "IAM Login UI")

Choose Microsoft and log in. After a successful login, you will be redirected back to grafana.
