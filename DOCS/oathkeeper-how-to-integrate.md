# Integrate your Charmed Operator with Identity and Access Proxy

Applications that do not conform to OAuth/OIDC standards or don't offer built-in access control can be secured using the Identity and Access Proxy (IAP) solution, which offers a possibility to protect endpoints by intercepting incoming requests and delegating the authn/authz process to the relevant components of the [Identity Platform](https://charmhub.io/identity-platform).

Oathkeeper is the main entrypoint to plug the Identity and Access Proxy to your charmed operator. It can be achieved using the power of juju relations.

This guide will explain how to extend the Identity Platform with the Identity and Access Proxy and integrate the solution with your charm, allowing you to restrict access to your application to authenticated users only.

We are going to assume that:
1. Your charmed application doesn't support the OAuth 2.0/OIDC protocols, otherwise refer to [this](https://charmhub.io/topics/canonical-identity-platform/how-to/integrate-oidc-compatible-charms) guide instead.
2. Your charmed application supports integration with Charmed Traefik via `ingress-per-app` or `ingress-per-unit` interface and provides Charmed Oathkeeper with necessary data by supporting the `auth_proxy` [interface](https://discourse.charmhub.io/t/13973).
3. You have deployed the [Identity Platform bundle](https://charmhub.io/topics/canonical-identity-platform/tutorials/e2e-tutorial).
4. You have deployed your charmed application on Kubernetes.

This deployment should be your starting point:
```
$ juju status
Model  Controller          Cloud/Region        Version  SLA          Timestamp
iam    microk8s-localhost  microk8s/localhost  3.1.5    unsupported  14:21:47+03:00

App                                  Version  Status   Scale  Charm                                Channel      Rev  Address         Exposed  Message
hydra                                v2.1.1   active       1  hydra                                latest/edge  267  10.152.183.98   no
identity-platform-login-ui-operator           active       1  identity-platform-login-ui-operator  latest/edge   74  10.152.183.56   no
kratos                               v1.0.0   active       1  kratos                               latest/edge  383  10.152.183.207  no
kratos-external-idp-integrator                active      1  kratos-external-idp-integrator       latest/edge  182  10.152.183.18   no
postgresql-k8s                       14.7     active       1  postgresql-k8s                       14/stable     73  10.152.183.46   no       Primary
self-signed-certificates                      active       1  self-signed-certificates             edge          30  10.152.183.189  no
traefik-admin                        2.10.4   active       1  traefik-k8s                          latest/edge  149  10.64.140.45    no
traefik-public                       2.10.4   active       1  traefik-k8s                          latest/edge  149  10.64.140.44    no

Unit                                    Workload  Agent  Address      Ports  Message
hydra/0*                                active    idle   10.1.184.6
identity-platform-login-ui-operator/0*  active    idle   10.1.184.38
kratos-external-idp-integrator/0*       active    idle   10.1.184.63
kratos/0*                               active    idle   10.1.184.44
postgresql-k8s/0*                       active    idle   10.1.184.28         Primary
self-signed-certificates/0*             active    idle   10.1.184.22
traefik-admin/0*                        active    idle   10.1.184.45
traefik-public/0*                       active    idle   10.1.184.5
```

In order to set up the proxy, you first need to enable the ForwardAuth feature in Charmed Traefik and integrate its instance with your charm:
```commandline
juju config traefik-public enable_experimental_forward_auth=True
juju integrate your-charm traefik-public
```

The next step is to deploy Charmed Oathkeeper and integrate it with Charmed Traefik:
```commandline
juju deploy oathkeeper --channel edge --trust
juju integrate oathkeeper traefik-public:experimental-forward-auth
```

You can follow the deployment status with `watch -c juju status --color`.

Then, integrate your charm with the proxy by running:
```commandline
juju integrate oathkeeper your-charm:auth-proxy
```

As a result of the integration, Charmed Oathkeeper will create a set of access rules that define restrictions on your charmed application access. Charmed Traefik will enforce applying those rules with the ForwardAuth middleware.

Finally, integrate the proxy with Identity Platform with the use of Kratos charmed operator:
```commandline
juju integrate oathkeeper kratos
juju config kratos dev=True
```

When you access your application, Charmed Traefik will ask Oathkeeper whether access to the endpoint is protected. If so, it will check if there is a valid session. In case it doesn't find one, it will redirect to the Identity Platform login page. Upon successful authentication, you will be redirected back to the original url.

> See more: [Charmhub | Oathkeeper > Integrations](https://charmhub.io/oathkeeper/integrations)
