# Changelog

## [Unreleased][]

[Unreleased]: https://github.com/chaostoolkit-incubator/chaostoolkit-azure/compare/0.3.1...HEAD

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