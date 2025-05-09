# Qadence Hub Overview

Welcome to the documentation for the **Qadence Hub**.
This repository contains multiple modular Python packages developed for **Qadence** features

## Included Packages

- [**qadence-commons**](https://pasqal-io.github.io/qadence-hub/qadence-commons/latest/): Shared quantum utilities library in Qadence
- [**qadence-mitigation**](https://pasqal-io.github.io/qadence-hub/qadence-mitigation/latest/): Quantum error mitigation techniques
- [**qadence-measurement**](https://pasqal-io.github.io/qadence-hub/qadence-measurement/latest/): Quantum output measurement methods
- [**qadence-model**](https://pasqal-io.github.io/qadence-hub/qadence-model/latest/): Quantum constructors for various blocks and ansätze.


## Package Codes

- [**qadence-commons**](https://github.com/pasqal-io/qadence-hub/tree/main/qadence-commons)
- [**qadence-mitigation**](https://github.com/pasqal-io/qadence-hub/tree/main/qadence-mitigation)
- [**qadence-measurement**](https://github.com/pasqal-io/qadence-hub/tree/main/qadence-measurement)
- [**qadence-model**](https://github.com/pasqal-io/qadence-hub/tree/main/qadence-model)


## Development Resources

- [Setup Guide](setup.md)
- [Testing](test.md)


## Qadence-Hub Structure

This repository follows a modular monorepo layout.

    qadence-hub/
    ├── qadence-commons/           # Shared utility libraries for Qadence
    ├── qadence-mitigation/        # Tools for error mitigation in quantum circuit execution
    ├── qadence-measurement/       # Interfaces for executing and analyzing quantum measurement
    ├── qadence-model/             # Quantum ML models built on variational quantum circuits
    ├── docs/                       # Root documentation site
    ├── pyproject.toml              # Project configuration (Hatch-based)
    └── .github/workflows/          # CI/CD pipelines (tests, docs, lint)

Each module is independently versioned and will be published to PyPI.

## Directory Conventions

- Use `project_name/` layout inside each module for source codes
- Tests should live in `tests/` inside each module
- Documentation should reside in the root `docs/` or module-specific docs
