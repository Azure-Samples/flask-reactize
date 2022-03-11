from os import path

from setuptools import setup


def get_description() -> str:
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()


setup(
    name="flask-reactize",
    package_dir={"": "src"},
    packages=["flask_reactize"],
    version="1.0.0a3",
    author="Julien Chomarat",
    license="MIT",
    author_email="juchomar@microsoft.com",
    description="Serve React JS application from a Flask application.",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    keywords=["python"],
    url="https://github.com/Azure-samples/flask-reactize",
    project_urls={
        "Bug Tracker": "https://github.com/Azure-samples/flask-reactize/issues",
    },
    install_requires=["flask==2.0.2", "requests==2.26.0"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)
