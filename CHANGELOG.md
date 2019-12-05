# Changelog

## [Unreleased][]
[Unreleased]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.6.0...HEAD

### Added

- Supporting criteria for selection of the virtual machine scale set instance to stop

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
