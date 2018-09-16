from django.db import models
from .workflow import Workflow
import json

class WorkflowPerm(models.Model):
    workflow = models.ForeignKey(Workflow, models.CASCADE)
    description = models.TextField()

    def execute(self, data):
        for phase in data:
            from .task import Task
            t = Task()
            t.execute(self.id, data[phase])
        from .result import Result
        return list(Result.objects.filter(wf_perm_id=self.id).values())

    def __str__(self):
        return json.dumps(self.description)
