# from django.db import models


class Task:
    from lab.executers.data_executors.read_data_executor import ReadDataExecutor
    from lab.executers.classification_executors.dnn_executor import DNNExecutor
    task_adapter = {
        "Data": ReadDataExecutor,
        "DNN": DNNExecutor
    }

    def execute(self, run_id, data):
        task_name = data["task_name"]
        parameters_arguments = {}
        for parameter in data["parameters"]:
            parameters_arguments[parameter["name"]] = parameter["value"]
        return self.task_adapter[task_name].execute(run_id, parameters_arguments)
