SHELL := /bin/bash

MAIN = fly_in.py
CONFIG_FILE = 

EXECUTE = python3
MUTE = > /dev/null

PIP = -m pip install

VENV = -m venv venv

FLAKE = -m flake8 .

MYPY = -m mypy .
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
STRICT = --strict

DEBUG = -m pdb

FIND = find .
PYCACHE = -type d -name '__pycache__'
MYPY_CACHE = -type d -name '.mypy_cache'
VENV_DIR = -type d -name 'venv'
REMOVE = -exec rm -rf {} +


.SILENT:

all: install

install:
	echo 'Installing dependencies...'
	$(FIND) $(VENV_DIR) $(REMOVE) && \
	$(EXECUTE) $(VENV) && \
	source venv/bin/activate && \
	$(EXECUTE) $(PIP) --upgrade pip $(MUTE) && \
	$(EXECUTE) $(PIP) pygame-ce flake8 mypy $(MUTE)
	echo 'Done.'
	echo ''

run $(args): install
	source venv/bin/activate && \
	$(EXECUTE) $(MAIN) $(filter-out run,$(MAKECMDGOALS))

debug: install
	echo 'Running in Debug mode'
	echo ''
	source venv/bin/activate && \
	$(EXECUTE) $(DEBUG) $(MAIN) $(CONFIG_FILE)

clean:
	echo 'Cleaning caches and temporary files...'
	$(FIND) $(PYCACHE) $(REMOVE)
	$(FIND) $(MYPY_CACHE) $(REMOVE)
	$(FIND) $(VENV_DIR) $(REMOVE)
	echo 'Done.'
	echo ''

lint: install
	echo 'Running flake8...'
	source venv/bin/activate && \
	$(EXECUTE) $(FLAKE) --exclude venv/
	echo ''
	echo 'Running mypy...'
	source venv/bin/activate && \
	$(EXECUTE) $(MYPY) $(MYPY_FLAGS)
	echo 'Done.'
	echo ''

lint-strict: install
	echo 'Running flake8...'
	source venv/bin/activate && \
	$(EXECUTE) $(FLAKE) --exclude venv/
	echo ''
	echo 'Running mypy strict...'
	source venv/bin/activate && \
	$(EXECUTE) $(MYPY) $(STRICT)
	echo 'Done.'
	echo ''

%:
	@: