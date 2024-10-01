# Example FastApi app

Application for the administration of telegram bot users

## Table of contents

- [Stack](#stack)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Tests](#tests)
- [CI/CD](#ci/cd)
- [Monitoring](#monitoring)
- [ADR](#adr)
- [Makefile](#makefile)

## Stack

Description of the technology stack used in the project.

- Python 3.12
- FastApi
- Postgres

## Prerequisites

Information about all needed tools you have to install before you start the development.

Make sure you have installed all the following prerequisites on your development machine:

- [Python 3.12](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/)
- [GIT](https://git-scm.com/downloads)
- [Make](http://gnuwin32.sourceforge.net/packages/make.htm)
- [Docker version >= 20.10.7](https://www.docker.com/get-started)
- [docker-compose version >= 1.29.2](https://docs.docker.com/compose/install/)

## Setup

Description of how to setup the project to be able to start the development.

1. Install dependencies:

```bash
$ poetry install
```

2. Setup pre-commit hooks before committing:

```bash
$ poetry run pre-commit install
```

## Architecture

Description of the project's architecture. Diagrams, maps, etc.

## Tests

Description of how to run the tests.

**Example:**

To run all tests you can use:

```bash
$ poetry run pytest
```

or

```bash
$ make tests
```

## CI/CD

Description of what the CI/CD process looks like and how it works. What is the deployment strategy etc?

## Monitoring

Information about tools used to monitor the application, how to use them, what is the purpose, how to access etc.

## ADR

Information about ADRs

**Example:**

We are using ADRs to describe our architecture/project decisions

[What is ADR?](https://github.com/joelparkerhenderson/architecture-decision-record)

If you are interesting take a look at `./docs/adr` directory.

## Makefile

We use Makefile to automate some common stuff

If you want to run all linting tools

```bash
$ make lint
```

If you want to run all audit checks:

```bash
$ make audit
```

If you want to run tests:

```bash
$ make tests
```
