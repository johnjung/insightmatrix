from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views import View
from .forms import ProjectFormSet
from .models import Project

class ProjectCreate(CreateView):
    model = Project
    fields = ['name', 'description']
    success_url = '/'

    def get_context_data(self, **kwargs):
        data = super(ProjectCreate, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            data['project'] = ProjectFormSet(self.request.POST)
        else:
            data['project'] = ProjectFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        project = context['project']
        with transaction.atomic():
            self.object = form.save()
            if project.is_valid():
                project.instance = self.object
                project.save()
            return super(ProjectCreate, self).form_valid(form) 

# this should render the svg. 
class ProjectDetail(DetailView):
    model = Project

class ProjectList(ListView):
    model = Project
    context_object_name = 'project'
    paginate_by = 9
    ordering = ['-creation_date']
