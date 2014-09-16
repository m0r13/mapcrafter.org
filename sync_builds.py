#!/usr/bin/env python2

import os
import re
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mapcrafterweb_site.settings_dev")
import django
django.setup()

from mapcrafterweb.models import Package, PackageType

REGEX_VERSION = "(?P<version>\d\.\d(\.\d)?(-\d+)?)"
REGEX_DEB_PACKAGE = re.compile("mapcrafter_%s_(?P<arch>i386|amd64)\.deb" % REGEX_VERSION)
REGEX_WIN_PACKAGE = re.compile("mapcrafter_%s_(?P<arch>win32|win64)\.zip" % REGEX_VERSION)

if __name__ == "__main__":    
    if len(sys.argv) < 2:
        print "Usage: %s [dist_dir]" % sys.argv[0]
        sys.exit(1)
    
    dist_dir = sys.argv[1]
    
    type_win, _ = PackageType.objects.get_or_create(name="win")
    type_deb, _ = PackageType.objects.get_or_create(name="deb")
    packages = []

    for filename in os.listdir(os.path.join(dist_dir, "debian", "packages")):
        match = REGEX_DEB_PACKAGE.match(filename)
        if match is None:
            print "Warning: Unknown package '%s'." % filename
            continue
        
        arch = Package.ARCH_32_BIT
        if match.group("arch") == "amd64":
            arch= Package.ARCH_64_BIT
        package = Package()
        package.type = type_deb
        package.arch = arch
        package.version = match.group("version")
        package.url = "//mapcrafter.org/debian/packages/%s" % filename
        packages.append(package)
    
    for filename in os.listdir(os.path.join(dist_dir, "windows")):
        match = REGEX_WIN_PACKAGE.match(filename)
        if match is None:
            print "Warning: Unknown package '%s'." % filename
            continue
        
        arch = Package.ARCH_32_BIT
        if match.group("arch") == "amd64":
            arch= Package.ARCH_64_BIT
        package = Package()
        package.type = type_win
        package.arch = arch
        package.version = match.group("version")
        package.url = "//mapcrafter.org/windows/%s" % filename
        packages.append(package)
    
    for package in packages:
        try:
            Package.objects.get(
                type=package.type, arch=package.arch,
                version_major=package.version_major, version_minor=package.version_minor,
                version_build=package.version_build, version_commit=package.version_commit)
        except Package.DoesNotExist:
            package.save()