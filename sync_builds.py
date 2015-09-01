#!/usr/bin/env python2

import datetime
import glob
import os
import pytz
import sys
import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mapcrafterweb_site.settings_dev")
import django
from django.utils import timezone
django.setup()

from mapcrafterweb.models import Package, PackageType, BuildChannel

REGEX_VERSION = "(?P<version>\d\.\d(?:\.\d)?(?:~\d+)?(?:~[a-z0-9]+)?)"
REGEX_DEB_PACKAGE = re.compile(".*dist/packages/(?P<distro>[a-z]+)/(?P<release>[a-z]+)/(?P<channel>[a-z]+)/mapcrafter_%s-1_(?P<arch>i386|amd64)\.deb" % REGEX_VERSION)
REGEX_WIN_PACKAGE = re.compile(".*dist/windows/(?P<channel>[a-z]+)/mapcrafter_%s_(?P<arch>win32|win64)\.zip" % REGEX_VERSION)

def timestamp_to_datetime(timestamp):
    local_tz = timezone.get_current_timezone()
    utc_dt = datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    return local_tz.normalize(utc_dt.astimezone(local_tz))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s [dist_dir]" % sys.argv[0]
        sys.exit(1)
    
    dist_dir = sys.argv[1]
    
    files = glob.glob(os.path.join(dist_dir, "packages/*/*/*/*.deb"))
    files += glob.glob(os.path.join(dist_dir, "windows/*/*.zip"))
    packages = set()
    for path in files:
        package = Package()
        package.date = timestamp_to_datetime(os.stat(path).st_mtime)
        package.url = "//mapcrafter.org/%s" % os.path.relpath(path, dist_dir)
        package.downloads = 0
        package.visible = True

        match_deb = REGEX_DEB_PACKAGE.match(path)
        match_win = REGEX_WIN_PACKAGE.match(path)
        if match_deb is not None:
            package.channel = BuildChannel.get_channel(match_deb.group("channel"))
            package.type = PackageType.get_deb_type(match_deb.group("distro"), match_deb.group("release"))
            package.arch = {"i386" : Package.ARCH_32_BIT, "amd64" : Package.ARCH_64_BIT}[match_deb.group("arch")]
            package.version = match_deb.group("version")
        elif match_win is not None:
            package.channel = BuildChannel.get_channel(match_win.group("channel"))
            package.type = PackageType.get_win_type()
            package.arch = {"win32" : Package.ARCH_32_BIT, "win64" : Package.ARCH_64_BIT}[match_win.group("arch")]
            package.version = match_win.group("version")
        else:
            print "### Warning: Unknown package '%s'!" % path
            continue

        try:
            p = Package.objects.get(
                channel=package.channel, type=package.type, arch=package.arch,
                version_major=package.version_major, version_minor=package.version_minor,
                version_build=package.version_build, version_commit=package.version_commit, version_githash=package.version_githash)
            if (p.date, p.url) != (package.date, package.url):
                p.date = package.date
                p.url = package.url
                p.save()
            print "Already have package: %s" % package
            packages.add(p.multi_key)
        except Package.DoesNotExist:
            print "New package: %s" % package
            package.save()
            packages.add(package.multi_key)

    for package in Package.objects.all():
        if not package.multi_key in packages:
            print "Removed package: %s" % package
            package.delete()

