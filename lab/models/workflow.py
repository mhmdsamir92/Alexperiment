from django.db import models
from .run import Run


class Workflow(models.Model):
    run = models.ForeignKey(Run, models.CASCADE)
