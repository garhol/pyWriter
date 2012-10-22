from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
   
@csrf_protect 
def login_view(request):
	
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				# Return a 'disabled account' error message
				return HttpResponseRedirect('/')
		else:
			# Return an 'invalid login' error message.
			return HttpResponseRedirect('/')
	else:
		context ={}
		template = 'login.html'
		return render_to_response(template, context, context_instance=RequestContext(request))

	
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')
