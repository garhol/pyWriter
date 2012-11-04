from django.db import models
from django.forms import ModelForm
from tinymce.widgets import TinyMCE
from django.contrib.auth.models import User
from django import forms

class Story(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=128)

    def __unicode__(self):
        return self.title

class Chapter(models.Model):
    user = models.ForeignKey(User)
    story = models.ForeignKey(Story)
    title = models.CharField(max_length=256)
    weight = models.IntegerField(default=1)
    
    def __unicode__(self):
        return self.title


class Scene(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    perspective = models.ForeignKey('Character', related_name='perspective', null=True, blank=True)
    chapter = models.ForeignKey(Chapter, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    characters = models.ManyToManyField('Character', null=True, blank=True)
    location = models.ManyToManyField('Location', null=True, blank=True)
    artifacts = models.ManyToManyField('Artifact', null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name
       

class Character(models.Model):
    user = models.ForeignKey(User)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    nicknames = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    
    def __unicode__(self):
        return "%s %s" % (self.firstname, self.lastname)
    
    
class Artifact(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(Character, null=True, blank=True)
    location = models.ForeignKey('Location', null=True, blank=True)
    
    def __unicode__(self):
        return self.name
    

class Location(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class SceneForm(forms.ModelForm):
    user = forms.CharField(widget=forms.HiddenInput)
    description = forms.CharField(widget=TinyMCE(), help_text="Enter a simple description of the scene")
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
   
    class Meta:
        model = Scene
        
        
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=Scene)
def create_narrator(instance, **kwargs):
    if not instance.pk:
        narrator, created = Character.objects.get_or_create(user=instance.user, firstname='John', nicknames='Narrator')
        if not instance.perspective:
            instance.perspective = narrator
    
