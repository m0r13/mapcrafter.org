from django.db.models.base import Model
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey

# Create your models here.

class Platform(Model):
    class Meta:
        verbose_name = "platform"
        verbose_name_plural = "platforms"
    
    name = CharField(max_length=255, verbose_name="name")
    
    def __unicode__(self):
        return self.name

class Build(Model):
    class Meta:
        verbose_name = "build"
        verbose_name_plural = "builds"
    
    platform = ForeignKey(Platform, verbose_name="platform")
    version = CharField(max_length=255, verbose_name="version")
    filename = CharField(max_length=255, verbose_name="filename")
    
    def __unicode__(self):
        return "Build %s %s" % (self.version, self.platform)
