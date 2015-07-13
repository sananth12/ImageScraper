#!/bin/sh
set -e


PACKAGE=ImageScraper
PACKAGE_ROOT="./$PACKAGE"

echo "Building $PACKAGE..."


# Sets the version in the control file.
VERSION=`python -c "print [r for r in open('ImageScraper.control', 'r').read().split('\n') if 'Version' in r][0].split(':')[-1].strip()"`
ARCH=all


echo "Removing previous files..."
rm -rf $PACKAGE_ROOT
rm -rf $PACKAGE.deb


mkdir -p $PACKAGE_ROOT
cd $PACKAGE_ROOT


echo "Copying files..."
mkdir -p ./tmp/$PACKAGE
pwd
cp -r ../../{setup.py,image_scraper,requirements.txt} ./tmp/$PACKAGE


echo "Copying auxiliary files..."
mkdir -p ./DEBIAN
cp ../$PACKAGE.control ./DEBIAN/control
cp ../$PACKAGE.postinst ./DEBIAN/postinst
chmod 755 ./DEBIAN/postinst


echo "Building deb..."
cd ..
dpkg-deb --build ./$PACKAGE_ROOT
FILE=${PACKAGE}_${VERSION}_${ARCH}.deb
mv $PACKAGE.deb $FILE


echo "Cleaning up..."
rm -rf $PACKAGE_ROOT