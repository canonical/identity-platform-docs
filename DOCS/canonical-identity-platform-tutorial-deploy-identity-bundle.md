# Introduction

The Canonical Identity Platform is a composable identity broker and identity provider based on open source products from [Ory](https://www.ory.sh/open-source/), [Postgres](https://www.postgresql.org/) and [Traefik Labs](https://traefik.io/).

The core components of the Canonical Identity Platform are grouped in a [Juju Bundle](https://juju.is/docs/juju/bundle). In this tutorial you will:

1. Deploy the Canonical Identity platform bundle
2. Register a client application in Azure AD
3. Configure Azure AD as an external identity provider
4. Deploy Charmed Grafana and add single sign on

# Requirements

This tutorial assumes you have 

- Familiarity with the core Juju concepts and how to [manage charms](https://juju.is/docs/juju)
- A Juju controller(v3.1+) bootstrapped on a MicroK8s cluster that is ready to use. A typical setup using [snaps](https://snapcraft.io/) can be found in the [Juju documentation](https://juju.is/docs/sdk/dev-setup) (see the **Microk8s** section).
An Azure AD tenant and a user with sufficient permissions to provision a client application.

# Set up the environment

For the Identity Platform bundle deployment to go smoothly, make sure the following MicroK8s [addons](https://microk8s.io/docs/addons) are enabled: ```dns```, ```hostpath-storage``` and ```metallb```.
You can check this with ```microk8s status```, and if any are missing, enable them with:

```
microk8s enable dns hostpath-storage
```

The bundle comes with Charmed Traefik to provide ingress, for which the ```metallb``` addon must be enabled:

```
microk8s enable metallb:10.64.140.43-10.64.140.49
```

The following commands can be used to monitor the deployment rollout status:

```
microk8s kubectl rollout status deployments/hostpath-provisioner -n kube-system -w
microk8s kubectl rollout status deployments/coredns -n kube-system -w
microk8s kubectl rollout status daemonset.apps/speaker -n metallb-system -w
```

# Deploy the Identity Platform bundle
Create a dedicated model for the Identity Platform bundle. To do that, run: 

```
juju add-model iam
```

To deploy the Identity Platform bundle, run:

```
juju deploy identity-platform --trust --channel beta
```

The Juju controller will now fetch the Identity Platform bundle from Charmhub and begin deploying it on the Microk8s cloud. 
This process will take several minutes depending on your hardware and network speed. It will install the following charmed applications:
- [Charmed Postgresql](https://charmhub.io/postgresql) - the SQL database of choice
- [Charmed Ory Hydra](https://charmhub.io/hydra) - the solution Oauth/OIDC server
- [Charmed Ory Kratos](https://charmhub.io/kratos) - the user management and authentication component
- [Charmed Traefik](https://charmhub.io/traefik-k8s) - which will be used for ingress
- [Login UI operator](https://github.com/canonical/identity-platform-login-ui-operator) - a middleware which routes calls between the different services and serves the login/error pages

The bundle will also deploy a the following helper charms:
- [Kratos External IdP Integrator](https://charmhub.io/kratos-external-idp-integrator) - an integrator charm that will be used later in this tutorial to configure an external identity provider 
- [Self Signed Certificates](https://charmhub.io/self-signed-certificates), for managing the TLS certificates that our ingress will use

This process can take several minutes depending on your network speed and resource availability. You can track the progress by running:

```
juju status --watch 1s
```

This command displays the status of the installation and information about the model, like IP addresses, ports, versions etc. 

When  ```juju status``` displays the following output it means that the bundle is ready:

```
Model  Controller      	Cloud/Region    	Version  SLA      	Timestamp
iam	microk8s-localhost  microk8s/localhost  3.2.0	unsupported  13:43:18+03:00

App                              	Version  Status   Scale  Charm                            	Channel	Rev  Address     	Exposed  Message
hydra                                     	active   	1  hydra                            	edge   	232  10.152.183.33   no  	 
identity-platform-login-ui-operator       	active   	1  identity-platform-login-ui-operator  edge    	30  10.152.183.65   no  	 
kratos                                    	active   	1  kratos                           	edge   	340  10.152.183.188  no  	 
kratos-external-idp-integrator            	waiting  	1  kratos-external-idp-integrator   	edge   	166  10.152.183.69   no   	installing agent
postgresql-k8s                   	14.7 	active   	1  postgresql-k8s                   	14/stable   73  10.152.183.201  no  	 
self-signed-certificates                  	active       	1  self-signed-certificates         	edge     22  10.152.183.111  no   	installing agent
traefik-admin                    	2.9.6	active   	1  traefik-k8s                      	edge   	139  10.64.140.44	no  	 
traefik-public                   	2.9.6	active   	1  traefik-k8s                      	edge   	139  10.64.140.45	no  	 

Unit                                	Workload  Agent  Address  	Ports  Message
hydra/0*                            	active	idle   10.1.184.54    	 
identity-platform-login-ui-operator/0*  	active	idle   10.1.184.60    	 
kratos-external-idp-integrator/0*   	blocked	idle   10.1.184.3      	       Invalid configuration: Missing required configuration 'issuer_url' for provider 'generic'
kratos/0*                           	active	idle   10.1.184.21    	 
postgresql-k8s/0*                   	active	idle   10.1.184.59    	 
self-signed-certificates/0*         	active	idle   10.1.184.4
traefik-admin/0*                    	active	idle   10.1.184.6     	 
traefik-public/0*                   	active	idle   10.1.184.10    	  	 
```

The *kratos-external-idp-integrator* is in a blocked state. This is expected as they require configuration in order to be operational.

# Register a client application in Azure AD 

Create a confidential client in Azure AD by following the instructions found in the [Microsoft documentation](https://learn.microsoft.com/en-us/azure/healthcare-apis/register-application#register-a-new-application). The redirect uri will be \<kratos-base-url\>/microsoft. To get the kratos base URL run:

```
juju run traefik-public/0 show-proxied-endpoints  | yq '.proxied-endpoints' | jq '.kratos.url'
```

At the end of the process you will get a *client_id*.

Once the client is registered, you have to create a secret by following the instructions found in the [Microsoft documentation](https://learn.microsoft.com/en-us/azure/healthcare-apis/register-application#certificates--secrets). Make sure to save the *client_secret*. And keep it confidential.

You then need to find and copy the *tenant_id* by following [these](https://learn.microsoft.com/en-us/azure/active-directory/fundamentals/how-to-find-tenant) instructions.

# Add Azure AD as an external identity provider

You are now ready to use the Kratos external IDP integrator charm to configure Azure AD as an external identity provider. To do this, run:

```
juju config kratos-external-idp-integrator \
  provider=microsoft \
  provider_id=microsoft \
  client_id=<client_id> \
  client_secret=<client_secret> \
  microsoft_tenant_id=<tenant_id>
```

After a while the *kratos-external-idp-integrator* status will change to active, this means that Azure AD has been added as a Kratos sign in provider.

# Add SSO to Charmed Grafana 

To deploy [Charmed Grafana](https://charmhub.io/grafana-k8s), run:

```
juju deploy grafana-k8s
```

This command deploys Charmed Grafana in the same model as the Identity Platform Bundle.

The newly deployed Grafana requires ingress, and it can get that from the existing Traefik instance that was deployed together with the bundle. 

You can integrate Charmed Grafana with Traefik by running:

```
juju integrate grafana-k8s:ingress traefik-public
```

And then you can integrate Grafana with Hydra, by running:

```
juju integrate grafana-k8s:oauth hydra
```

This command registers Grafana as an OIDC client in Hydra and configures Grafana to use the Canonical Identity Platform as an authentication provider.

Once all applications are ready, you can access the Grafana dashboard on the URL http://\<traefik_public_ip\>/\<juju_model_name\>-\<application-name\>. You can get the *traefik_public_ip* by running the following command:

```
juju status --format json | yq '.applications.traefik-public.address'
```

Upon navigating to the URL you will be presented with the following login screen:

![Alt]( https://raw.githubusercontent.com/canonical/canonical-identity-platform-docs/main/Diagram_sources/deploy_iam_bundle_1.png "Grafana Login UI")

Click on *Sign in with external identity provider* and, after you trust the self-signed TLS cert, you will be redirected to the login page where you can select to authenticate with Azure AD:

![Alt]( https://raw.githubusercontent.com/canonical/canonical-identity-platform-docs/main/Diagram_sources/deploy_iam_bundle_2.png "IAM Login UI")

Choose Microsoft and log in. After a successful login, you will be redirected back to grafana.
