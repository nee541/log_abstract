PY = python
# PFlags = -s time
DEFAULT_SRC = app/core.py
RECORD_FILE = out/files.txt
VENV = .venv
TRUE = true
FALSE = false

.SILENT: install uninstall 

run:
ifdef SRC
	$(PY) $(PFlags) $(SRC)
else ifdef src
	$(PY) $(PFlags) $(src)
else
	$(PY) $(PFlags) $(DEFAULT_SRC)
endif

install: setup.py
	python setup.py install --record $(RECORD_FILE)

# check if file exists, if so, return true, else return false
exists = $(if $(wildcard $(1)),$(TRUE),$(FALSE))

uninstall:
# ifneq ("$(wildcard $(RECORD_FILE))","")
ifeq ($(call exists,$(RECORD_FILE)),$(TRUE))
	xargs rm -rf < $(RECORD_FILE); 
	rm $(RECORD_FILE); 
endif
ifeq ($(call exists, build), $(TRUE))
	rm -rf build
endif
ifeq ($(call exists, dist), $(TRUE))
	rm -rf dist
endif
ifeq ($(call exists, *.egg-info), $(TRUE))
	rm -rf *.egg-info
endif
	echo "Uninstall complete"

init:
ifeq ($(call exists,$(VENV)),$(TRUE))
	python -m venv $(VENV)
else
	echo "Virtual environment already exists"
endif
ifeq ($(call exists,requirements.txt),$(TRUE))
	pip install -r requirements.txt
endif

test:
	nosetests tests
