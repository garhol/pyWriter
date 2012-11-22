from django.db import models
from django.forms import ModelForm
from tinymce.widgets import TinyMCE
from django.contrib.auth.models import User
from django import forms

import math

MOTIVATION_LIST = [
    'Time to start writing',
    'You\'ve barely started!',
    'Time to get writing?',
    'You\'re getting somewhere now',
    'Nearly halfway there!',
    'The midway point',
    'It\'s all downhill from here',
    'Three quarters of the way there',
    'Almost at the finish',
    'Last push and you\'ll be done',
    'You\'ve done it!'
    ];


class Genre(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Story(models.Model): 
    user = models.ForeignKey(User)
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=128)
    synopsis = models.TextField(blank=True)
    genre = models.ForeignKey(Genre, null=True, blank=True)
    fiction = models.BooleanField(default=True)

    @property
    def get_chapters(self):
        chapters = Chapter.objects.all().filter(story=self).order_by('title')          
        return chapters
        
    @property
    def get_scenes(self):
        chapters = self.get_chapters
        scenes = []
        for chap in chapters:
            scenes += Scene.objects.filter(chapter=chap)
        return scenes

    @property
    def get_stats(self):
        stats = {}
        scenes = []
        wc = 0
        wt = 0
        scenes = self.get_scenes
        for s in scenes:
           wc = wc+s.word_count
           wt = wt+s.word_target
        stats['wordcount'] = wc
        stats['wordtarget'] = wt
        try:
            stats['percentage'] = int((float(wc) / float(wt)) * 100)
        except:
            stats['percentage'] = 0
        
        return stats
    
    @property
    def get_motivation(self):
        stats = self.get_stats
        percentage = stats['percentage']
        motivation = int(math.floor(int(percentage) * 0.1))
        
        if motivation >= 10:
            motivation = 10
        return MOTIVATION_LIST[motivation]
    
    def __unicode__(self):
        return self.title


class Chapter(models.Model):
    user = models.ForeignKey(User)
    story = models.ForeignKey(Story)
    title = models.CharField(max_length=256)
    weight = models.IntegerField(default=1)

    @property
    def get_scenes(self):
        scenes = Scene.objects.filter(chapter=self)
        return scenes
        
    def __unicode__(self):
        return self.title


class Scene(models.Model):
    OUTLINE = 'OL'
    DRAFT = 'DR'
    FIRSTEDIT = 'FE'
    SECONDEDIT = 'SE'
    DONE = 'DO'

    SUBPLOT = 'SP'
    MAINPLOT = 'MP'

    PLOT_CHOICES = (
        (MAINPLOT, 'Main plot'),
        (SUBPLOT, 'Subplot'),
    )

    STATUS_CHOICES = (
        (OUTLINE, 'Outline'),
        (DRAFT, 'Draft'),
        (FIRSTEDIT, '1st Edit'),
        (SECONDEDIT, '2nd Edit'),
        (DONE, 'Complete'),
    )

    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    importance = models.CharField(
        max_length=15, choices=PLOT_CHOICES, default=SUBPLOT)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default=OUTLINE)
    perspective = models.ForeignKey(
        'Character', related_name='perspective', null=True, blank=True)
    chapter = models.ForeignKey(Chapter, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    characters = models.ManyToManyField('Character', null=True, blank=True)
    location = models.ManyToManyField('Location', null=True, blank=True)
    artifacts = models.ManyToManyField('Artifact', null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    word_target = models.IntegerField(blank=True, default=1000)
    word_count = models.IntegerField(blank=True, null=True)

    @property
    def get_percentage_complete(self):
        return int((float(self.word_count) / float(self.word_target)) * 100)

    def __unicode__(self):
        return self.name


class Character(models.Model):
    user = models.ForeignKey(User)
    firstname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255, blank=True)
    lastname = models.CharField(max_length=255, blank=True)
    nicknames = models.TextField(null=True, blank=True)
    major_character = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to='characters/%Y/%m/%d', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.firstname, self.lastname)


class Artifact(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to='artifacts/%Y/%m/%d', null=True, blank=True)
    owner = models.ForeignKey(Character, null=True, blank=True)
    location = models.ForeignKey('Location', null=True, blank=True)

    def __unicode__(self):
        return self.name


class Location(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to='locations/%Y/%m/%d', null=True, blank=True)

    def __unicode__(self):
        return self.name


class SceneForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop(
            'user', None)  # get user for the scene form to limit the content
        super(SceneForm, self).__init__(*args, **kwargs)  # populates the post

        self.fields[
            'perspective'].queryset = Character.objects.filter(user=self.user)
        self.fields['chapter'].queryset = Chapter.objects.filter(
            user=self.user)
        self.fields[
            'characters'].queryset = Character.objects.filter(user=self.user)
        self.fields['location'].queryset = Location.objects.filter(
            user=self.user)
        self.fields[
            'artifacts'].queryset = Artifact.objects.filter(user=self.user)

    description = forms.CharField(
        widget=TinyMCE(), help_text="Enter a simple description of the scene")
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 100, 'rows': 30}, mce_attrs={'theme': 'advanced', 'theme_advanced_toolbar_location': 'top', 'theme_advanced_statusbar_location': 'bottom', 'plugins': 'wordcount'}))

    class Meta:
        model = Scene
        fields = ('name', 'word_target', 'status', 'importance', 'perspective', 'chapter', 'description', 'characters', 'location', 'artifacts', 'content')


class CharacterForm(forms.ModelForm):

    class Meta:
        model = Character
        fields = ('firstname', 'middlename', 'lastname', 'nicknames', 'major_character', 'description', 'image', 'bio', 'date_of_birth', 'date_of_death')


class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = ('name', 'description', 'image')


class ArtifactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop(
            'user', None)  # get user for the scene form to limit the content
        super(
            ArtifactForm, self).__init__(*args, **kwargs)  # populates the post

        self.fields['owner'].queryset = Character.objects.filter(
            user=self.user)
        self.fields['location'].queryset = Location.objects.filter(
            user=self.user)

    class Meta:
        model = Artifact
        fields = ('name', 'description', 'image', 'owner', 'location')


class StoryForm(forms.ModelForm):

    class Meta:
        model = Story
        fields = ('title', 'author', 'synopsis', 'genre', 'fiction')


class ChapterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop(
            'user', None)  # get user for the scene form to limit the content
        super(
            ChapterForm, self).__init__(*args, **kwargs)  # populates the post

        self.fields['story'].queryset = Story.objects.filter(user=self.user)

    class Meta:
        model = Chapter
        fields = ('story', 'title', 'weight')

from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=Scene)
def create_wordcount(instance, **kwargs):
    words = instance.content.split()
    instance.word_count = len(words)


@receiver(pre_save, sender=Scene)
def create_narrator(instance, **kwargs):
    if not instance.pk:
        narrator, created = Character.objects.get_or_create(
            user=instance.user, firstname='Narrator', nicknames='John')
        if not instance.perspective:
            instance.perspective = narrator
