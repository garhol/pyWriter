from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect
from .models import Story, Chapter, Scene, Character, Artifact, Location, SceneForm, CharacterForm



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

def character(request, character):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)
    else:
        context ={}
        ch = Character.objects.get(pk=character)
        context['character'] = ch
        template = 'story/character.html'
        if request.method == 'POST':
            form = CharacterForm(request.POST, request.FILES, instance=ch)
            if form.is_valid(): # save it and tell them that all is well
                form.save()
                context['saved'] = True
                context['form'] = CharacterForm(instance=ch)              
                return render_to_response(template, context, context_instance=RequestContext(request))
            else: # bung an error
                context['form'] = CharacterForm(instance=ch)
                context['error'] = True
                return render_to_response(template, context, context_instance=RequestContext(request))
        else: # not in post, show them the scene
            context['form'] = CharacterForm(instance=ch)
            return render_to_response(template, context, context_instance=RequestContext(request))

        
        
def scene(request, scene):
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
