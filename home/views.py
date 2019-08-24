from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views import View
from .forms import ProjectForm
from .models import Label, Project, Similarity


def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            for label in request.POST['labels'].split():
                Label.objects.create(name=label, project=project)
            return redirect('similarity_create', project=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'home/project_create.html', {'form': form})


def project_update(request, pk=None):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            form_label_names = request.POST['labels'].split()
            # delete labels that no longer exist. 
            Label.objects.filter(project=project).exclude(name__in=form_label_names).delete()

            # add labels that are new.
            for form_label_name in list(
                set(form_label_names).difference(
                    set(Label.objects.filter(project=project).values_list('name', flat=True))
                )
            ):
                Label.objects.create(name=form_label_name, project=project)
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(
        request, 
        'home/project_update.html',
        {
            'form': form,
            'labels': ' '.join(Label.objects.filter(project__pk=pk).values_list('name', flat=True))
        }
    )


def similarity_create(request, project=None):
    # add a new similarity score to the database.
    if request.method == "POST":
        form = SimilarityForm(request.POST)
        if form.is_valid():
            similarity = form.save()
            return redirect('similarity_create', project=project.pk)
    else:
        random_label_pair = Project.objects.get(pk=project).get_random_unranked_label_pair()
        if random_label_pair:
            form = SimilarityForm()
            return render(
                request, 
                'home/similarity_create.html',
                {
                    'label_one': random_label_pair[0][1],
                    'label_one_pk': random_label_pair[0][0],
                    'label_two': random_label_pair[1][1],
                    'label_two_pk': random_label_pair[1][0]
                }
            )
        else:
            return redirect('similarity_list', project=project)


def similarity_list(request, project=None):
    return render(request, 'home/similarity_list.html', {
        'project': Project.objects.get(pk=project)
    })


class HomePage(TemplateView):
    template_name = 'home/homepage.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('project_list')
        else:
            return super(HomePage, self).dispatch(request, *args, **kwargs)

 
class ProjectList(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    model = Project
    context_object_name = 'project'
    paginate_by = 9

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user).order_by('-creation_date')
