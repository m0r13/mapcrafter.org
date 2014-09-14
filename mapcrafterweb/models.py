from django.db.models.base import Model
from django.db.models.fields import CharField, DateTimeField
from django.utils import timezone
from django.db.models.fields.related import ForeignKey

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
    
    ARCH_32_BIT = "32"
    ARCH_64_BIT = "64"
    ARCHS = (
        (ARCH_32_BIT, "32 Bit"),
        (ARCH_64_BIT, "64 Bit"),
    )
    
    type = ForeignKey(PackageType, verbose_name="type")
    arch = CharField(choices=ARCHS, max_length=255, verbose_name="architecture")
    date = DateTimeField(default=timezone.now, verbose_name="date")
    # todo version
    url = CharField(max_length=255, verbose_name="url")
    
    @property
    def arch_name(self):
        if self.arch == Package.ARCH_32_BIT:
            return "32 Bit"
        if self.arch == Package.ARCH_64_BIT:
            return "64 Bit"
        return "Unknown architecture"
    
    @property
    def filename(self):
        if not "/" in self.url:
            return self.url
        return self.url.split("/")[-1]
    
    def __unicode__(self):
        return "Build %s %s%s" % (self.date, self.type, self.arch)
