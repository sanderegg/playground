.venv:
	@python3 --version
	python3 -m venv $@
	## upgrading tools to latest version in $(shell python3 --version)
	$@/bin/pip3 --quiet install --upgrade \
		pip~=23.1 \
		wheel \
		setuptools
	@$@/bin/pip3 list --verbose

devenv: .venv
	$</bin/pip3 --quiet install -r requirements.txt
	# Installing pre-commit hooks in current .git repo
	@$</bin/pre-commit install
	@echo "To activate the venv, execute 'source .venv/bin/activate'"

clean:
	-@rm -rf .venv