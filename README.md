# Chaos Toolkit Extension for Azure

[![Build](https://github.com/chaostoolkit-incubator/chaostoolkit-azure/actions/workflows/build.yaml/badge.svg)](https://github.com/chaostoolkit-incubator/chaostoolkit-azure/actions/workflows/build.yaml)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-azure.svg)](https://www.python.org/)

This project is a collection of [actions][] and [probes][], gathered as an
extension to the [Chaos Toolkit][chaostoolkit]. It targets the
[Microsoft Azure][azure] platform.

[actions]: http://chaostoolkit.org/reference/api/experiment/#action
[probes]: http://chaostoolkit.org/reference/api/experiment/#probe
[chaostoolkit]: http://chaostoolkit.org
[azure]: https://azure.microsoft.com/en-us/

## Install

This package requires Python 3.8+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

```
$ pip install -U chaostoolkit-azure
```

## Usage

To use the probes and actions from this package, add the following to your
experiment file:

```json
{
  "type": "action",
  "name": "start-service-factory-chaos",
  "provider": {
    "type": "python",
    "module": "chaosazure.vm.actions",
    "func": "stop_machines",
    "secrets": ["azure"],
    "arguments": {
      "parameters": {
        "TimeToRunInSeconds": 45
      }
    }
  }
}
```

That's it!

Please explore the code to see existing probes and actions.

### Credentials

This extension uses the [Azure SDK][sdk] under the hood.

[sdk]: https://github.com/Azure/azure-sdk-for-python

#### Environment Variables

The extensions uses a chained approach to locating the appropriate
credentials, starting from the secrets in the experiment before moving to
[environment variables](envvar) and so on as per the [Azure documentation][creds].

[creds]: https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.defaultazurecredential?view=azure-python
[envvar]: https://learn.microsoft.com/fr-fr/python/api/azure-identity/azure.identity.environmentcredential?view=azure-python

In theory, at the bare minimum you don't need to set anything explicitely 
into the experiment and let the client figure it out based on the local
machine settings.

#### Experiment Secrets

You may also pass them via the secrets block of the experiment:

  ```json
  {
    "secrets": {
      "azure": {
        "client_id": "your-super-secret-client-id",
        "client_secret": "your-even-more-super-secret-client-secret",
        "tenant_id": "your-tenant-id"
      }
    }
  }
  ```

  You can retrieve secretes as well from [environment][env_secrets] or [HashiCorp vault][vault_secrets]. 

  
  If you are not working with Public Global Azure, e.g. China Cloud You can set the cloud environment.

  ```json
  {
    "client_id": "your-super-secret-client-id",
    "client_secret": "your-even-more-super-secret-client-secret",
    "tenant_id": "your-tenant-id",
    "cloud": "AZURE_CHINA_CLOUD"
  }
  ```

  Available cloud names:

  - AZURE_CHINA_CLOUD
  - AZURE_GERMAN_CLOUD
  - AZURE_PUBLIC_CLOUD
  - AZURE_US_GOV_CLOUD

  Either of these values can be passed via `AZURE_CLOUD` as well.

  [vault_secrets]: https://docs.chaostoolkit.org/reference/api/experiment/#vault-secrets
  [env_secrets]: https://docs.chaostoolkit.org/reference/api/experiment/#environment-secrets

### Subscription

Additionally you need to provide the Azure subscription id.

- As an  environment variable
  
  - AZURE_SUBSCRIPTION_ID

- Subscription id in the experiment file

  ```json
  {
    "configuration": {
      "azure_subscription_id": "your-azure-subscription-id"
    }
  }
  ```

  Configuration may be as well retrieved from an [environment][env_configuration].

  An old, but deprecated way of doing it was as follows, this still works
  but should not be favoured over the previous approaches as it's not the
  Chaos Toolkit way to pass structured configurations.

  ```json
  {
    "configuration": {
      "azure": {
        "subscription_id": "your-azure-subscription-id"
      }
    }
  }
  ```

  [env_configuration]: https://docs.chaostoolkit.org/reference/api/experiment/#environment-configurations

- Subscription id in the Azure credential file

  Credential file described in the previous "Credential" section contains as well subscription id. If **AZURE_AUTH_LOCATION** is set and subscription id is **NOT** set in the experiment definition, extension will try to load it from the credential file.

  

### Putting it all together

Here is a full example for an experiment containing secrets and configuration: 

```json
{
  "version": "1.0.0",
  "title": "...",
  "description": "...",
  "tags": ["azure", "kubernetes", "aks", "node"],
  "configuration": {
    "azure_subscription_id": "xxx"
  },
  "secrets": {
    "azure": {
      "client_id": "xxx",
      "client_secret": "xxx",
      "tenant_id": "xxx"
    }
  },
  "steady-state-hypothesis": {
    "title": "Services are all available and healthy",
    "probes": [
      {
        "type": "probe",
        "name": "consumer-service-must-still-respond",
        "tolerance": 200,
        "provider": {
          "type": "http",
          "url": "https://some-url/"
        }
      }
    ]
  },
  "method": [
    {
      "type": "action",
      "name": "restart-node-at-random",
      "provider": {
        "type": "python",
        "module": "chaosazure.machine.actions",
        "func": "restart_machines",
        "secrets": ["azure"],
        "config": ["azure_subscription_id"]
      }
    }
  ],
  "rollbacks": []
}
```

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://peps.python.org/pep-0008/

The Chaos Toolkit projects require all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works

### Develop

If you wish to develop on this project, make sure to install the development
dependencies.

```console
$ pdm install --dev
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
$ pdm run test
```
