.PHONY: core-build core-run devcontainer-build print-test


core-build:
	docker compose build tm-t20iiil-core

core-run: core-build
	docker compose run --rm tm-t20iiil-core


devcontainer-build:
	docker compose build tm-t20iiil-devcontainer

print-test: devcontainer-build
	docker compose run --rm --entrypoint="env PYTHONPATH=/workspace/src python -m tm_t20iiil.scripts.print_test" tm-t20iiil-devcontainer
