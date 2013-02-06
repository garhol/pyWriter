from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .widgets import AgkaniCoverWidget

from .models import Story, Chapter, Scene, Character, Artifact, Location, Getfeed, Getissues
from .forms import SceneForm, CharacterForm, ArtifactForm, LocationForm, StoryForm, ChapterForm

import os.path

#@login_required
def index(request):
    context = {}
    template = 'index.html'
    published_books = []
    for st in Story.objects.filter(public_access=True):
        ebookpath = os.path.join(settings.STATIC_ROOT, "media", "epub", str(st.pk))
        filename  = "%s.epub" % st.title
        zippath = os.path.join(ebookpath, filename)
        if os.path.exists(zippath):
            book = []
            book.append(st.pk)
            book.append(filename)
            book.append(st.author)
            book.append(st.title)
            if st.cover:
                book.append(st.cover)
            else:
                nocover =  "covers/no-cover.jpg"
                book.append (nocover)
            published_books.append(book)
    context['published_books'] = published_books          
    
    if request.user.is_authenticated():
        context['title'] = "logged in"
        context['user'] = request.user
        context['stories'] = Story.objects.filter(
            user=request.user).order_by('title')
        context['chapters'] = Chapter.objects.filter(
            user=request.user).order_by('title')
        context['scenes'] = Scene.objects.filter(
            user=request.user).order_by('importance', 'name')
        context['characters'] = Character.objects.filter(
            user=request.user).order_by('-major_character', 'firstname')
        context['artifacts'] = Artifact.objects.filter(
            user=request.user).order_by('name')
        context['locations'] = Location.objects.filter(
            user=request.user).order_by('name')
        context['loggedin'] = True
    else:
        context['loggedin'] = False
        
    context['feed'] = Getfeed('https://github.com/garhol/pyWriter/commits/master.atom')
    context['issues'] = Getissues()
    return render_to_response(template, context, context_instance=RequestContext(request))


def get_active_story(request):
    st = request.session.get('active_story')
    if st != None:
	return int(st)
    else:
	return None


@login_required
def storylist(request):
    context = {}
     
    nocover = "covers/no-cover.jpg"
    
    context['stories'] = Story.objects.filter(
        user=request.user).order_by('title')
    context['nocover'] = nocover
    context['activestory'] = get_active_story(request)

    template = 'listings/list_story.html'
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def print_story(request, story=None):
    context = {}
    if story:
        st = get_object_or_404(Story, pk=story, user=request.user)

        ebookpath = os.path.join(settings.STATIC_ROOT, "library", "epub", str(st.pk))
        filename  = "%s.epub" % st.title
        zippath = os.path.join(ebookpath, filename)
        if os.path.exists(zippath):
            context['printversion'] = "epub"
        context['story'] = st
    template = 'story/print_story.html'
    return render_to_response(template, context, context_instance=RequestContext(request))    

@login_required
def activate_story(request, story=None):
    context = {}
    if story:
        st = get_object_or_404(Story, pk=story, user=request.user)
        request.session['active_story'] = story
        messages.success(request, 'Activated story.')
    context['story'] = st
    context["story_action"] = "story_activate"
    template = 'story/story.activate.html'
    return render_to_response(template, context, context_instance=RequestContext(request))    
        

@login_required
def story(request, story=None):
    context = {}
    
    if story:
        template = 'story/story.edit.html'
        st = get_object_or_404(Story, pk=story, user=request.user)
        context["story_action"] = "story_edit"
        context['story'] = st
        form = StoryForm(instance=st)
        context['form'] = form
    else:
        template = 'story/story.add.html'
        context['story'] = StoryForm()
        context["story_action"] = "story_add"
        context['form'] = StoryForm()

    if request.method == 'POST':
        if story:
            form = StoryForm(request.POST, request.FILES, instance=st)

        else:
            story = Story(user_id=request.user.pk)
            form = StoryForm(request.POST, request.FILES, instance=story)
        if form.is_valid():  # save it and tell them that all is well
            newstory = form.save()
            messages.success(request, 'Story details updated.')
            return HttpResponseRedirect(reverse('edit_story', args=(newstory.pk,)))
            #return render_to_response(template, context, context_instance=RequestContext(request))
        else:  # bung an error
            messages.error(request, 'There was an error - Look out below.')

            return render_to_response(template, context, context_instance=RequestContext(request))
    else:  # not in post, show them the location
        return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def chapterlist(request):
    context = {}
    context['chapters'] = Chapter.objects.filter(
        user=request.user).order_by('weight')
    if get_active_story(request):
        mystoryid = int(get_active_story(request))
        context['story'] = Story.objects.get(pk=mystoryid)
        context['active_chapters'] = Chapter.objects.filter(
            user=request.user).filter(story=mystoryid).order_by('weight')
        context['chapters'] = Chapter.objects.filter(
            user=request.user).order_by('weight').exclude(story=mystoryid)
    else:
        context['chapters'] = Chapter.objects.filter(
        user=request.user).order_by('weight')
        
    template = 'listings/list_chapter.html'
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def chaptersort(request):
    if request.is_ajax():
        if request.method == 'GET':
            message = "GET['out']"
        elif request.method == 'POST':
               
            sorting = request.POST.getlist('chapter[]')
            chapter_list = Chapter.objects.filter(pk__in=sorting)
            count = 1
            for s in sorting:
                for chap in chapter_list:
                    if chap.pk == int(s):
                        chap.weight = count
                        chap.save()
                count+=1
            message = "Updated"
    return HttpResponse(message)


@login_required
def chapter(request, chapter=None):
    context = {}
    template = 'story/chapter.html'
    if chapter:
        ch = get_object_or_404(Chapter, pk=chapter, user=request.user)
        context['chapter'] = ch
        context['form'] = ChapterForm(instance=ch, user=request.user)
    else:
        context['form'] = ChapterForm(user=request.user)

    if request.method == 'POST':
        if chapter:
            form = ChapterForm(
                request.POST, request.FILES, instance=ch, user=request.user)
        else:
            chapter = Chapter(user_id=request.user.pk)
            form = ChapterForm(request.POST, request.FILES,
                               instance=chapter, user=request.user)
        if form.is_valid():  # save it and tell them that all is well
            newchapter = form.save()
            messages.success(request, 'Chapter details updated.')
            return HttpResponseRedirect(reverse('edit_chapter', args=(newchapter.pk,)))
            #return render_to_response(template, context, context_instance=RequestContext(request))
        else:  # bung an error
            messages.error(request, 'There was an error - Look out below.')

            return render_to_response(template, context, context_instance=RequestContext(request))
    else:  # not in post, show them the location
        return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def characterlist(request):
    context = {}
    context['characters'] = Character.objects.filter(
        user=request.user).order_by('-major_character')
    template = 'listings/list_character.html'
    return render_to_response(template, context, context_instance=RequestContext(request))
    
@login_required
def character(request, character=None):
    context = {}
    template = 'story/character.html'
    if character:
        ch = get_object_or_404(Character, pk=character, user=request.user)
        context['character'] = ch
        context['form'] = CharacterForm(instance=ch)
    else:
        context['form'] = CharacterForm()

    if request.method == 'POST':
        if character:
            form = CharacterForm(request.POST, request.FILES, instance=ch)
        else:
            character = Character(user_id=request.user.pk)
            form = CharacterForm(
                request.POST, request.FILES, instance=character)
        if form.is_valid():  # save it and tell them that all is well
            newcharacter = form.save()
            messages.success(request, 'Character details updated.')
            return HttpResponseRedirect(reverse('edit_character', args=(newcharacter.pk,)))
        else:  # bung an error
            messages.error(request, 'There was an error - Look out below.')
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:  # not in post, show them the scene
        return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def preview_character(request, character):
    context = {}
    template = 'story/preview_character.html'
    if character:
        ch = get_object_or_404(Character, pk=character, user=request.user)
        context['character'] = ch
    else:
        context['error'] = "Character matching query does not exist"
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def locationlist(request):
    context = {}
    context['locations'] = Location.objects.filter(
        user=request.user).order_by('name')
    template = 'listings/list_location.html'
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def location(request, location=None):
    context = {}
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
            location = Location(user_id=request.user.pk)
            form = LocationForm(request.POST, request.FILES, instance=location)
        if form.is_valid():  # save it and tell them that all is well
            newlocation = form.save()
            messages.success(request, 'Location details updated.')
            return HttpResponseRedirect(reverse('edit_location', args=(newlocation.pk,)))
        else:  # bung an error
            messages.error(request, 'There was an error - Look out below.')

            return render_to_response(template, context, context_instance=RequestContext(request))
    else:  # not in post, show them the location
        return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def preview_location(request, location=None):
    context = {}
    template = 'story/preview_location.html'
    if location:
        lo = get_object_or_404(Location, pk=location, user=request.user)
        context['location'] = lo
    else:
        context['error'] = "Location matching query does not exist"
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def artifactlist(request):
    context = {}
    context['artifacts'] = Artifact.objects.filter(
        user=request.user).order_by('name')
    template = 'listings/list_artifact.html'
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def artifact(request, artifact=None):
    context = {}
    template = 'story/artifact.html'
    if (artifact):
        ar = get_object_or_404(Artifact, pk=artifact, user=request.user)
        context['artifact'] = ar
        context['form'] = ArtifactForm(instance=ar, user=request.user)
    else:
        context['form'] = ArtifactForm(user=request.user)

    if request.method == 'POST':
        if (artifact):
            form = ArtifactForm(
                request.POST, request.FILES, instance=ar, user=request.user)
        else:
            artifact = Artifact(user_id=request.user.pk)
            form = ArtifactForm(request.POST, request.FILES,
                                instance=artifact, user=request.user)
        if form.is_valid():  # save it and tell them that all is well
            newartifact = form.save()
            messages.success(request, 'Artifact details updated.')
            return HttpResponseRedirect(reverse('edit_artifact', args=(newartifact.pk,)))
        else:  # bung an error
            messages.error(request, 'There was an error - Look out below.')
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:  # not in post, show them the artifact
        return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def preview_artifact(request, artifact=None):
    context = {}
    template = 'story/preview_artifact.html'
    if (artifact):
        ar = get_object_or_404(Artifact, pk=artifact, user=request.user)
        context['artifact'] = ar
    else:
        context['error'] = "Artifact matching query does not exist"
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def scenelist(request):
    context = {}
    context['scenes'] = Scene.objects.filter(
        user=request.user).order_by('order')
    template = 'listings/list_scene.html'
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def scenesort(request):
    if request.is_ajax():
        if request.method == 'GET':
            message = "GET['out']"
        elif request.method == 'POST':
               
            sorting = request.POST.getlist('scene[]')
            scene_list = Scene.objects.filter(pk__in=sorting)
            count = 1
            for s in sorting:
                for sce in scene_list:
                    if sce.pk == int(s):
                        sce.order = count
                        sce.save()
                count+=1
            message = "Updated"
    return HttpResponse(message)
        
@login_required
def scene(request, scene=None):
    context = {}
    template = 'story/scene.html'
    if(scene):
        sc = get_object_or_404(Scene, pk=scene, user=request.user)
        context['scene'] = sc
        context['user'] = request.user
        context['characters'] = Character.objects.filter(
            scene=sc, user=request.user)
        context['locations'] = Location.objects.filter(
            scene=sc, user=request.user)
        context['artifacts'] = Artifact.objects.filter(
            scene=sc, user=request.user)
        context['form'] = SceneForm(instance=sc, user=request.user)
    else:
        context['form'] = SceneForm(user=request.user)

    if request.method == 'POST':
        if (scene):
            form = SceneForm(
                request.POST, request.FILES, instance=sc, user=request.user)
        else:
            scene = Scene(user_id=request.user.pk)
            form = SceneForm(request.POST, request.FILES,
                             instance=scene, user=request.user)
        if form.is_valid():  # save it and tell them that all is well
            newscene = form.save()
            messages.success(request, 'Scene details updated.')
            return HttpResponseRedirect(reverse('edit_scene', args=(newscene.pk,)))
        else:  # bung an error
            messages.error(request, 'There was an error - Look out below.')
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:  # not in post, show them the scene
        return render_to_response(template, context, context_instance=RequestContext(request))
