#!/usr/bin/env python2

import datetime
import pytz
import os
import re
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mapcrafterweb_site.settings_dev")
import django
from django.utils import timezone
django.setup()

from mapcrafterweb.models import Package, PackageType

REGEX_VERSION = "(?P<version>\d\.\d(\.\d)?(-\d+)?)"
REGEX_DEB_PACKAGE = re.compile("mapcrafter_%s_(?P<arch>i386|amd64)\.deb" % REGEX_VERSION)
REGEX_WIN_PACKAGE = re.compile("mapcrafter_%s_(?P<arch>win32|win64)\.zip" % REGEX_VERSION)


def timestamp_to_datetime(timestamp):
    local_tz = timezone.get_current_timezone()
    utc_dt = datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    return local_tz.normalize(utc_dt.astimezone(local_tz))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s [dist_dir]" % sys.argv[0]
        sys.exit(1)
    
    dist_dir = sys.argv[1]
    
    type_win, _ = PackageType.objects.get_or_create(name="win")
    type_deb, _ = PackageType.objects.get_or_create(name="deb")
    packages = {}

    for filename in os.listdir(os.path.join(dist_dir, "debian", "packages")):
        match = REGEX_DEB_PACKAGE.match(filename)
        if match is None:
            print "Warning: Unknown package '%s'." % filename
            continue
        
        arch = Package.ARCH_32_BIT
        if match.group("arch") == "amd64":
            arch= Package.ARCH_64_BIT
        
        timestamp = os.stat(os.path.join(dist_dir, "debian", "packages", filename)).st_mtime
        date = timestamp_to_datetime(timestamp)
        
        package = Package()
        package.type = type_deb
        package.arch = arch
        package.date = date
        package.date = timestamp_to_datetime(timestamp)
        package.version = match.group("version")
        package.url = "//mapcrafter.org/debian/packages/%s" % filename
        package.downloads = 0
        package.visible = False
        type_arch_version = package.type, package.arch, package.version
        packages[type_arch_version] = package
    
    for filename in os.listdir(os.path.join(dist_dir, "windows")):
        match = REGEX_WIN_PACKAGE.match(filename)
        if match is None:
            print "Warning: Unknown package '%s'." % filename
            continue
        
        arch = Package.ARCH_32_BIT
        if match.group("arch") == "win64":
            arch= Package.ARCH_64_BIT
        
        timestamp = os.stat(os.path.join(dist_dir, "windows", filename)).st_mtime
        date = timestamp_to_datetime(timestamp)
        
        package = Package()
        package.type = type_win
        package.arch = arch
        package.date = date
        package.version = match.group("version")
        package.url = "//mapcrafter.org/windows/%s" % filename
        package.downloads = 0
        package.visible = False
        type_arch_version = package.type, package.arch, package.version
        packages[type_arch_version] = package
    
    for type_arch_version, package in packages.items():
        try:
            p = Package.objects.get(
                type=package.type, arch=package.arch,
                version_major=package.version_major, version_minor=package.version_minor,
                version_build=package.version_build, version_commit=package.version_commit)
            p.date = package.date
            p.url = package.url
            p.save()
        except Package.DoesNotExist:
            print "New package: %s" % package
            package.save()

    for package in Package.objects.all():
        type_arch_version = package.type, package.arch, package.version
        if not type_arch_version in packages:
            print "Removed package: %s" % package
            package.delete()
