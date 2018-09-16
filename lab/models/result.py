from django.db import models
from .workflow_perm import WorkflowPerm


class Result(models.Model):
    wf_perm = models.ForeignKey(WorkflowPerm, on_delete=models.DO_NOTHING)
    key = models.CharField(max_length=50)
    value = models.TextField()
    is_final_result = models.BooleanField(default=False)

    # class Meta:
    #     unique_together = ('run', 'key')
