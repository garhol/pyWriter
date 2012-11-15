from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Story, Chapter, Scene, Character, Artifact, Location, SceneForm, CharacterForm, ArtifactForm, LocationForm



def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)
    else:
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

def character(request, character=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)
    else:
        context ={}
        template = 'story/character.html'
        if character:
            ch = Character.objects.get(pk=character)
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


def location(request, location=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)
    else:
        context ={}
        template = 'story/location.html'
        if location:
            lo = Location.objects.get(pk=location)
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
 
 
 
def artifact(request, artifact=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)
    else:
        context ={}
        template = 'story/artifact.html'
        if (artifact):
            ar = Artifact.objects.get(pk=artifact)
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
            
                    
def scene(request, scene=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path) # not logged in. Kick them out.
    else:
        context ={}
        context['user'] = request.user
        sc = Scene.objects.get(pk=scene)
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
