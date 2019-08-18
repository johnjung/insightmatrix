from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    '''
    name = forms.CharField(help_text='I set help text.', label='Project Name', max_length=200)
    description = forms.CharField(label='Project Description', widget=forms.Textarea) 
    labels = forms.CharField(label='Labels', widget=forms.Textarea)
    '''
    class Meta:
        model = Project
        fields = ('name', 'description')
