#!/usr/bin/env python2

import os
import sys
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mapcrafterweb_site.settings_dev")
import django
from django.utils import timezone
django.setup()

from mapcrafterweb.models import Package

def read_json(filename):
    data = json.loads(open(filename).read().decode("ascii", "ignore"))

    files = {}
    for request in data["requests"]:
        if request["data"].endswith(".zip") or request["data"].endswith(".deb"):
            if request["data"] in files:
                files[request["data"]] += request["hits"]
            else:
                files[request["data"]] = request["hits"]
    return files

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: %s [goaccess-json] [goaccess-packages-json]" % sys.argv[0]
        sys.exit(1)

    Package.objects.all().update(downloads_packages=0, downloads_total=0)

    for i in range(1, 3):
        files = read_json(sys.argv[i])
        for path, count in files.items():
            url = "//mapcrafter.org" + path
            package = None
            try:
                package = Package.objects.get(url=url)
            except Package.DoesNotExist:
                continue

            package.downloads_packages += count
            package.downloads_total += count
            package.save()

            print url, count
        print ""

