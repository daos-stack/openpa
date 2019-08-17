NAME    := openpa
SRC_EXT := gz
SOURCE   = https://github.com/pmodels/$(NAME)/archive/v$(VERSION).tar.$(SRC_EXT)

include packaging/Makefile_packaging.mk
