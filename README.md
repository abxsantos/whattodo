### CLI tool to organize stuff.

`$ docker run -it -v "$(pwd)":/workspace abxsantos/python`
Branch | Travis | Codecov | SonarCloud
-------|--------|---------|------
master | [![Build Status](https://travis-ci.org/abxsantos/whattodo.svg?branch=main)](https://travis-ci.org/abxsantos/whattodo) | [![codecov](https://codecov.io/gh/abxsantos/whattodo/branch/main/graph/badge.svg?token=CW0DV93ZZY)](https://codecov.io/gh/abxsantos/whattodo) | [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=abxsantos_whattodo&metric=alert_status)](https://sonarcloud.io/dashboard?id=abxsantos_whattodo)
<br>

## Developing with Docker
---
<br>

```shell
$                                       # Or any other 
$                                       # python 3.9 image
$ docker run -it -v "$(pwd)":/workspace abxsantos/pydev /bin/bash
```

Once inside the container, to install the dependencies

`# pipenv install --dev --pre --system`
```shell
$ pipenv install --dev --pre --system
```

To lint the project

`# pipenv install --dev --pre --system`
```shell
$ ./scripts/lint.sh
```

## Building with poetry
---
<br>

```shell
$ # Build project with poetry
$ poetry build

$ # Install built package whl with pip
$ pip install --user dist/whattodo-0.0.0-py3-none-any.whl

$ # Export path  if needed
$ export PATH="${PATH}:/home/{user}/.local/bin"
```

Run using
```shell
$ whattodo --help
```