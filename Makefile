.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build-dev
build-dev:  ## Build local dev image
	docker-compose build --pull app

.PHONY: bash
bash:  ## Run inside container
	docker-compose run --rm app bash

.PHONY: test
test:  ## Run tests; can pass extra args like this: make test OPTIONS="-s"
	docker-compose run --rm app pytest $(OPT)

.PHONY: build-test ## Build local dev image and run tests
build-test: build-dev test

.PHONY: normalize
normalize:  ## Normalize CSV file
	docker-compose run --rm app python3 src/csv_normalizer.py

.PHONY: lint
lint:  ## Run black to lint code
	docker-compose run --rm app black .
