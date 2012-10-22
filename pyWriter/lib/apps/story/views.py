from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect


def index(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/?next=%s' % request.path)
	else:
		context ={}   
		template = 'index.html'    
		context['title'] = "logged in"
		context['user'] = request.user
		return render_to_response(template, context)
