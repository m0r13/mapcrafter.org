from django.shortcuts import render

# Create your views here.

def index(request, _):
    return render(request, "index.html")
