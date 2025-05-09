# Qadence-Hub


**Qadence-Hub** is a Github monorepo that hosts multiple Python packages developed under the **Qadence** initiative. It is structured to support independent development, testing, and deployment of each quantum features while maintaining a unified development environment.


[![Linting](https://github.com/pasqal-io/qadence-hub/actions/workflows/lint.yml/badge.svg)](https://github.com/pasqal-io/qadence-hub/actions/workflows/lint.yml)
[![Tests](https://github.com/pasqal-io/qadence-hub/actions/workflows/test.yml/badge.svg)](https://github.com/pasqal-io/qadence-hub/actions/workflows/test.yml)
[![Documentation](https://github.com/pasqal-io/qadence-hub/actions/workflows/build_docs.yml/badge.svg)](https://pasqal-io.github.io/qadence-hub/latest)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Qadence hub structure

<!-- insert figure of dependencies including qadence, pyqtorch and horqrux -->

<p align="center">
  <picture>
    <img alt="Qadence Hub structure" src="./docs/assets/qadence_hub.svg" width="75%">
  </picture>
<p align="center">

## 📦 Qadence extension packages

| Name | Description |
|------|-------------|
| `qadence-commons` | Shared libraries for Qadence​|
| `qadence-mitigation` | Tools for error mitigation in quantum circuit execution|
| `qadence-measurement` | Interfaces for executing and analyzing quantum measurement|
| `qadence-model` | Quantum ML models built on variational quantum circuits|

## Publishing to PyPI

We publish each package separately. After you merge your `sub-main` branch to `main,` you can publish your documents and Python package through release. To do this, you need to update the version number in the package's `pyproject.toml`. Then, you create a release with the format of `package_name-v.x.y.z,` where x, y, and z are for version numbers. For example, if you want to publish `qadence-model` with version 1.2.5, you must put `model-v1.2.5` as your release name.

## Contributing

Before making a contribution, please review our [code of conduct](docs/CODE_OF_CONDUCT.md).

- **Submitting Issues:** To submit bug reports or feature requests, please use our [issue tracker](https://github.com/pasqal-io/qadence-hub/issues).
- **Developing in qadence:** To learn more about how to develop within `qadence-hub`, please refer to [contributing guidelines](docs/contributing.md).

## License
Qadence-Hub is a free and open source software package, released under the Apache License, Version 2.0.
