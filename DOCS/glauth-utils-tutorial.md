# Charmed GLAuth Utility K8s Tutorial

This tutorial aims to provide a general walkthrough to set up a fully working
GLAuth utility using `glauth-utils` charmed operator, MicroK8s, and Juju.

## Set up the environment

Follow
this [guide](https://juju.is/docs/juju/set-up--tear-down-your-test-environment)
to bootstrap a MicroK8s cloud running a Juju controller.

Create a Juju model:

```shell
juju add-model dev
```

## Deploy prerequisite charmed operators

The `glauth-utils` charmed operator requires the following charmed operators
deployed in the MicroK8s cluster:

- [`glauth-k8s-operator`](https://charmhub.io/glauth-k8s)

```shell
juju deploy glauth-k8s --channel edge --trust
```

## Deploy `glauth-utils` charmed operator

The `glauth-utils` charmed operator can be deployed as follows:

```shell
juju deploy glauth-utils --channel edge --trust
```

## Integrate with other charmed operators

The `glauth-utils` charmed operator offers the `glauth-auxiliary` interface in
order to supplement the `glauth-k8s` charmed operator:

```shell
juju integrate glauth-utils:glauth-auxiliary glauth-k8s:glauth-auxiliary
```

## Tear down the environment

Remove the `dev` Juju model:

```shell
juju destroy-model dev
```
