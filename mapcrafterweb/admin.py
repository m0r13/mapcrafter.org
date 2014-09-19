from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from mapcrafterweb.models import PackageType, Package
from django.utils.safestring import mark_safe

class PackageTypeAdmin(ModelAdmin):
    list_display = ["name", "verbose_name"]

def url(package):
    package_url = package.url
    return mark_safe("<a href='%s'>%s</a>" % (package_url, package_url))

class PackageAdmin(ModelAdmin):
    list_display = ["type", "arch", "date", "version", url, "downloads"]

admin.site.register(PackageType, PackageTypeAdmin)
admin.site.register(Package, PackageAdmin)
