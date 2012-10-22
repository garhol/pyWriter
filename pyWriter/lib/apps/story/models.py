from django.db import models

class Story(models.Model):
	title = models.CharField(max_length=256)
	author = models.CharField(max_length=128)

	def __unicode__(self):
		return self.title

class Chapter(models.Model):
	story = models.ForeignKey(Story)
	title = models.CharField(max_length=256)
	
	def __unicode__(self):
		return self.title

class Scene(models.Model):
	Chapter = models.ForeignKey(Chapter)
	description = models.TextField()

	def __unicode__(self):
		return self.description

class Location(models.Model):
	description = models.TextField()

	def __unicode__(self):
		return self.description
	
