from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe

class AgkaniCoverWidget(ClearableFileInput):
	def render(self, name, value, attrs=None):
		output = []


		return mark_safe(u''.join(output))