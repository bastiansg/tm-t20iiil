.PHONY: core-build core-run devcontainer-build images print-test print-acopio print-acopio-test


core-build:
	docker compose build tm-t20iiil-core

core-run: core-build
	docker compose run --rm tm-t20iiil-core


devcontainer-build:
	docker compose build tm-t20iiil-devcontainer

process-acopio-images: devcontainer-build
	docker compose run --rm --entrypoint="env PYTHONPATH=/workspace/src python -m tm_t20iiil.scripts.acopio.process_images" tm-t20iiil-devcontainer

print-test: devcontainer-build
	docker compose run --rm --entrypoint="env PYTHONPATH=/workspace/src python -m tm_t20iiil.prints.test" tm-t20iiil-devcontainer

print-acopio: devcontainer-build
	docker compose run --rm --entrypoint="env PYTHONPATH=/workspace/src python -m tm_t20iiil.prints.acopio" tm-t20iiil-devcontainer

print-acopio-test: devcontainer-build
	docker compose run --rm --entrypoint="env PYTHONPATH=/workspace/src python -m tm_t20iiil.prints.acopio_test" tm-t20iiil-devcontainer
