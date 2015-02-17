from django.http.response import HttpResponse
from django.shortcuts import render
from django.conf import settings
from mapcrafterweb.models import Package, PackageType
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return render(request, "index.html")

def get_packages(package_type=None):
    groups = []
    current_version = None
    current_group = dict(packages=[])
    
    packages = Package.objects.filter(visible=True)
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
    context["packages"] = Package.objects.filter(visible=True)
    context["group_win"] = get_packages()
    return render(request, "downloads.html", context)

class JsonResponse(HttpResponse):
    def __init__(self, data):
        super(JsonResponse, self).__init__(json.dumps(data, sort_keys=True, indent=4, separators=(",", ": ")))
        self["Content-Type"] = "application/json"

class JsonErrorResponse(JsonResponse):
    def __init__(self, error):
        super(JsonErrorResponse, self).__init__({"status" : "error", "error" : error})

def api_get_packages(request):
    secret = getattr(settings, "API_SECRET", None)
    if not secret:
        return JsonErrorResponse("API secret is not set! API disabled!")
    packages = []
    for package in Package.objects.filter(visible=True):
        packages.append({
            "type" : package.type.name,
            "arch" : package.arch,
            "date" : str(package.date),
            "version" : package.version,
            "name" : package.filename,
            "url" : "http:" + package.url,
            "downloads" : package.downloads,
        })
    return JsonResponse({"packages" : packages})

@csrf_exempt
def api_update_package_downloads(request):
    secret = getattr(settings, "API_SECRET", None)
    if not secret:
        return JsonErrorResponse("API secret is not set! API disabled!")
    if request.method != "POST":
        return JsonErrorResponse("Invalid request method! Must be post!")
    data = {}
    try:
        data = json.loads(request.body)
    except ValueError, e:
        return JsonErrorResponse("Unable to parse json data!")
    if data.get("secret") != secret:
        return JsonErrorResponse("Invalid secret!")
    #packages = [
    #    {
    #        "type" : "deb",
    #        "arch" : "64",
    #        "version" : "1.5.2",
    #        "downloads" : 42,
    #    }
    #]
    updated = 0
    for package in data.get("packages", []):
        package_type = None
        try:
            package_type = PackageType.objects.get(name=package.get("type", ""))
        except PackageType.DoesNotExist:
            continue
        p = Package()
        p.version = package.get("version", "0.0.0")
        try:
            p = Package.objects.get(
                type=package_type, arch=package.get("arch", ""),
                version_major=p.version_major, version_minor=p.version_minor,
                version_build=p.version_build, version_commit=p.version_commit
            )
            if not "downloads" in package:
                continue
            try:
                p.downloads = int(package.get("downloads", 0))
                p.save()
                updated += 1
            except ValueError:
                continue
        except Package.DoesNotExist:
            continue
    return JsonResponse({"status" : "success", "message" : "Updated %d packages." % updated})
