#############################
# Makefile for Pyton Projects
# (c) by CaeSium
#############################

.PHONY: clean
clean:
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' | xargs rm -rf
	@find . -type d -name '*.ropeproject' | xargs rm -rf
	@rm -rf build/
	@rm -rf dist/
	@rm -f MANIFEST
	@rm -rf docs/build/
	@rm -f .coverage.*
	@rm -f output/*.py
	@rm -f output/*.json
	@rm -f logs/*.log

init:
	sudo pip3 install -r requirements.txt;

all: all_mt

all_mt: mt_model_matter mt_swagger_db_connector_matter mt_fsm_model_matter

mt_model_matter:
	./loki.py -i ./src/mt_model_matter.json -o -l
mt_swagger_db_connector_matter:
	./loki.py -i ./src/mt_swagger_db_connector_matter.json -o -l
mt_fsm_model_matter:
	./loki.py -i ./src/mt_fsm_model_matter.json -o -l
