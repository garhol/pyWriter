from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

def index(request):
    context ={}
    
    template = 'story/index.html'
    context['title'] = "title story"
    
    return render_to_response(template, context)
