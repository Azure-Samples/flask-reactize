SHELL=/bin/bash

clean:
	@make clean --directory ../

install-deps:
	@pip install -r requirements.txt --quiet
	@npm install --prefix "react_app" --quiet

compile-react:
	@npm run build --prefix "react_app"
	@rm -Rf static || true
	@mv react_app/build static

run-dev:
	@PYTHONPATH=../src/flask-reactize/src \
		MODE="dev" \
		FLASK_APP=main \
		flask run --reload

run-prod:
	@PYTHONPATH=../src/flask-reactize/src \
		MODE="prod" \
		FLASK_APP=main \
		flask run