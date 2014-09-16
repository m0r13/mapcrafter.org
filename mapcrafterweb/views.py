from django.shortcuts import render
from mapcrafterweb.models import Package

# Create your views here.

def index(request):
    return render(request, "index.html")

def get_packages(package_type=None):
    groups = []
    current_version = None
    current_group = dict(packages=[])
    
    packages = Package.objects.all()
    if package_type is not None:
        packages = packages.filter(type=package_type)
    for package in packages:
        version = package.version
        if current_version is None:
            current_version = version
        if current_version == version:
            current_group["packages"].append(package)
        else:
            current_group["version"] = current_version
            groups.append(current_group)
            current_version = version
            current_group = dict(packages=[package])
    if current_version is not None:
        current_group["version"] = current_version
        groups.append(current_group)
    return groups

def downloads(request):
    context = {}
    context["packages"] = Package.objects.all()
    context["group_win"] = get_packages()
    return render(request, "downloads.html", context)
