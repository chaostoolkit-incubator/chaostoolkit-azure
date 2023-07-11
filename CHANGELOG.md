# Changelog

## [Unreleased][]

[Unreleased]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.13.0...HEAD

## [0.13.0][] - 2023-07-11

[0.13.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.12.0...0.13.0

### Changed

* Swapped `psycopg2` for `pg8000` for two reasons:
  * The psycopg2 license (LGPL3) is incompatible with Apache v2
  * It requires to be built and since the binary package is also copyleft, we
    can't use it anyway

## [0.12.0][] - 2023-02-27

[0.12.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.11.1...0.12.0

### Added

-  Introduce actions for Azure Netapp Files, like deleting netapp volumes
-  Introduce actions and probes for Azure Storage, like deleting storage accounts and blob containers
-  Introduce actions and probes for Azure Kubernetes Service, like deleting or stopping managed clusters
-  Introduce action to deleting for a specific table or several random tables on databases.

## [0.11.1][] - 2023-02-26

[0.11.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.11.0...0.11.1

### Fixed

- Format of minimal Python version as per https://github.com/pypa/packaging/issues/673

### Added

-  Introduce actions for Azure Application Gateway, like starting, stopping, deleting application gateways and deleting routes
-  Introduce actions for Azure Database for PostgreSQL flexible, like starting, stoping, restarting and deleting servers
-  Introduce actions for Azure Database for PostgreSQL single, like restarting and deleting servers

## [0.11.0][] - 2022-06-14

[0.11.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.10.0...0.11.0

### Changed

-  Fix VM Scale Set Fetch and Commands [#134][134]
-  Requires Python 3.7 as Chaos Toolkit itself
-  Builds for Python 3.10 as well

[134]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/pull/134

## [0.10.0][] - 2021-06-10

[0.10.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.9.0...0.10.0

### Added

-  Adding new function attribute `arg_query_options` to make result as table, which is not the default option now
-  added an utility method to load version in setup.py
-  adding versions to azure libraries with a compatible release operator

### Changed

-  Renamed `credentials` to `credential` for the `ComputeManagementClient` and `WebSiteManagementClient` call
-  Replacing `ServicePrincipalCredentials` with `ClientSecretCredential` for service_principal authentication method
-  Using `logger.warning` instead of deprecated `logger.warn`
-  Stopped checking api version to generate dicts in `__to_dicts` function
-  changed function names to match new version of libraries:
`delete, restart, poweroff, deallocate` -> `begin_delete, begin_restart, begin_poweroff, begin_deallocate`
-  Switched from Travis to GitHub actions for building and releasing

## [0.9.0][] - 2021-03-15

[0.9.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.8.3...0.9.0

### Added

-   Individual Azure managemnt clients for website and compute resources

### Changed

-   Moved to support new Microsoft Azure python package dependencies. Now importt
    the msrestazure package.
-   Renamed `credentials` to `credential` for the `ResourceGraphClient` call

### Removed

-   Removed common init_client

## [0.8.3][] - 2020-05-14

[0.8.3]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.8.2...0.8.3

### Added

-   Missing init module files

## [0.8.2][] - 2020-05-14

[0.8.2]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.8.1...0.8.2

### Changed

-   Letting setuptools find all packages

## [0.8.1][] - 2020-05-14

[0.8.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.8.0...0.8.1

### Added

-   Expose the `auth` and `common` packages on building the top-level package

## [0.8.0][] - 2020-05-14

[0.8.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.7.0...0.8.0

### Added
- Return output from activities
- Allow user to load more than one VMSS instance for VMSS actions
- Update list of unsupported scripts for Windows VM
- Added network latency operation vor VMSS instances
- Added burn io (memory exploit) operation vor VMSS instances
- Added fill disk operation vor VMSS instances
- Interrupt an experiment execution when secrets are error-prone
- Interrupt an experiment execution when an invalid cloud is configured
- Remove an unused configuration property from the resource graph since it is deprecated
- Technical refactoring: Separate concerns from the main _init_ module
- Technical refactoring: Applied DRY principles in test module
- Technical refactoring: Resource graph client now outputs error messages
- Allow to load secrets from azure credential file

## [0.7.0][] - 2020-04-09

[0.7.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.6.0...0.7.0

### Added

- Supporting criteria for selection of the virtual machine scale set instance to stop
- Added optional path parameter to fill_disk

### Changed

- Use the official configuration accessor for `subscription_id` [#91][91]

[91]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/issues/91

## [0.6.0][] - 2019-11-12

[0.6.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.5.0...0.6.0

### Added

- Added the burn_io feature: increase the I/O operations per seconds of the 
hard drive for a time period (default time period is 1 minute). Works by 
copying random data into a burn folder, which is deleted at the end of the 
script.
- Added the network_latency feature: disturb the network of the VM, adding some
 latency for a time period (defaults to a 200 +/- 50ms latency for 1 minute).
  Only works on Linux machines for now.
- Supporting multiple Azure Cloud, such as AZURE_CHINA_CLOUD.
- Code clean up and refactoring, moving up client initiation.
- Added the ability to stress a machine instance in a virtual machine scale set
- Supporting Azure token based credentials (no refresh token support yet)

## [0.5.0][] - 2019-07-05

[0.5.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.4.0...0.5.0

### Added

-  Added the FillDisk feature: Create a file of random data on the disk of the 
VM for a time period (defaults to a 1GB file for 2 minutes).
-  Fixed the new MS Azure REST API version 2019-04-01

## [0.4.0][] - 2019-04-15

[0.4.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.3.1...0.4.0

### Changed

-   Enable virtual machine actions to select more than one machine
-   Introduce rollback action for virtual machines
-   Separate service fabric functionality from the chaostoolkit-azure extension
-   Introduce CPU stress action for VMs
-   Remove not used azure-mgmt dependencies (#53)
-   Introduce actions to stop, restart and start Azure Web Apps
-   Introduce probes to take measures of Azure Web Apps
-   Refactoring: Remove redundant check for security variables  from environment

## [0.3.1][] - 2019-06-01

[0.3.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.3.0...0.3.1

-   Remove Azure CLI and introduce the Azure Python SDK instead. See #36.
-   Ensure all packages are exported [#41][41]

[41]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/issues/41

## [0.3.0][] - 2018-12-19

[0.3.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.2.0...0.3.0

-   Introduce Azure CLI
-   Install Azure CLI resource-graph extension if it is not installed
-   Enable filtering of Azure infrastructure resources, e.g. virtual machines
-   Enable filtering of Azure infrastructure resources in probes
-   Introduce actions on Azure Kubernetes Services (AKS), like stopping, restarting, and
    deleting AKS nodes
-   Introduce actions on Azure Virtual Machine Scalesets (VMSS), like stopping, restarting, and
    deallocating AKS nodes
-   Emphasize the risk of deleting actions in the docstrings

## [0.2.0][] - 2018-10-19

[0.2.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.1.3...0.2.0

-   Refactoring: Straighten dependencies in requirements.txt
-   Update documentation
-   Refactoring: Moving authentication functions one module up
-   Manage Azure virtual machines with the machine subpackage
-   Exporting discovery ability

## [0.1.3][] - 2018-06-06

[0.1.3]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.1.2...0.1.3

### Changed

-   Exporting fabric subpackage

## [0.1.2][] - 2018-05-14

[0.1.2]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.1.1...0.1.2

### Changed

-   MANIFEST.in so that non-source code files are included in source distribution package

## [0.1.0][]

[0.1.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/tree/0.1.0

### Added

-   Initial release
