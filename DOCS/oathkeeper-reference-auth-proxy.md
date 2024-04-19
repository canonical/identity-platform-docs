# Oathkeeper `auth_proxy` interface reference
In this reference we will provide a technical description of the parameters passed by charmed applications to [Charmed Oathkeeper](https://discourse.charmhub.io/t/charmed-ory-oathkeeper-documentation-index/13972) as part of `auth_proxy` integration.

> See more: [Charmhub | Oathkeeper > Integrations > `auth_proxy`](https://charmhub.io/oathkeeper/integrations)

The parameters passed to Oathkeeper by the charms aiming to integrate with the Identity and Access Proxy are an important part of the integration as they will be translated into access rules and define restrictions on your application access.

## `protected_urls`
### Required: yes
### Description
A list of urls that your application is reachable at. It is recommended to set up tls, for example with [tls-certificates](https://github.com/canonical/charm-relation-interfaces/blob/main/interfaces/tls_certificates/v0/README.md) interface and [self-signed-certificates](https://charmhub.io/self-signed-certificates) operator.
This parameter should be updated whenever the Traefik ingress relation changes.
### Examples
```
["https://my-domain.com"]
["https://my-domain.com/private"]
["https://10.64.140.43/test-app/unit-0", "https://10.64.140.43/test-app/unit-1"]
```

## `allowed_endpoints`
### Required: no
### Description
A list of endpoints you want to allow access to without the need of going through the authentication process. All other endpoints except for the ones provided in that parameter will require authentication.
### Examples
```
[“health”, “about/app”]
```

Given `protected_urls=["https://my-domain.com"]`, all application endpoints except for `https://my-domain.com/health` and `https://my-domain.com/about/app` will require authentication.

## `headers`
### Required: no
### Description
A list of response headers that your charmed application expects to receive from the proxy once authenticated. The headers can be custom as oathkeeper supports mutators - it's able to transform credentials into headers that your backend understands, i.e. `X-User`.
Check the currently supported headers [here](https://github.com/canonical/oathkeeper-operator/blob/7682baaf6f1a6b257fe9cfa78a90a96e21556b41/lib/charms/oathkeeper/v0/auth_proxy.py#L88).
### Examples
```commandline
["X-User", “X-Email"]
```
