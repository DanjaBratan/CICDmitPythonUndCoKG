IMAGE_REG ?= docker.io
IMAGE_REPO ?= danielderking11/cicdmitpythonundcokg
IMAGE_TAG ?= latest
TEST_HOST ?= localhost:5000
SRC_DIR := src

.PHONY: clean lint lint-fix run-python-app test test-report test-api docker-build-image docker-run-container docker-push-image venv .EXPORT_ALL_VARIABLES


# ===========================================

clean:  ## 🧹 Projekt aufräumen
	rm -rf $(SRC_DIR)/.venv
	rm -rf postman-test/node_modules
	rm -rf postman-test/package*
	rm -rf test-results.xml
	rm -rf $(SRC_DIR)/app/__pycache__
	rm -rf $(SRC_DIR)/app/tests/__pycache__
	rm -rf .pytest_cache
	rm -rf $(SRC_DIR)/.pytest_cache

lint: venv  ## 🔎 Stilprüfung & Formatierung, behebt keine Fehler, returnt Exit bei Fehlern 
	. $(SRC_DIR)/.venv/bin/activate \
	&& black --check $(SRC_DIR) \
	&& flake8 src/website/ && flake8 src/main.py

lint-fix: venv  ## 📜 Stilprüfung & Formatierung, versucht Fehler zu beheben und Code zu ändern
	. $(SRC_DIR)/.venv/bin/activate \
	&& black $(SRC_DIR)

# ===========================================

## 🏃 lokales Ausführen des Servers mit Python und Flask im Hintergrund
run-python-app: venv
	. $(SRC_DIR)/.venv/bin/activate \
	&& python3 src/run.py &

stop-python-app: ## 🛑 Beendet den im Hintergrund laufenden Python-Server
	pkill -f 'python3 src/run.py'

test: venv  ## 🎯 Unit Tests für Flask app (ohne report xml)
	. $(SRC_DIR)/.venv/bin/activate \
	&& pytest -v

test-report: venv  ## 🎯 Unit tests für Flask app 
	. $(SRC_DIR)/.venv/bin/activate \
	&& pytest -v --junitxml=test-results.xml

test-api: .EXPORT_ALL_VARIABLES ## 🚦 Durchführen von Integration-API-Tests; Server muss ausgeführt werden
	cd postman-test \
	&& npm install newman \
	&& ./node_modules/.bin/newman run ./pm-test.json --env-var apphost=$(TEST_HOST)

# ===========================================

docker-build-image:  ## 🔨 Erstellt ein Container-Image aus dem Dockerfile 
	sudo docker build . --file build/Dockerfile \
	--tag $(IMAGE_REG)/$(IMAGE_REPO):$(IMAGE_TAG)
	
docker-run-container: ## Bringt alle bisherigen Container zum Stoppen und startet den Python-Container
	sudo docker run -d --rm -it -p 5000:5000 danielderking11/cicdmitpythonundcokg:latest

docker-push-image:  ## 📤 Pushen des Container-Images ins Registry 
	sudo docker push $(IMAGE_REG)/$(IMAGE_REPO):$(IMAGE_TAG)

# ===========================================

## venv aufsetzen
venv: $(SRC_DIR)/.venv/touchfile

$(SRC_DIR)/.venv/touchfile: $(SRC_DIR)/requirements.txt
	python3 -m venv $(SRC_DIR)/.venv
	. $(SRC_DIR)/.venv/bin/activate; pip install -Ur $(SRC_DIR)/requirements.txt
	touch $(SRC_DIR)/.venv/touchfile
