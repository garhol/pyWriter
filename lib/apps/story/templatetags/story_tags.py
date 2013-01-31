# Registering Template Inclusion Tags
from django.template import Library

register = Library()

@register.inclusion_tag("form_partials/_story_details_form.html", takes_context=True)
def story_form(context, fm):
    return {"form" :fm, "s":context['story'],}

@register.inclusion_tag("form_partials/_scene_form.html")
def scene_form(fm):
	return {"form": fm,}

# dummy form for now
@register.inclusion_tag("form_partials/_story_facets_form.html", takes_context=True)
def story_facets(context):
    return {"s":context['story'],}

@register.inclusion_tag("form_partials/_generic_one_column_form.html")
def generic_one_column_form(fm):
    return {"form" : fm}

@register.filter('is_checkbox')
def is_checkbox(form_field_obj):
	return (form_field_obj.field.widget.__class__.__name__ == "CheckboxInput")

@register.filter('is_textarea')
def is_textarea(form_field_obj):
	return (form_field_obj.field.widget.__class__.__name__ == "Textarea")

@register.filter('is_textinput')
def is_textinput(form_field_obj):
	return (form_field_obj.field.widget.__class__.__name__ == "TextInput")

@register.filter('is_select')
def is_select(form_field_obj):
	return (form_field_obj.field.widget.__class__.__name__ == "Select")

@register.filter('is_file')
def is_file(form_field_obj):
	return (form_field_obj.field.widget.__class__.__name__ == "ClearableFileInput")
