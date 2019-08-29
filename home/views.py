from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from .forms import ProjectForm, SimilarityForm
from .models import Label, Project, Similarity


def label_list(request, project=None):
    """Return the list of labels, in order. Always returns JSON for the
    javascript front end. project is an integer, the pk.
    """
    label_list = []
    for l in Project.objects.get(pk=project).labels.order_by('pk'):
        label_list.append(l.name)
    return JsonResponse(label_list, safe=False)


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
    """project is an integer, the pk."""
    if request.method == "POST":
        form = SimilarityForm(request.POST)
        if form.is_valid():
            similarity = form.save()
            return redirect('similarity_create', project=project)
    else:
        random_label_pair = Project.objects.get(pk=project).get_random_unranked_label_pair()
        if random_label_pair:
            form = SimilarityForm(initial={
                'label_one': Label.objects.get(pk=random_label_pair[0][0]),
                'label_two': Label.objects.get(pk=random_label_pair[1][0]),
                'project': project
            })
            return render(request, 'home/similarity_create.html', {
                'form': form,
                'label_one': random_label_pair[0][1],
                'label_two': random_label_pair[1][1]
            })
        else:
            return redirect('similarity_list', project=project)


def similarity_list(request, project=None):
    if 'format' in request.GET and request.GET['format'] == 'json':
        labels = Project.objects.get(pk=project).labels.all().values_list('name', flat=True)
        similarity_dict = {a: {b: 0.0 for b in labels} for a in labels}
        # set diagonals to 3.0
        for l in labels:
            similarity_dict[l][l] = 3.0
        # look up all other similarities in the db.
        for s in Similarity.objects.filter(project__pk=project):
            similarity_dict[s.label_one.name][s.label_two.name] = \
            similarity_dict[s.label_two.name][s.label_one.name] = s.score
        return JsonResponse(similarity_dict)
    else:
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
