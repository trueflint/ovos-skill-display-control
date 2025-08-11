PROJECT := ovos-skill-display-control
ARCHIVE_DIR := /home/ovos/skill-work/archives

PROJECT_UNDERSCORES := $(subst -,_,$(PROJECT))

install:
	pip install .

clean:
	rm -rf build $(PROJECT_UNDERSCORES).egg-info translations/*
	find . -name '*~' -delete

uninstall:
	pip uninstall -y $(PROJECT)

reload_skills:
	systemctl --user restart ovos-core

reinstall: uninstall clean install

retry: reinstall reload_skills

archive: clean
	tar zcvf $(ARCHIVE_DIR)/$(PROJECT).tgz -C .. $(PROJECT)

.PHONY: install uninstall reinstall clean reload_skills retry archive
