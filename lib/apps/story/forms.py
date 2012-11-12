from .models import Scene

class SceneForm(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        
        self.request = kwargs.pop('request', None)        
        super (SceneForm, self).__init__(*args,**kwargs) # populates the post
        
        
        self.fields['persepective'].queryset = Character.objects.filter(user=self.request.user)
        #self.fields['characters'].queryset = Character.objects.filter(user=self.User)
        #self.fields['location'].queryset = Location.objects.filter(user=self.User)
        #self.fields['artifacts'].queryset = Artifact.objects.filter(user=self.User)

    description = forms.CharField(widget=TinyMCE(), help_text="Enter a simple description of the scene")
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}, mce_attrs={'theme':'advanced','theme_advanced_toolbar_location':'top','theme_advanced_statusbar_location':'bottom','plugins':'wordcount' } ))

    class Meta:
        model = Scene
        fields =('name', 'perspective', 'chapter', 'description', 'characters', 'location', 'artifacts', 'content')
