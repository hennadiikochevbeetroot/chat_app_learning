.DEFAULT_GOAL := help

.PHONY: help
help: ## Display this help
	@echo "Available make commands:"
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

.PHONY: server
server: ## Run chat server
	python main.py --server

.PHONY: client
client: ## Run chat client
	python main.py --client
