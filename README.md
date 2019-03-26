# Chaos Toolkit Extension for Azure

[![Build Status](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-azure.svg?branch=master)](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-azure)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-azure.svg)](https://www.python.org/)

This project is a collection of [actions][] and [probes][], gathered as an
extension to the [Chaos Toolkit][chaostoolkit]. It targets the
[Microsoft Azure][azure] platform.

[actions]: http://chaostoolkit.org/reference/api/experiment/#action
[probes]: http://chaostoolkit.org/reference/api/experiment/#probe
[chaostoolkit]: http://chaostoolkit.org
[azure]: https://azure.microsoft.com/en-us/

## Install

This package requires Python 3.5+

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



## Configuration

### Credentials
This extension uses the [Azure SDK][sdk] libraries under the hood. The Azure SDK library
expects that you have a tenant and client identifier, as well as a client secret and subscription, that allows you to 
authenticate with the Azure resource management API.

[creds]: https://docs.microsoft.com/en-us/azure/service-fabric/service-fabric-connect-to-secure-cluster
[requests]: http://docs.python-requests.org/en/master/
[sdk]: https://github.com/Azure/azure-sdk-for-python

There are two ways of doing this:

* you can either pass the name of the environment variables to the experiment definition as follows (recommended):

    ```json
    {
        "azure": {
            "client_id": "AZURE_CLIENT_ID",
            "client_secret": "AZURE_CLIENT_SECRET",
            "tenant_id": "AZURE_TENANT_ID"
        }
    }
    ```
    
* or you inject the secrets explicitly to the experiment definition:

    ```json
    {
        "azure": {
            "client_id": "your-super-secret-client-id",
            "client_secret": "your-even-more-super-secret-client-secret",
            "tenant_id": "your-tenant-id"
        }
    }
    ```
    
    Additionally you need to provide the Azure subscription id.

    ```json
    {
        "azure": {
            "subscription_id": "your-azure-subscription-id"
        }
    }
    ```

### Putting it all together

Here is a full example:

```json
{
  "version": "1.0.0",
  "title": "...",
  "description": "...",
  "tags": [
    "azure",
    "kubernetes",
	"aks",
	"node"
  ],
  "configuration": {
    "azure": {
      "subscription_id": "xxx"
	}
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
        "secrets": [
          "azure"
        ],
        "config": [
          "azure"
        ]
      }
    }
  ],
  "rollbacks": [
    
  ]
}
```

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Chaos Toolkit projects require all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works

### Develop

If you wish to develop on this project, make sure to install the development
dependencies. But first, [create a virtual environment][venv] and then install
those dependencies.

[venv]: http://chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```console
$ pip install -r requirements-dev.txt -r requirements.txt 
```

Then, point your environment to this directory:

```console
$ python setup.py develop
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
$ pytest
```
