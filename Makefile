VERSION=1.0.3
RELEASE=2015-03-29

.PHONY: naemon-core naemon-livestatus

all: naemon-core naemon-livestatus
	@echo "***************************************"
	@echo "Naemon build complete"
	@echo ""
	@echo "continue with"
	@echo "make deb"
	@echo ""


naemon-core:
	cd naemon-core && make

naemon-livestatus:
	cd naemon-livestatus && make CPPFLAGS="$$CPPFLAGS -I$$(pwd)/../naemon-core/src"

clean:
	-cd naemon-core && make clean
	-cd naemon-livestatus && make clean
	rm -rf naemon-${VERSION} naemon-${VERSION}.tar.gz

install:
	cd naemon-core && make install
	cd naemon-livestatus && make install

deb:
	debuild -i -us -uc -b
