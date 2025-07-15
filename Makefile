PROJECT := ovos-skill-display-control
ARCHIVE_DIR := /home/ovos/skill-work/archives

PROJECT_UNDERSCORES := $(subst -,_,$(PROJECT))

install:
	pip install .

uninstall:
	pip uninstall $(PROJECT)

reinstall: uninstall install

clean:
	rm -rf build $(PROJECT_UNDERSCORES).egg-info translations/*
	find . -name '*~' -delete

archive: clean
	tar zcvf $(ARCHIVE_DIR)/$(PROJECT).tgz -C .. $(PROJECT)
