# -*- coding: utf-8 -*-
import configparser
import contextlib
import os.path
import tempfile

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets

from chaosazure.types import ServiceFabricAuth

__all__ = ["auth"]


@contextlib.contextmanager
def auth(configuration: Configuration, secrets: Secrets) -> ServiceFabricAuth:
    """
    Attempt to load the Service Fabric authentication information from a local
    configuration file or the passed `configuration` mapping. The latter takes
    precedence over the local configuration file.

    If you provide a configuration and secrets dictionary, the returned mapping
    will be created from their content. For instance, you could have:

    Configuration mapping (in your experiment file):
    ```python
    {
        "endpoint": "https://XYZ.westus.cloudapp.azure.com:19080",
        "verify_tls": False,
        "use_ca": False
    }
    ```

    Secrets mapping (in your experiment file):
    ```python
    {
        "azure": {
            "security": "pem",
            "pem_content": {
                "type": "env",
                "key": "AZURE_SERVICE_FABRIC_PEM"
            }
        }
    }
    ```

    In that case, the PEM content will be read from the local environment
    variable `AZURE_SERVICE_FABRIC_PEM` that you will have populated before
    hand. The content will be saved by the extension into a temporary file
    before being used to authenticate.

    You could also simply have that file ready instead:

    Secrets mapping (in your experiment file):
    ```python
    {
        "azure": {
            "security": "pem",
            "pem_path": "./party-cluster-XYZ-client-cert.pem"
        }
    }
    ```

    If you want to load the information from a local Service Fabric
    config file, set the `config_path` key in the `configuration mapping.

    Configuration mapping (in your experiment file):
    ```python
    {
        "config_path": "~/.sfctl/config"
    }
    ```
    The path will be expanded.

    The authentification file should look like this:

    ```ini
    [servicefabric]
    endpoint = https://XYZ.westus.cloudapp.azure.com:19080
    no_verify = true
    use_ca = false
    security = pem
    pem_path = ./party-cluster-XYZ-client-cert.pem
    ```

    No matter the input, the yielded dictionary looks like this:

    ```python
    {
        "endpoint": "https://XYZ.westus.cloudapp.azure.com:19080",
        "verify": False,
        "security": {
            "type": "pem",
            "path": "./party-cluster-XYZ-client-cert.pem"
        }
    }
    ```

    Using this function goes as follows:

    ```python
    with auth(configuration, secrets) as info:
        url = "{}{}".format(
            info["endpoint"], "/Tools/Chaos/$/Start?api-version=6.0")

        r = requests.get(
            url, cert=info["security"]["path"], verify=info["verify"])

    """
    c = configuration or {}
    s = secrets or {}

    config_path = c.get("config_path")
    endpoint = c.get("endpoint", s.get("endpoint"))

    if config_path:
        config_path = os.path.expanduser(config_path)
        if not os.path.exists(config_path):
            raise FailedActivity(
                "Service Fabric configuration file not found at {}".format(
                    config_path
                ))

        with open(config_path) as f:
            parser = configparser.ConfigParser()
            parser.read_file(f)

            pem_path = parser.get("servicefabric", "pem_path")
            if not pem_path:
                raise FailedActivity("cannot find {}".format(pem_path))

            yield {
                "endpoint": parser.get("servicefabric", "endpoint"),
                "verify": not (
                    parser.get("servicefabric", "no_verify") != "true"),
                "security": {
                    "type": parser.get("servicefabric", "security"),
                    "path": pem_path
                }
            }

    elif endpoint:
        verify_tls = c.get("verify_tls", s.get("verify_tls", True))
        use_ca = c.get("use_ca", s.get("use_ca", True))
        security_kind = s.get("security", c.get("security", "pem"))
        pem_path = s.get("pem_path", c.get("pem_path", None))
        pem_content = s.get("pem_content", c.get("pem_content", None))

        info = {
            "endpoint": endpoint,
            "verify": verify_tls,
            "security": {
                "type": security_kind,
                "path": pem_path
            }
        }

        if not pem_path or (not os.path.exists(pem_path) and pem_content):
            # the file will be deleted when we leave the context block
            with tempfile.NamedTemporaryFile(mode="w+",
                                             encoding='utf-8') as pem_path:

                pem_path.write(pem_content)
                pem_path.seek(0)

                info["security"]["pem_path"] = pem_path.name
                yield info
        else:
            yield info
    else:
        raise FailedActivity(
            "Service Fabric client needs to know how to authenticate")
