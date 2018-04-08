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
        "module": "chaosazure.factory.actions",
        "func": "start_chaos",
        "secrets": ["azure"],
        "arguments": {
            "parameters": {
                "TimeToRunInSeconds": 45
            }
        }
    }
},
{
    "type": "action",
    "name": "stop-service-factory-chaos",
    "provider": {
        "type": "python",
        "module": "chaosazure.factory.actions",
        "func": "stop_chaos",
        "secrets": ["azure"]
    }
}
```

That's it!

Please explore the code to see existing probes and actions.



## Configuration

### Credentials

This extension uses the [requests][] library under the hood. This library
expects that you have a PFX certificate, converted as to the PEM format, that
allows you to authenticate with the [Service Factory][sf] endpoint.

[sf]: https://docs.microsoft.com/en-us/azure/service-fabric/service-fabric-controlled-chaos
[creds]: https://docs.microsoft.com/en-us/azure/service-fabric/service-fabric-connect-to-secure-cluster

Generally speaking, there are two ways of doing this:

* you have [created][creds] a configuration file where you will run the
  experiment from (so with a `~/.sfctl/config` file)
* you explicitely pass the correct environment variables to the experiment
  definition as follows:

    Configuration section:

    ```json
    {
        "endpoint": "https://XYZ.westus.cloudapp.azure.com:19080",
        "verify_tls": false,
        "use_ca": false
    }
    ```

    Secrets section:

    ```json
    {
        "azure": {
            "security": "pem",
            "pem_path": "./cluster-client-cert.pem"
        }
    }
    ```

    The PEM can also be passed as an environment variable:


    ```json
    {
        "azure": {
            "security": "pem",
            "pem_content": {
                "type": "env",
                "key": "AZURE_PEM"
            }
        }
    }
    ```

    The environment variable name can be anything.

### Putting it all together

Here is a full example:

```json
{
    "version": "1.0.0",
    "title": "...",
    "description": "...",
    "configuration": {
        "endpoint": "https://XYZ.westus.cloudapp.azure.com:19080",
        "verify_tls": false,
        "use_ca": false
    },
    "secrets": {
        "azure": {
            "security": "pem",
            "pem_path": "./cluster-client-cert.pem"
        }
    },
    "steady-state-hypothesis": {
        "title": "Services is healthy",
        "probes": [
            {
                "type": "probe",
                "name": "application-must-respond",
                "tolerance": 200,
                "provider": {
                    "type": "http",
                    "verify_tls": false,
                    "url": "https://some-url-in-cluster/"
                }
            }
        ]
    },
    "method": [
        {
            "type": "action",
            "name": "start-service-factory-chaos",
            "provider": {
                "type": "python",
                "module": "chaosazure.factory.actions",
                "func": "start_chaos",
                "secrets": ["azure"],
                "arguments": {
                    "parameters": {
                        "TimeToRunInSeconds": 45
                    }
                }
            },
            "pauses": {
                "after": 30
            }
        },
        {
            "type": "probe",
            "ref": "application-must-respond"
        },
        {
            "type": "action",
            "name": "stop-service-factory-chaos",
            "provider": {
                "type": "python",
                "module": "chaosazure.factory.actions",
                "func": "stop_chaos",
                "secrets": ["azure"]
            },
            "pauses": {
                "after": 5
            }
        },
        {
            "type": "probe",
            "name": "get-service-factory-chaos-report",
            "provider": {
                "type": "python",
                "module": "chaosazure.factory.probes",
                "func": "chaos_report",
                "secrets": ["azure"],
                "arguments": {
                    "start_time_utc": "1 minute ago",
                    "end_time_utc": "now"
                }
            }
        }
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
