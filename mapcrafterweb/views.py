from django.shortcuts import render
from mapcrafterweb.models import Package

# Create your views here.

def index(request, _):
    return render(request, "index.html")

def downloads(request):
    context = {}
    context["packages"] = Package.objects.all()
    return render(request, "downloads.html", context)
