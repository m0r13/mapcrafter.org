from django.db.models.base import Model
from django.db.models.fields import CharField, DateTimeField, IntegerField
from django.utils import timezone
from django.db.models.fields.related import ForeignKey
import re

REGEX_VERSION = re.compile("(?P<major>\d)\.(?P<minor>\d)(\.(?P<build>\d))?(-(?P<commit>\d+))?")

class PackageType(Model):
    class Meta:
        verbose_name = "package type"
        verbose_name_plural = "package types"
    
    name = CharField(max_length=255, verbose_name="name")
    verbose_name = CharField(max_length=255, verbose_name="verbose name")
    
    def __unicode__(self):
        return self.name

class Package(Model):
    class Meta:
        verbose_name = "package"
        verbose_name_plural = "packages"
        
        ordering = ["-version_major", "-version_minor", "-version_build", "-version_commit", "-type", "-arch"]
    
    ARCH_32_BIT = "32"
    ARCH_64_BIT = "64"
    ARCHS = (
        (ARCH_32_BIT, "32 Bit"),
        (ARCH_64_BIT, "64 Bit"),
    )
    
    type = ForeignKey(PackageType, verbose_name="type")
    arch = CharField(choices=ARCHS, max_length=255, verbose_name="architecture")
    date = DateTimeField(default=timezone.now, verbose_name="date")
    # version of built package
    # for example version 1.5.1-2: major=1, minor=5, build=1, commit=2
    version_major = IntegerField(verbose_name="version major")
    version_minor = IntegerField(verbose_name="version minor")
    version_build = IntegerField(verbose_name="version build")
    version_commit = IntegerField(verbose_name="version commit")
    url = CharField(max_length=255, verbose_name="url")
    downloads = IntegerField(verbose_name="downloads")
    
    @property
    def arch_name(self):
        if self.arch == Package.ARCH_32_BIT:
            return "32 Bit"
        if self.arch == Package.ARCH_64_BIT:
            return "64 Bit"
        return "Unknown architecture"
    
    def get_version(self):
        version = "%d.%d" % (self.version_major, self.version_minor)
        if self.version_build != 0:
            version += ".%s" % self.version_build
        if self.version_commit != 0:
            version += "-%d" % self.version_commit 
        return version
    
    def set_version(self, value):
        match = REGEX_VERSION.match(value)
        if match is None:
            raise ValueError(value)
        self.version_major = int(match.group("major"))
        self.version_minor = int(match.group("minor"))
        if match.group("build"):
            self.version_build = int(match.group("build"))
        else:
            self.version_build = 0
        if match.group("commit"):
            self.version_commit = int(match.group("commit"))
        else:
            self.version_commit = 0
    
    version = property(get_version, set_version)
    
    @property
    def filename(self):
        if not "/" in self.url:
            return self.url
        return self.url.split("/")[-1]
    
    def __unicode__(self):
        return "Build v.%s %s%s" % (self.version, self.type, self.arch)
