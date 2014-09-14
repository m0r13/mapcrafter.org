from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from mapcrafterweb.models import Platform, Build

class PlatformAdmin(ModelAdmin):
    list_display = ["name"]

class BuildAdmin(ModelAdmin):
    list_display = ["platform", "version", "filename"]

admin.site.register(Platform, PlatformAdmin)
admin.site.register(Build, BuildAdmin)
