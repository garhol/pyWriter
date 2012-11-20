from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

from .forms import UserCreateForm


@csrf_protect
def login_view(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Login successful.')
                return HttpResponseRedirect('/')
            else:
                messages.error(request, 'This user account is disabled.')
                # Return a 'disabled account' error message
                return HttpResponseRedirect('/')
        else:
            messages.error(request, "There's something wrong there. Did you mistype something?")
            # Return an 'invalid login' error message.
            return HttpResponseRedirect('/')
    else:
        context = {}
        template = 'login.html'
        return render_to_response(template, context, context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return HttpResponseRedirect('/')


def create_user_view(request, *args, **kwargs):
    context = {}
    template = 'signup.html'
    context['user_form'] = UserCreateForm()

    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username,
                                password=password)
            login(request, user)
            messages.success(request, "That went better than expected")
            return HttpResponseRedirect('/')
        else:
            context['user_form'] = UserCreateForm(request.POST)
            messages.error(
                request, "That didn't work, you sure you typed that cleanly?")
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        return render_to_response(template, context, context_instance=RequestContext(request))
