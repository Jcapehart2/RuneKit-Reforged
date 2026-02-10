LINUXDEPLOY ?= linuxdeploy-$(shell uname -m).AppImage

dev: runekit/_resources.py

runekit/_resources.py: resources.qrc $(wildcard runekit/**/*.js) $(wildcard runekit/**/*.png)
	pyside6-rcc $< -o $@

# Sdist

dist/runekit.tar.gz: main.py poetry.lock runekit/_resources.py $(wildcard runekit/**/*)
	poetry build -f sdist
	cd dist; cp runekit-*.tar.gz runekit.tar.gz

# Mac

dist/RuneKit.app: RuneKit.spec main.py poetry.lock runekit/_resources.py $(wildcard runekit/**/*)
	pyinstaller --noconfirm $<

dist/RuneKit.app.zip: dist/RuneKit.app
	# Use ditto on macOS to preserve symlinks (critical for PyInstaller 6.0+ bundles)
	# PyInstaller uses symlinks to avoid duplicating frameworks - if symlinks aren't preserved,
	# the bundle can expand from ~300MB to 3GB+ due to framework duplication
	cd dist; ditto -c -k --sequesterRsrc --keepParent RuneKit.app RuneKit.app.zip

# AppImage

build/python3.11.AppImage:
	mkdir build || true
	wget https://github.com/niess/python-appimage/releases/download/python3.11/python3.11.14-cp311-cp311-manylinux2014_x86_64.AppImage -O "$@"
	chmod +x "$@"

build/appdir: build/python3.11.AppImage
	$< --appimage-extract
	mv squashfs-root build/appdir

dist/RuneKit.AppImage: dist/runekit.tar.gz build/appdir deploy/runekit-appimage.sh
	build/appdir/usr/bin/python3 -m pip install dist/runekit.tar.gz
	rm $(wildcard build/appdir/*.desktop) $(wildcard build/appdir/usr/share/applications/*.desktop) $(wildcard build/appdir/usr/share/metainfo/*)
	cp deploy/RuneKit.desktop build/appdir/
	cp deploy/RuneKit.desktop build/appdir/usr/share/applications/
	cp deploy/de.cupco.runekit.metainfo.xml build/appdir/usr/share/metainfo/
	cp deploy/runekit-appimage.sh build/appdir/AppRun
	$(LINUXDEPLOY) --appdir build/appdir --output appimage
	cp RuneKit-*.AppImage "$@"

.PHONY: dev
