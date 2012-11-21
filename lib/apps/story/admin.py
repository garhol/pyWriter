from pyWriter.lib.apps.story.models import Story, Chapter, Scene, Location, Character, Artifact, Genre
from django.contrib import admin


class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'user',)
    list_filter = ('user',)


class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'story', 'user',)
    list_filter = ('user', 'story', )


class SceneAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'importance', 'status',)
    list_filter = ('user',  )

    
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user',)
    list_filter = ('user',  )


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'major_character', 'user',)
    list_filter = ('user', 'major_character',)

    
class ArtifactAdmin(admin.ModelAdmin):
    list_display = ('name', 'user',)
    list_filter = ('user',  )
    
admin.site.register(Story, StoryAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Scene, SceneAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Artifact, ArtifactAdmin)
admin.site.register(Genre)
