# Contributing

We welcome contributions to this repository! 

Please use the following guidelines for contributing. 

We distinguish two types of contributions: new templates, and changes to the structure of the API. 


## New templates
For adding new templates, install the packages in requirements-dev.txt in a new virtual environment, then follow the steps described [here](https://github.com/hubmapconsortium/user-templates-api/blob/development/src/user_templates_api/templates/jupyter_lab/templates/new_template/README.md)


## Editing the main structure of the API
We use a Docker container. Please see [the docker documentation](https://hub.docker.com/_/docker)


## Linting
We use Flake8, Black and isort for linting Python code. If you have installed the packages in requirements-dev.txt, you can simply run the following:
```sh
flake8 path-to-file
```
```sh
black path-to-file
```
```sh
isort path-to-file
```