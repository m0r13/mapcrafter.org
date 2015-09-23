from django.db.models.base import Model
from django.db.models.fields import CharField, DateTimeField, IntegerField, BooleanField
from django.utils import timezone
from django.db.models.fields.related import ForeignKey
import re

REGEX_VERSION = re.compile("(?P<major>\d)\.(?P<minor>\d)(\.(?P<build>\d))?(~(?P<commit>\d+))?(~(?P<githash>[a-z0-9]+))?")

class PackageType(Model):
    class Meta:
        verbose_name = "package type"
        verbose_name_plural = "package types"

        ordering = ["name"]
    
    name = CharField(max_length=255, verbose_name="name")
    verbose_name = CharField(max_length=255, verbose_name="verbose name")

    @staticmethod
    def get_win_type():
        package_type, created = PackageType.objects.get_or_create(name="win")
        if created:
            package_type.verbose_name = "Windows Package"
            package_type.save()
        return package_type

    @staticmethod
    def get_deb_type(distro, release):
        name = "deb_%s_%s" % (distro, release)
        package_type, created = PackageType.objects.get_or_create(name=name)
        if created:
            verbose_name = ("%s package (%s)" % (distro, release)).title()
            package_type.verbose_name = verbose_name
            package_type.save()
        return package_type

    def __unicode__(self):
        return self.verbose_name

class BuildChannel(Model):
    class Meta:
        verbose_name = "build channel"
        verbose_name_plural = "build channels"

        ordering = ["name"]

    name = CharField(max_length=255, verbose_name="name")
    verbose_name = CharField(max_length=255, verbose_name="verbose name")

    @staticmethod
    def get_channel(channel):
        channel, created = BuildChannel.objects.get_or_create(name=channel)
        if created:
            channel.verbose_name = channel.name.title()
            channel.save()
        return channel

    def __unicode__(self):
        return self.verbose_name

class Package(Model):
    class Meta:
        verbose_name = "package"
        verbose_name_plural = "packages"
        
        ordering = ["-version_major", "-version_minor", "-version_build", "-version_commit", "-type", "-arch", "-channel"]
        unique_together = (("channel", "type", "arch", "version_major", "version_minor", "version_build", "version_commit", "version_githash"))
    
    ARCH_32_BIT = "32"
    ARCH_64_BIT = "64"
    ARCHS = (
        (ARCH_32_BIT, "32 Bit"),
        (ARCH_64_BIT, "64 Bit"),
    )
    
    channel = ForeignKey(BuildChannel, verbose_name="build channel")
    type = ForeignKey(PackageType, verbose_name="type")
    arch = CharField(choices=ARCHS, max_length=255, verbose_name="architecture")
    date = DateTimeField(default=timezone.now, verbose_name="date")
    # version of built package
    # for example version 1.5.1~2~abcdef12: major=1, minor=5, build=1, commit=2, githash=abcdef12
    version_major = IntegerField(verbose_name="version major")
    version_minor = IntegerField(verbose_name="version minor")
    version_build = IntegerField(default=0, verbose_name="version build")
    version_commit = IntegerField(default=0, verbose_name="version commit")
    version_githash = CharField(max_length=255, default="", verbose_name="version githash")
    url = CharField(max_length=255, verbose_name="url")
    downloads_packages = IntegerField(default=0, verbose_name="downloads packages")
    downloads_total = IntegerField(default=0, verbose_name="downloads total")
    visible = BooleanField(default=True, verbose_name="visible")

    @property
    def multi_key(self):
        return self.channel.name, self.type.name, self.arch, self.version
    
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
            version += "~%d" % self.version_commit 
        if self.version_githash:
            version += "~%s" % self.version_githash
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
        if match.group("githash"):
            self.version_githash = match.group("githash")
        else:
            self.version_githash = ""
    
    version = property(get_version, set_version)

    @property
    def gitname(self):
        if self.version_githash:
            return self.version_githash
        # TODO
        return "nope"
    
    @property
    def filename(self):
        if not "/" in self.url:
            return self.url
        return self.url.split("/")[-1]
    
    def __unicode__(self):
        return "%s @ %s %s %s" % (self.version, self.channel, self.type, self.arch)
