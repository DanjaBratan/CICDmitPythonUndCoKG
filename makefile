IMAGE_REG ?= docker.io
IMAGE_REPO ?= danielderking11/cicdmitpythonundcokg
IMAGE_TAG ?= latest
TEST_HOST ?= localhost:5000
SRC_DIR := src


lint: venv  ## 🔎 Lint & format, will not fix but sets exit code on error 
	. $(SRC_DIR)/.venv/bin/activate \
	&& black --check $(SRC_DIR) \
	&& flake8 src/website/ && flake8 src/main.py

lint-fix: venv  ## 📜 Lint & format, will try to fix errors and modify code
	. $(SRC_DIR)/.venv/bin/activate \
	&& black $(SRC_DIR)


docker-build-image:  ## 🔨 Build container image from Dockerfile 
	sudo docker build . --file build/Dockerfile \
	--tag $(IMAGE_REG)/$(IMAGE_REPO):$(IMAGE_TAG)
	
docker-run-container: 
	sudo docker run -d --rm -it -p 5000:5000 danielderking11/cicdmitpythonundcokg:latest

docker-push-image:  ## 📤 Push container image to registry 
	sudo docker push $(IMAGE_REG)/$(IMAGE_REPO):$(IMAGE_TAG)

## 🏃 für lokales Ausführen des Servers mit Python und Flask 
run-python-app: venv
	. $(SRC_DIR)/.venv/bin/activate \
	&& python3 src/main.py


test: venv  ## 🎯 Unit tests for Flask app
	. $(SRC_DIR)/.venv/bin/activate \
	&& pytest -v

test-report: venv  ## 🎯 Unit tests for Flask app (with report output)
	. $(SRC_DIR)/.venv/bin/activate \
	&& pytest -v --junitxml=test-results.xml

test-api: .EXPORT_ALL_VARIABLES  ## 🚦 Run integration API tests, server must be running 
	cd postman-test \
	&& npm install newman \
	&& ./node_modules/.bin/newman run ./pm-test.json --env-var apphost=$(TEST_HOST)

clean:  ## 🧹 Clean up project
	rm -rf $(SRC_DIR)/.venv
	rm -rf postman-test/node_modules
	rm -rf postman-test/package*
	rm -rf test-results.xml
	rm -rf $(SRC_DIR)/app/__pycache__
	rm -rf $(SRC_DIR)/app/tests/__pycache__
	rm -rf .pytest_cache
	rm -rf $(SRC_DIR)/.pytest_cache

# ============================================================================

venv: $(SRC_DIR)/.venv/touchfile

$(SRC_DIR)/.venv/touchfile: $(SRC_DIR)/requirements.txt
	python3 -m venv $(SRC_DIR)/.venv
	. $(SRC_DIR)/.venv/bin/activate; pip install -Ur $(SRC_DIR)/requirements.txt
	touch $(SRC_DIR)/.venv/touchfile
