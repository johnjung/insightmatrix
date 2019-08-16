from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import Label, Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

ProjectFormSet = inlineformset_factory(Project, Label, form=ProjectForm, fields=('name',), extra=3)
