.venv:
	@python3 --version
	uv venv $@
	## upgrading tools to latest version in $(shell python3 --version)
	@uv pip list --verbose

devenv: .venv
	uv pip install -r requirements.txt
	# Installing pre-commit hooks in current .git repo
	@$</bin/pre-commit install
	@echo "To activate the venv, execute 'source .venv/bin/activate'"

clean:
	-@rm -rf .venv