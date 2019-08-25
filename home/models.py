import itertools
import random

from django.conf import settings
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
        all_labels = set()
        for label_one, label_two in itertools.combinations(
                set(
                    Label.objects.filter(project=self).values_list('pk', 'name')
                ),
                2
            ):
            if label_one[0] <= label_two[0]:
                all_labels.add((
                    (label_one[0], label_one[1]),
                    (label_two[0], label_two[1])
                ))
            else:
                all_labels.add((
                    (label_two[0], label_two[1]),
                    (label_one[0], label_one[1])
                ))

        ranked_labels = set()
        for s in Similarity.objects.filter(project=self):
            if s.label_one.pk <= s.label_two.pk:
                ranked_labels.add((
                    (s.label_one.pk, s.label_one.name), 
                    (s.label_two.pk, s.label_two.name)
                ))
            else:
                ranked_labels.add((
                    (s.label_two.pk, s.label_two.name),
                    (s.label_one.pk, s.label_one.name) 
                ))
        unranked_labels = all_labels.difference(ranked_labels)

        if ranked and unranked:
            return list(all_labels)
        elif ranked:
            return list(ranked_labels)
        elif unranked:
            return list(unranked_labels)
        else:
            return list()

    def get_random_unranked_label_pair(self):
        unranked_label_pairs = self.get_all_label_pairs(
            ranked=False,
            unranked=True
        )
        if unranked_label_pairs:
            random.shuffle(unranked_label_pairs)
            return unranked_label_pairs[0]
        else:
            return None


class Label(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="labels")
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = ('project', 'name')


class Similarity(models.Model):
    label_one = models.ForeignKey(Label, on_delete=models.CASCADE, related_name="similarity_one")
    label_two = models.ForeignKey(Label, on_delete=models.CASCADE, related_name="similarity_two")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="similarity")
    score = models.FloatField()
