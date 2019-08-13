from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(default='')
    creation_date = models.DateTimeField(default=timezone.now)

class Label(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = ('project', 'name')

class Similarity(models.Model):
    label_one = models.ForeignKey(Label, on_delete=models.CASCADE, related_name="similarity_one")
    label_two = models.ForeignKey(Label, on_delete=models.CASCADE, related_name="similarity_two")
    score = models.FloatField()
