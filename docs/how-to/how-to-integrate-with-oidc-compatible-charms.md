# How To Integrate With OIDC Compatible Charms

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

