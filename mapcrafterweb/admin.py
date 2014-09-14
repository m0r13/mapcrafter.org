from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from mapcrafterweb.models import Platform, Build

class PlatformAdmin(ModelAdmin):
    list_display = ["name", "download_dir"]

class BuildAdmin(ModelAdmin):
    list_display = ["date", "platform", "version", "filename"]

admin.site.register(Platform, PlatformAdmin)
admin.site.register(Build, BuildAdmin)
