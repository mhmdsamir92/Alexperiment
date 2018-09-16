from lab.executers.base_executor import BaseExecutor
import numpy
from lab.models.result import Result
import json


class ReadDataExecutor(BaseExecutor):
    @staticmethod
    def execute(run_id, params):
        datasetName = params["path"]
        dataset = numpy.loadtxt(datasetName, delimiter=",")
        numberOfMetrics = dataset.shape[1] - 1
        X = dataset[:, 0:numberOfMetrics]
        Y = dataset[:, numberOfMetrics]
        x_result = Result()
        x_result.wf_perm_id = run_id
        x_result.key = "X"
        x_result.value = json.dumps(X.tolist())
        x_result.save()
        y_result = Result()
        y_result.wf_perm_id = run_id
        y_result.key = "Y"
        y_result.value = json.dumps(Y.tolist())
        y_result.save()
