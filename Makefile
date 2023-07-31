.PHONY: download clean

BASEURL ?= https://archriscv.felixc.at/images/
RELEASE_REGEX ?= ^.*href="archriscv-([0-9-]+).tar.zst".*$$

define get_release
	curl '$(BASEURL)' 2> /dev/null | \
		grep -E '$(RELEASE_REGEX)' | \
		tail -n 1 | \
		sed -E 's/$(RELEASE_REGEX)/\1/'
endef

RELEASE ?= $(shell $(get_release))
ARCHIVE ?= archriscv-$(RELEASE).tar.zst

download: $(ARCHIVE)
	@echo "RootFS archive $(ARCHIVE) succefully downloaded"

$(ARCHIVE):
	@curl --location --remote-name "$(BASEURL)/$(ARCHIVE)"

clean:
	rm *.tar.zst
