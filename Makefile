DEPENDENCIES=requirements.txt
PJ_MAIN=pac-man.py
PJ_MAIN_PACK=pac_man_build.py
CONFIG=config.json
ENV_NAME=pacmana
PIP_VENV=pacmana/bin/pip
EXE_FILE=pac-man.exe
DIR_EXE=dist/pac-man

build:
	python3 -m build

install:
	python3 -m venv ${ENV_NAME}
	${PIP_VENV} install mypy
	${PIP_VENV} install -r ${DEPENDENCIES}

create_exe:
	pyinstaller pac-man.py --onedir --contents-directory . --add-data "config.json:." --add-data "src/interface/assets:src/interface/assets" --noconfirm

run_exe:
	cd $(DIR_EXE) && ./$(EXE_FILE) ./$(CONFIG)

run:
	python ${PJ_MAIN} ${CONFIG}

debug:
	python3 -m pdb ${PJ_MAIN} ${CONFIG}

clean:
	rm -rf ${ENV_NAME}
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name ".mypy_cache" -exec rm -rf {} +
	find . -name "${FILENAME}" -exec rm -rf {} +

lint:
	flake8 . \
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint_strict:
	flake8 --exclude=$(ENV_NAME) . ;\
	mypy --strict .