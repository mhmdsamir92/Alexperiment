from lab.models.task import Task


class Phase:
    def execute(self, run_id, data):
        t = Task()
        t.execute(run_id, data)
