SHELL=/bin/bash

clean:
	@find . -name '__pycache__' -exec rm -fr {} +
	@find . -name '.pytest_cache' -exec rm -fr {} +
	@find . -name 'build' ! -path '*/node_modules/*' -exec rm -fr {} +
	@find . -name 'dist' ! -path '*/node_modules/*' -exec rm -fr {} +
	@find . -name 'flask_reactize.egg-info' -exec rm -fr {} +
	@find . -name '.coverage' -exec rm -f {} +
	@find . -name 'coverage.xml' -exec rm -f {} +
	@find . -name 'pytest-results.xml' -exec rm -f {} +

install-deps:
	@make install-deps --directory src/flask-reactize

docker-build-sample-py38:
	@test -d ./sample/static || (echo "You need to compile your React application first"; exit 1)
	
	@echo "Build docker image"
	@docker build --no-cache -t flask-reactize-sample:latest -f DockerFile-py38 .

docker-build-sample-py310:
	@test -d ./sample/static || (echo "You need to compile your React application first"; exit 1)
	
	@echo "Build docker image"
	@docker build -t flask-reactize-sample:latest -f DockerFile-py310 .

docker-run-sample:
	@test -z "$(shell docker images -q flask-reactize-sample:latest)" || \
		docker run -p 8080:80 flask-reactize-sample:latest