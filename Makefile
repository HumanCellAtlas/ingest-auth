ZIP_FILE := Ingest_App.zip
TARGET := target/$(ZIP_FILE)

default: build

.PHONY: install
install:
	virtualenv -p python3 venv
	. venv/bin/activate && pip install -r requirements.txt --upgrade

.PHONY: test
test:
	. venv/bin/activate && python -m unittest discover -s test -p 'test_*.py'

.PHONY: build
build:
	rm -rf target
	mkdir target
	cd target && zip -r $(ZIP_FILE) ../*.py

.PHONY: deploy
deploy:
	$(MAKE) build
	export ACCOUNT_ID=aws sts get-caller-identity | jq -r .Account
	aws s3api create-bucket --bucket=ingest-auth-$(ACCOUNT_ID) --region=us-east-1 --profile hca
	aws s3 rm s3://ingest-auth-$(ACCOUNT_ID)/ingest-auth.zip
	aws s3 cp $(TARGET) s3://ingest-auth-$(ACCOUNT_ID)/ingest-auth.zip
