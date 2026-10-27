DEPENDENCIES=requirements.txt
PJ_MAIN=pac-man.py
PJ_MAIN_PACK=pac_man_build.py
CONFIG=config.json
ENV_NAME=pacmana
PIP_VENV=pacmana/bin/pip

build:
	python3 -m build

install:
	python3 -m venv ${ENV_NAME}
	${PIP_VENV} install mypy
	${PIP_VENV} install -r ${DEPENDENCIES}

install_packages:
	python3 -m venv ${ENV_NAME}
	${PIP_VENV} install mypy  
	${PIP_VENV} install -r ${DEPENDENCIES}
	${PIP_VENV} install pacman-0.0.1-py3-none-any.whl

run:
	python3 ${PJ_MAIN} ${CONFIG}

run_pack:
	python3 ${PJ_MAIN_PACK} ${CONFIG}

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