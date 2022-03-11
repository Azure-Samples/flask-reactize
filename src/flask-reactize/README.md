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

## Installation

To install with `pip`, run the following command in a terminal:

```bash
/> python -m pip install flask-reactize
```

## Usage

In order to use *flask-reactize*, you first need to have a [React JS](https://reactjs.org/) application (it if is not already the case).

Follow the steps below to setup a sample demo site and activate *flask-reactize* to serve both the development application (via an underlying nodejs server) and the production application (compiled in static):

```bash
# Ensure you have nodejs and Python 3.8/3.10 on your environment
# Create a React JS application
/> npx create-react-app demo-app

# Create the python bootstrap to serve this created app
/> python -m pip install flask-reactize
/> vi main.py
```

Paste the following snippet into your `main.py` file:

```python
import os
from flask import Flask
from flask_reactize import FlaskReactize

app = Flask(__name__)

FlaskReactize(app).serve_react_app(
        os.path.join(os.path.dirname(__file__), "demo-app")
    )
```

Save your file and start your `Flask` server:

```bash
/> FLASK_APP=main flask run -p 8080 # Or whatever port you want to use
```

Open your browser and navigate to [http://localhost:8080](http://localhost:8080)

If you want to try the compiled version of the [React JS](https://reactjs.org/) application, run the following:

```bash
# Compile the react app
/> cd demo-app
/> npm run build

# Once the compilation is done, create a new python file
/> cd ../ && vi main_static.py
```

Paste the following snippet into your `main_static.py` file:

```python
import os
from flask import Flask
from flask_reactize import FlaskReactize

app = Flask(__name__)

FlaskReactize(app).serve_static(
        static_folder=os.path.join(os.path.dirname(__file__), "demo-app/build")
    )
```

Save your file and start your `Flask` server:

```bash
/> FLASK_APP=main_static flask run -p 8080 # Or whatever port you want to use
```

Open your browser and navigate to [http://localhost:8080](http://localhost:8080)

## More samples

If you want more samples, with both not compiled and compiled [React JS](https://reactjs.org/) served by the same file, or if you want to see the API proxy in action, navigate [there](https://github.com/Azure-samples/flask-reactize) and clone the project to either use the `sample` site or one of the `dockerFile` available.

## API

*flask-reactize* API is very minimaliste, you have two methods available to call.

To serve static files, use:

```python
from flask import Flask
from flask_reactize import FlaskReactize

app = Flask(__name__)

FlaskReactize(app).serve_static(
        static_folder="Folder where the static assets are",
        proxy_api="Dictionary with proxied routes
    )

```

To serve the application in developer mode, use:

```python
from flask import Flask
from flask_reactize import FlaskReactize

app = Flask(__name__)

FlaskReactize(app).serve_react_app(
        source_react_folder="Folder where the react sources are",
        port="Port number to start the React app on. Optional, default 3005",
        proxy_api="Dictionary with proxied routes
    )

```

Each method can take a `dict` called `proxy_api` in order to route API calls from the [React JS](https://reactjs.org/) to the remote endpoint to avoid security issue.

Let's say your remote endpoint is `http://some-api/api` where, for instance, you get a users list. Your endpoint in your code would be `http://some-api/api/users`.

To proxy that endpoint you'll need to create a dict and pass it to one of the method of the `FlaskReactize` you are using:

```python
from flask import Flask
from flask_reactize import FlaskReactize

app = Flask(__name__)

proxy_api = {
    "/someApi": "http://some-api/api"
}

FlaskReactize(app).serve_react_app(
        source_react_folder="Folder where the react sources are",
        port="Port number to start the React app on. Optional, default 3005",
        proxy_api="Dictionary with proxied routes
    )

```

Then, in your React code (client code) you can call the following endoint

```javascript
onst usersListEndpoint = "/someApi/users";

const getUsers = async () => {

  return await fetch(usersListEndpoint, {
      method: "GET",
      headers:  {
          'Content-Type': 'application/json'
      }
    })
};
```

`/someApi/users` will be processed by the Python application, replaced with `http://some-api/api/users` and called. The output of the remote endpoint will be sent *as it is* to the client.

More info and sample code can be found on [Github](https://github.com/azure-samples/flask-reactize).

## Known limitions

As of today:

* *flask-reactize* does not support calling protected APIs.
