from django.db import models
from django.contrib.auth.models import User

from django.template.defaultfilters import slugify

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
    storyslug = models.SlugField(null=True, blank=True)
    title = models.CharField(max_length=256,  help_text="Short and snappy? Verbose yet informative?")
    author = models.CharField(max_length=128, help_text="A pseudonym? Remember, you can always change this later")
    synopsis = models.TextField(blank=True, help_text="A brief summary, your salespitch. What are the main themes/points of your story?")
    genre = models.ForeignKey(Genre, null=True, blank=True, help_text="If a genre is not listed then feel free to get in touch with suggestions")
    fiction = models.BooleanField(default=True, help_text="Leave this blank if you are writing a factual account. If it's a tissue of lies however...")
    cover = models.ImageField(
        upload_to='covers/%Y/%m/%d', null=True, blank=True, help_text="A picture is worth a thousand words. This doesn't mean we will add this to your word count")
    registered_access = models.BooleanField(default=False, help_text="When published make this story available to registered users")
    public_access = models.BooleanField(default=False, help_text="When published, make this story available to the public (Overrides registered user access)")
    
    def save(self, *args, **kwargs):
		uniquestring = "%s %s" % (self.title, self.author)
		self.storyslug = slugify(uniquestring)
		super(Story, self).save(*args, **kwargs)
		
    @property
    def get_chapters(self):
        chapters = Chapter.objects.all().filter(story=self).order_by('weight')          
        return chapters
        
    @property
    def get_chapter_count(self):
        chapters = Chapter.objects.all().filter(story=self)
        return len(chapters)
        
    @property
    def get_scenes(self):
        chapters = self.get_chapters
        scenes = []
        for chap in chapters:
            scenes += Scene.objects.filter(chapter=chap).order_by('order')
        return scenes
    
    @property
    def get_characters(self):
        scenes = self.get_scenes
        charlist = []
        for s in scenes:
            charlist += Character.objects.filter(scene=s)
        charlist = set(charlist) # converts the charlist to distinct values
        return charlist
    
    @property
    def get_locations(self):
        scenes = self.get_scenes
        locations = []
        for s in scenes:
            locations += Location.objects.filter(scene=s)
        locations = set(locations)
        return locations

    @property
    def get_artifacts(self):
        scenes = self.get_scenes
        artifacts = []
        for s in scenes:
            artifacts += Artifact.objects.filter(scene=s)
        artifact = set(artifacts)
        return artifacts

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
        scenes = Scene.objects.filter(chapter=self).order_by('order')
        return scenes
    
    @property
    def get_scene_count(self):
        scenes = Scene.objects.filter(chapter=self)
        return len(scenes)
        
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
    order = models.IntegerField(default=1)
    scene_start_time = models.DateTimeField(null=True, blank=True)
    scene_end_time = models.DateTimeField(null=True, blank=True)

    @property
    def get_percentage_complete(self):
        return int((float(self.word_count) / float(self.word_target)) * 100)

    @property
    def get_character_count(self):
        charlist = Character.objects.filter(scene=self)
        return len(charlist)

    @property
    def get_location_count(self):
        locationlist = Location.objects.filter(scene=self)
        return len(locationlist)

    @property
    def get_scene_location(self):
        scene_location = Location.objects.filter(scene=self)
        if scene_location:
            return scene_location[0]
        else:
            return "an unknown location"
        
    @property
    def get_artifact_count(self):
        artifactlist = Artifact.objects.filter(scene=self)
        return len(artifactlist)

    def __unicode__(self):
        return self.name


class Character(models.Model):
    user = models.ForeignKey(User)
    firstname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255, blank=True)
    lastname = models.CharField(max_length=255, blank=True)
    nicknames = models.TextField(null=True, blank=True)
    major_character = models.BooleanField(default=False)
    role = models.CharField(max_length=255, null=True, blank=True, 
        help_text="The role this character might play. Is he lover, father, killer, chauffeur, detective, soldier, wizard?")
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to='characters/%Y/%m/%d', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    
    def get_timeline(self):
        t = Scene.objects.all().filter(characters=self).order_by('scene_start_time')
        
        return t;
        
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
    date_of_construction = models.DateField(null=True, blank=True)
    date_of_destruction = models.DateField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name


class Location(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    date_of_construction = models.DateField(null=True, blank=True)
    date_of_destruction = models.DateField(null=True, blank=True)
    image = models.ImageField(
        upload_to='locations/%Y/%m/%d', null=True, blank=True)

    def __unicode__(self):
        return self.name

import feedparser
def Getfeed(url):
    d = feedparser.parse(url)
    return d.entries;

def Getissues():
    import urllib, json
    url = "https://api.github.com/repos/garhol/pywriter/issues"
    try:
        myresponse = urllib.urlopen(url)
        jsonResponse = json.loads(myresponse.read())
    except:
        jsonResponse = None
    return jsonResponse
    

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
