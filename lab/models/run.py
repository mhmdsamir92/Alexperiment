from django.db import models


class Run(models.Model):
    started_at = models.DateTimeField(auto_now_add=True)
