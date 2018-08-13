NAME    := openpa
VERSION := 1.0.4
RELEASE := 1
DIST    := .el7.centos
SRPM    := _topdir/SRPMS/$(NAME)-$(VERSION)-$(RELEASE)$(DIST).src.rpm
RPMS    := _topdir/RPMS/x86_64/$(NAME)-$(VERSION)-$(RELEASE)$(DIST).x86_64.rpm           \
	   _topdir/RPMS/x86_64/$(NAME)-devel-$(VERSION)-$(RELEASE)$(DIST).x86_64.rpm     \
	   _topdir/RPMS/x86_64/$(NAME)-debuginfo-$(VERSION)-$(RELEASE)$(DIST).x86_64.rpm
SPEC    := $(NAME).spec
SOURCE  := https://trac.mpich.org/projects/openpa/raw-attachment/wiki/Downloads/$(NAME)-$(VERSION).tar.gz
TARGETS := $(RPMS) $(SRPM)

all: $(TARGETS)

%/:
	mkdir -p $@

_topdir/SOURCES/%: % | _topdir/SOURCES/
	ln $< $@

$(NAME)-$(VERSION).tar.gz:
	curl -O '$(SOURCE)'

# see https://stackoverflow.com/questions/2973445/ for why we subst
# the "rpm" for "%" to effectively turn this into a multiple matching
# target pattern rule
$(subst rpm,%,$(RPMS)): $(SPEC) _topdir/SOURCES/$(NAME)-$(VERSION).tar.gz
	rpmbuild -bb --define "%_topdir $$PWD/_topdir" $(SPEC)

$(SRPM): $(SPEC)
	rpmbuild -bs --define "%_topdir $$PWD/_topdir" $(SPEC)

srpm: $(SRPM)

rpms: $(RPMS)

ls: $(TARGETS)
	ls -ld $^

mockbuild: $(SRPM)
	mock $<
