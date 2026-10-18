DEPENDENCIES=requirements.txt
PJ_MAIN=pac-man.py
CONFIG=config.json
ENV_NAME=pacman
PIP_VENV=pacman/bin/pip

install:
	python3 -m venv ${ENV_NAME}
	${PIP_VENV} install mypy
	${PIP_VENV} install -r ${DEPENDENCIES}

run:
	python3 ${PJ_MAIN} ${CONFIG}

debug:
	python3 -m pdb ${PJ_MAIN} ${CONFIG}

clean:
	rm -rf ${ENV_NAME}
	find . -name "__pycache__" -exec rm -rf {} \;
	find . -name ".mypy_cache" -exec rm -rf {} \;
	find . -name "${FILENAME}" -exec rm -rf {} \;

lint:
	flake8 . && mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint_strict:
	flake8 && mypy . --strict