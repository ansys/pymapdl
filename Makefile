# Simple makefile to simplify repetitive build env management tasks under posix

CODESPELL_DIRS ?= ./
CODESPELL_SKIP ?= "*.pyc,*.txt,*.gif,*.png,*.jpg,*.js,*.html,*.doctree,*.ttf,*.woff,*.woff2,*.eot,*.mp4,*.inv,*.pickle,*.ipynb,flycheck*,./.git/*,./.hypothesis/*,*.yml,./doc/build/*,./doc/images/*,./dist/*,*~,.hypothesis*,./doc/source/examples/*,*cover,*.dat,*.mac,\#*,build,./docker/mapdl/v*,./factory/*,./ansys/mapdl/core/mapdl_functions.py,PKG-INFO,*.mypy_cache/*,./docker/mapdl/*"
CODESPELL_IGNORE ?= "ignore_words.txt"

all: doctest

doctest: codespell

codespell:
	@echo "Running codespell"
	@codespell $(CODESPELL_DIRS) -S $(CODESPELL_SKIP) -I $(CODESPELL_IGNORE)

pydocstyle:
	@echo "Running pydocstyle"
	@pydocstyle ansys.mapdl

doctest-modules:
	@echo "Runnnig module doctesting"
	pytest -v --doctest-modules ansys.mapdl

coverage:
	@echo "Running coverage"
	@pytest -v --cov ansys.mapdl

coverage-xml:
	@echo "Reporting XML coverage"
	@pytest -v --cov ansys.mapdl --cov-report xml

coverage-html:
	@echo "Reporting HTML coverage"
	@pytest -v --cov ansys.mapdl --cov-report html

flake8:
	@echo "Running flake8"
	@flake8 .
