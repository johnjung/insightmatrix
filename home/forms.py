from django import forms
from .models import *

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description')


class SimilarityForm(forms.ModelForm):
    class Meta:
        model = Similarity
        fields = ('label_one', 'label_two', 'project', 'score')
        widgets = {
            'label_one': forms.HiddenInput(),
            'label_two': forms.HiddenInput(),
            'project': forms.HiddenInput()
        }
