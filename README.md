# flask-reactize

[![PyPI version](https://badge.fury.io/py/flask-reactize.svg)](https://badge.fury.io/py/flask-reactize)

Developing a ReactJS application requires to use nodejs as back end server.
What if you want to consume external APIs: how are you going to handle cross origin calls?

In modern days, as we are now, [React JS](https://reactjs.org/) offers many nice functionalities to develop an application easily, from any IDE.

In development mode, [React JS](https://reactjs.org/) requires [NodeJS](https://nodejs.org/en/) as a back end server. [NodeJS](https://nodejs.org/en/) maintains a connection between your development environment and your browser where the application is loaded so that:

* it refreshes automatically when an update is made,
* it sends in real time any error, warning that may have, in both the console and the developers toolbar of your browser of choice.

For production, you can compile your [React JS](https://reactjs.org/) application into static assets - you can then use any technology to serve those static files.

However, if your [React JS](https://reactjs.org/) calls external APIs (whether there are customs, or public) you will face security issues.

## Features

*flask-reactize* is a boostrap to serve any [React JS](https://reactjs.org/) via a Python back-end, using [Flask](https://flask.palletsprojects.com/en/2.0.x/) as web framework. 

Your back-end web server can be anything: [Flask](https://flask.palletsprojects.com/en/2.0.x/) itself (although not recommended for production), [Uvicorn](https://www.uvicorn.org/), [Gunicorn](https://gunicorn.org/) etc.

In a nutshell, *flask-reactize* is a proxy for your [React JS](https://reactjs.org/) application and for your APIs:

* It has a development mode: a nodejs server is transparently started by the Python back-end,
* It supports production mode: this back-end can also serve your static assets,
* It supports hot reload while developing: changing the Python code or the React code will trigger a browser refresh,
* It supports proxying multiple APIs via specific routes.

## Getting Started

Here is what you are going to find in this repo:

* Under *src/flask-reactize* you will find the Python module (also available via [PyPi](https://pypi.org/project/flask-reactize/)),
* Under *sample/* you will find a simple demo site built with [React JS](https://reactjs.org/) using *flask-reactize*,
* Two *DockerFile* for Python 3.8 and Python 3.10.

### Prerequisites

* [vscode](https://code.visualstudio.com/) because you are going to use [DevContainers](https://code.visualstudio.com/docs/remote/containers) to have all prerequisites without any hassle,
* [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) extension,
* [docker](https://www.docker.com/)

### Quickstart with Docker

To experiment in a minimum of effort what this library is doing, follow the steps below:

1. git clone https://github.com/Azure-samples/flask-reactize
2. cd flask-reactize
3. run `code .` to open the repository in [vscode](https://code.visualstudio.com/) (if the command is not available, activate it [here](https://code.visualstudio.com/docs/setup/setup-overview)).

Once [vscode](https://code.visualstudio.com/) is opened, build the development container:

1. open the Palette (Ctrl+Shift+P / Cmd+Shift+P)
2. select *Remote-Containers: Reopen in container*

Once the container is built, your [vscode](https://code.visualstudio.com/) is fully operational. If you open the terminal built in [vscode](https://code.visualstudio.com/), you will be prompted directly inside the container, as a "dummy" user called *alex*.

You can now build the *flask-reactize* container to test *flask-reactize* in either Python 3.8 or 3.10 version

1. run `make docker-build-sample-py38` in the terminal for Python 3.8
2. OR run `make docker-build-sample-py310` in the terminal for Python 3.10
3. then run `make docker-run-sample` to start the sample demo site

> If running the commands above result in an access is denied for the file `/var/run/docker.sock`, ensure that your user is the owner of this file. If it is not the case, run `sudo chown vscode:vscode /var/run/docker.sock` in the terminal.

You can now open your browser and load the url [http://localhost:8080](http://localhost:8080).

This sample uses [req|res](https://reqres.in) test APIs.

### Use this library in your project

**Please note** that you need to be on a *nix system for that, whether you are on Linux, Mac or Windows with [WSL](https://docs.microsoft.com/en-us/windows/wsl/about).

Instructions to follow can be found [here](./src/flask-reactize/README.md).

### Deploy to Azure

You can deploy your web application on Azure following one of the following methods (non exhaustive list):

1. Using [Web App for Containers](https://docs.microsoft.com/en-us/azure/app-service/quickstart-custom-container?tabs=dotnet&pivots=container-linux),
2. Using a [Web App](https://docs.microsoft.com/en-US/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-portal%2Cterminal-bash%2Cvscode-deploy%2Cdeploy-instructions-azportal%2Cdeploy-instructions-zip-azcli),
3. Using [Azure Kubernetes Service](https://azure.microsoft.com/en-us/services/kubernetes-service/#overview) in a multi-scalable containers scenario.

## Changelog

Changelog can be found [here](./CHANGELOG.md).

## Contributing

If you want to contribute to *flask-reactize*, [follow this guide](./CONTRIBUTING.md).
