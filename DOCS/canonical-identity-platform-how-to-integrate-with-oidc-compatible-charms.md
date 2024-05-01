The Identity Platform provides seamless integration with your OIDC compatible charms using the power of juju relations. We are going to assume that:
1. You have deployed the [identity platform bundle](/t/11916).
2. You have deployed an OIDC compatible charmed application.

To connect an OIDC compatible charmed application with the `identity-platform` bundle, integrate it with `hydra`:

```
juju integrate hydra <OIDC compatible charmed application>
```

Use ```juju status``` to inspect the progress of the integration. After the applications have settled down, you should be able to log in to your application using the Identity Platform.

> See more: [Charmhub | Hydra > Integrations > `oauth`](https://charmhub.io/hydra/integrations)
