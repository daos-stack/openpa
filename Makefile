NAME    := openpa
VERSION := 1.0.4
RELEASE := 3
DIST    := $(shell rpm --eval %{?dist})
SRPM    := _topdir/SRPMS/$(NAME)-$(VERSION)-$(RELEASE)$(DIST).src.rpm
RPMS    := _topdir/RPMS/x86_64/$(NAME)-$(VERSION)-$(RELEASE)$(DIST).x86_64.rpm           \
	   _topdir/RPMS/x86_64/$(NAME)-devel-$(VERSION)-$(RELEASE)$(DIST).x86_64.rpm     \
	   _topdir/RPMS/x86_64/$(NAME)-debuginfo-$(VERSION)-$(RELEASE)$(DIST).x86_64.rpm
SPEC    := $(NAME).spec
SRC_EXT := gz
SOURCE  := https://github.com/pmodels/$(NAME)/archive/v$(VERSION).tar.$(SRC_EXT)
SOURCES := _topdir/SOURCES/v$(VERSION).tar.$(SRC_EXT)
TARGETS := $(RPMS) $(SRPM)

# need to use -k because the certificate store is not properly
# configured on SLES 12.3 containers
ifeq ($(shell lsb_release -sir),SUSE 12.3)
  CURL_INSECURE := -k
endif

all: $(TARGETS)

%/:
	mkdir -p $@

_topdir/SOURCES/%: % | _topdir/SOURCES/
	rm -f $@
	ln $< $@

v$(VERSION).tar.$(SRC_EXT):
	curl $(CURL_INSECURE) -f -L -O '$(SOURCE)'

# see https://stackoverflow.com/questions/2973445/ for why we subst
# the "rpm" for "%" to effectively turn this into a multiple matching
# target pattern rule
$(subst rpm,%,$(RPMS)): $(SPEC) $(SOURCES)
	rpmbuild -bb --define "%_topdir $$PWD/_topdir" $(SPEC)

$(SRPM): $(SPEC) $(SOURCES)
	rpmbuild -bs --define "%_topdir $$PWD/_topdir" $(SPEC)

srpm: $(SRPM)

$(RPMS): Makefile

rpms: $(RPMS)

ls: $(TARGETS)
	ls -ld $^

mockbuild: $(SRPM) Makefile
	mock $<

rpmlint: $(SPEC)
	rpmlint $<

.PHONY: srpm rpms ls mockbuild rpmlint FORCE
