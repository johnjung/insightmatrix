import itertools

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        editable=False,
        null=True,
        on_delete=models.CASCADE
    )
    description = models.TextField(default='')
    creation_date = models.DateTimeField(default=timezone.now, editable=False)

    def get_all_label_pairs(self, ranked=True, unranked=True):
        """Should return pairs, e.g.:
            [
                ((1, 'apple'), (2, 'orange')),
                ((1, 'apple'), (3, 'peach'))
            ]
        """

        all_labels = set(
            Label.objects.filter(project=self).values_list('pk', 'name')
        )
        ranked_labels = set(
            Similarity.objects.filter(
                label_one__project=self
            ).values_list(
                'label_one__pk',
                'label_one__name'
            )
        ).union(
            set(
                Similarity.objects.filter(
                    label_two__project=self
                ).values_list(
                    'label_two__pk',
                    'label_two__name'
                )
            )
        )
        unranked_labels = all_labels.difference(ranked_labels)

        if ranked and unranked:
            return itertools.combinations(all_labels)
        elif ranked:
            return itertools.combinations(ranked_labels)
        elif unranked:
            return itertools.combinations(unranked_labels)
        else:
            return itertools.combinations(set())

    def get_random_unranked_label_pair(self):
        return random.shuffle(
            self.get_all_label_pairs(ranked=False, unranked=True)
        )[0]


class Label(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="labels")
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = ('project', 'name')


class Similarity(models.Model):
    label_one = models.ForeignKey(Label, on_delete=models.CASCADE, related_name="similarity_one")
    label_two = models.ForeignKey(Label, on_delete=models.CASCADE, related_name="similarity_two")
    score = models.FloatField()
