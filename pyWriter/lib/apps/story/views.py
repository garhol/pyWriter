from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect
from .models import Story, Chapter, Scene, Character, Artifact, Location, SceneForm


def index(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/?next=%s' % request.path)
	else:
		context ={}   
		template = 'index.html'    
		context['title'] = "logged in"
		context['user'] = request.user
		context['stories'] = Story.objects.all();
		context['chapters'] = Chapter.objects.all();
		context['scenes'] = Scene.objects.all();
		context['characters'] = Character.objects.all();
		context['artifacts'] = Artifact.objects.all();
		context['locations'] = Location.objects.all();
		return render_to_response(template, context)
		
def scene(request, scene):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/?next=%s' % request.path)
	else:
		context ={}
		context['user'] = request.user
		sc = Scene.objects.get(pk=scene)
		context['scene'] = sc
		
		if request.method == 'POST':
			form = SceneForm(request.POST, instance=sc)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/') # redirect
		else:
			context['form'] = SceneForm(instance=sc)
			template = 'story/scene.html'
			return render_to_response(template,
									context,
									context_instance=RequestContext(request))
