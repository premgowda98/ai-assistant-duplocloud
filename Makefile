# to print vairable values with make
print-% : ; @echo $* = $($*)

# code checks
check_ruff:
	@(which ruff) > /dev/null || (pip install ruff) > /dev/null

codechecks: check_ruff
	@echo "* \e[0;33mRunning code fixes\e[m"
	@ruff check --fix
	@echo "* \e[0;33mFinished code fixes\e[m"

	@echo "* \e[0;33mRunning code format\e[m"
	@ruff format
	@echo "* \e[0;33mFinished code formt\e[m"

	@echo "* \e[0;33mRunning code checks\e[m"
	@ruff check
	@echo "* \e[0;33mFinished code checks\e[m"

uv_requirements:
	uv pip compile pyproject.toml -o requirements.txt

# Docker section

IMAGE_REGISTRY=localhost:5000
IMAGE_TAG=latest

docker_build:
	$(MAKE) uv_requirements
	docker build -t $(IMAGE_REGISTRY)/duplocloud-ai-assistant:$(IMAGE_TAG) -f docker/Dockerfile .

docker_run:
	docker compose -f docker/docker-compose.yml --env-file .env -p duplocloud up -d 

docker_status:
	docker compose -f docker/docker-compose.yml --env-file .env -p duplocloud ps

docker_logs:
	docker compose -f docker/docker-compose.yml --env-file .env -p duplocloud logs
