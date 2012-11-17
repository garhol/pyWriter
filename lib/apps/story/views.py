from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Story, Chapter, Scene, Character, Artifact, Location, SceneForm, CharacterForm, ArtifactForm, LocationForm, StoryForm

@login_required
def index(request):
	context ={}   
	template = 'index.html'    
	context['title'] = "logged in"
	context['user'] = request.user
	context['stories'] = Story.objects.filter(user=request.user);
	context['chapters'] = Chapter.objects.filter(user=request.user);
	context['scenes'] = Scene.objects.filter(user=request.user);
	context['characters'] = Character.objects.filter(user=request.user);
	context['artifacts'] = Artifact.objects.filter(user=request.user);
	context['locations'] = Location.objects.filter(user=request.user);
	return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def story(request, story=None):
	context ={}
	template = 'story/story.html'
	if story:
		st = get_object_or_404(Story, pk=story, user=request.user)
		context['story'] = st
		context['form'] = StoryForm(instance=st)
	else:
		context['form'] = StoryForm()
		
	if request.method == 'POST':
		if story:
			form = StoryForm(request.POST, request.FILES, instance=st)
		else:
			story = Story(user_id = request.user.pk)
			form = StoryForm(request.POST, request.FILES, instance=story)
		if form.is_valid(): # save it and tell them that all is well
			newstory = form.save()
			context['saved'] = True                
			return HttpResponseRedirect(reverse('edit_story', args=(newstory.pk,)))
			#return render_to_response(template, context, context_instance=RequestContext(request))
		else: # bung an error
			context['error'] = True
			
			return render_to_response(template, context, context_instance=RequestContext(request))
	else: # not in post, show them the location
		return render_to_response(template, context, context_instance=RequestContext(request))
        
        
@login_required
def character(request, character=None):
	context ={}
	template = 'story/character.html'
	if character:
		ch = get_object_or_404(Character, pk=character, user=request.user)
		context['character'] = ch
		context['form'] = CharacterForm(instance=ch)              
	else:
		context['form'] = CharacterForm()
	
	if request.method == 'POST':
		if character:
			form = CharacterForm(request.POST, request.FILES, instance = ch)
		else:
			character = Character(user_id = request.user.pk)
			form = CharacterForm(request.POST, request.FILES, instance = character)
		if form.is_valid(): # save it and tell them that all is well
			form.save()
			context['saved'] = True
			return render_to_response(template, context, context_instance=RequestContext(request))
		else: # bung an error
			context['error'] = True
			return render_to_response(template, context, context_instance=RequestContext(request))
	else: # not in post, show them the scene
		return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def location(request, location=None):
	context ={}
	template = 'story/location.html'
	if location:
		lo = get_object_or_404(Location, pk=location, user=request.user)
		context['location'] = lo
		context['form'] = LocationForm(instance=lo)
	else:
		context['form'] = LocationForm()
		
	if request.method == 'POST':
		if location:
			form = LocationForm(request.POST, request.FILES, instance=lo)
		else:
			location = Location(user_id = request.user.pk)
			form = LocationForm(request.POST, request.FILES, instance=location)
		if form.is_valid(): # save it and tell them that all is well
			newlocation = form.save()
			context['saved'] = True                
			return HttpResponseRedirect(reverse('edit_location', args=(newlocation.pk,)))
			#return render_to_response(template, context, context_instance=RequestContext(request))
		else: # bung an error
			context['error'] = True
			
			return render_to_response(template, context, context_instance=RequestContext(request))
	else: # not in post, show them the location
		return render_to_response(template, context, context_instance=RequestContext(request))
 
@login_required
def artifact(request, artifact=None):
	context ={}
	template = 'story/artifact.html'
	if (artifact):
		ar = get_object_or_404(Artifact, pk=artifact, user=request.user)
		context['artifact'] = ar       
		context['form'] = ArtifactForm(instance=ar)
	else:
		context['form'] = ArtifactForm()
	
	if request.method == 'POST':
		if (artifact):
			form = ArtifactForm(request.POST, request.FILES, instance=ar)
		else:
			artifact = Artifact(user_id = request.user.pk)
			form = ArtifactForm(request.POST, request.FILES, instance=artifact)
		if form.is_valid(): # save it and tell them that all is well
			form.save()
			context['saved'] = True
			return render_to_response(template, context, context_instance=RequestContext(request))
		else: # bung an error                
			context['error'] = True
			return render_to_response(template, context, context_instance=RequestContext(request))
	else: # not in post, show them the artifact
		return render_to_response(template, context, context_instance=RequestContext(request))
            
@login_required                  
def scene(request, scene=None):
	context ={}
	context['user'] = request.user
	sc = get_object_or_404(Scene, pk=scene, user=request.user)
	context['scene'] = sc
	context['characters'] = Character.objects.filter(scene=sc, user=request.user)
	context['locations'] = Location.objects.filter(scene=sc, user=request.user)
	context['artifacts'] = Artifact.objects.filter(scene=sc, user=request.user)
	template = 'story/scene.html'
	if request.method == 'POST':
		form = SceneForm(request.POST, instance=sc, user=request.user)
		if form.is_valid(): # save it and tell them that all is well
			form.save()
			context['saved'] = True
			context['form'] = SceneForm(instance=sc, user=request.user)              
			return render_to_response(template, context, context_instance=RequestContext(request))
		else: # bung an error
			context['form'] = SceneForm(instance=sc, user=request.user)
			context['error'] = True
			return render_to_response(template, context, context_instance=RequestContext(request))
	else: # not in post, show them the scene
		context['form'] = SceneForm(instance=sc, user=request.user)
		return render_to_response(template, context, context_instance=RequestContext(request))
