from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Faq(models.Model):
    question = models.CharField(max_length=254, blank=False)
    answer = models.TextField(blank=True)
    display = models.IntegerField(
        default=50, null=True, blank=True,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])

    def __str__(self):
        return self.question
