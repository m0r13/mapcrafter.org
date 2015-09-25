import json

from django.http.response import HttpResponse
from django.shortcuts import render

from mapcrafterweb.models import Package, BuildChannel
from zinnia.models.entry import Entry

# Create your views here.
def index(request):
    entries = Entry.objects.all()[:3]
    return render(request, "index.html", {"entries" : entries})

def update_download_stats(group):
    packages, total = 0, 0
    for package in group["packages"]:
        packages += package.downloads_packages
        total += package.downloads_total
    group["downloads_packages"] = packages
    group["downloads_total"] = total

def get_packages(channel):
    types = set()
    groups = []
    current_version = None
    current_group = dict(packages=[])
    
    packages = Package.objects.filter(channel=BuildChannel.get_channel(channel), visible=True)
    for package in packages:
        version = package.version
        if current_version is None:
            current_version = version
        if (package.type, package.arch) not in types:
            package.first = True
            types.add((package.type, package.arch))
        if current_version == version:
            current_group["packages"].append(package)
        else:
            current_group["version"] = current_version
            current_group["gitname"] = package.gitname
            update_download_stats(current_group)
            groups.append(current_group)
            current_version = version
            current_group = dict(packages=[package])
    if current_version is not None:
        current_group["version"] = current_version
        update_download_stats(current_group)
        groups.append(current_group)
    return groups

def downloads(request, channel):
    if channel is None:
        channel = "main"

    channels = []
    for c in BuildChannel.objects.all().order_by("name"):
        channels.append((c, c.name == channel))

    context = {}
    context["channels"] = channels
    context["package_groups"] = get_packages(channel)
    return render(request, "downloads.html", context)

def downloads_json(request):
    packages = []
    for package in Package.objects.filter(visible=True):
        packages.append({ "type" : package.type.name,
            "arch" : package.arch,
            "date" : str(package.date),
            "version" : package.version,
            "name" : package.filename,
            "url" : "http:" + package.url,
            #"downloads" : package.downloads,
        })
    content = json.dumps(packages, sort_keys=True, indent=4, separators=(",", ": "))
    return HttpResponse(content, "application/json")

