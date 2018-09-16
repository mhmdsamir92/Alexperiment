from celery import shared_task
# import numpy
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.wrappers.scikit_learn import KerasClassifier
# from sklearn.model_selection import cross_val_score
# from sklearn.model_selection import StratifiedKFold
# from sklearn.ensemble import RandomForestClassifier
# from sklearn import preprocessing
# import os
import json
# from Alexperiment.settings import BASE_DIR
from lab.models.workflow import Workflow
from copy import deepcopy
from lab.models.workflow_perm import WorkflowPerm


# def create_baseline(numberOfMetrics):
#     model = Sequential()
#     model.add(Dense(10, input_dim=numberOfMetrics, activation='relu'))
#     model.add(Dense(1, activation='sigmoid'))
#     model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#     return model


# def prepareData(inputData, normalizeFun=preprocessing.normalize):
#     return normalizeFun(inputData)


@shared_task
def execute_atomic_workflow(wf_perm_id, data):
    wf_perm = WorkflowPerm.objects.get(id=wf_perm_id)
    return wf_perm.execute(data)


@shared_task
def execute_workflow(data, wf_id, run_id):
    inner_workflows = []
    for phase in data:
        tasks_list = []
        for task in data[phase]:
            one_task = {}
            one_task[phase] = {"task_name": task["task_name"]}
            params = []
            for parameter in task["parameters"]:
                params_to_add = []
                for value in parameter["possible_values"]:
                    new_param = {"name": parameter["name"], "value": value}
                    params_to_add.append([new_param])
                if not params:
                    params.extend(params_to_add)
                else:
                    new_params = []
                    for param_to_add in params_to_add:
                        temp = deepcopy(params)
                        for param in temp:
                            param.extend(param_to_add)
                        new_params.extend(temp)
                    params = new_params

            for param in params:
                new_task = deepcopy(one_task)
                new_task[phase]["parameters"] = param
                tasks_list.append(new_task)

        if not inner_workflows:
            inner_workflows.extend(tasks_list)
        else:
            new_workflows = []
            for task_to_add in tasks_list:
                temp = deepcopy(inner_workflows)
                for item in temp:
                    item.update(task_to_add)
                new_workflows.extend(temp)
            inner_workflows = new_workflows
    for workflow in inner_workflows:
        description = get_workflow_description(workflow)
        wf_perm = WorkflowPerm.objects.create(
            workflow_id=wf_id,
            description=description
        )
        execute_atomic_workflow.delay(wf_perm.id, workflow)


@shared_task
def execute_all_workflows(workflows, run_id):
    '''
        This method should retrieve all workflows json, execute/delay each workflow
        Example for a json
        {
            "workflows":[{
                "DataPhase": [{
                    "task_name": "Data",
                    "parameters": [{
                        "name": "name1",
                        "possible_values": [v1, v2, v3]
                    }, {
                        "name": "name2",
                        "possible_values": [vv1, vv2, vv3]
                    }]
                }]
            }],
        }
    '''
    # workflows = [{
    #     "DataPhase": [{
    #         "task_name": "Data",
    #         "parameters": [{
    #             "name": "path",
    #             "possible_values": [os.path.join(BASE_DIR, "Data", "Mylyn--CK.csv")]
    #         }]
    #     }],
    #     "ClassificationPhase": [{
    #         "task_name": "DNN",
    #         "parameters": [{
    #             "name": "nb_epoch",
    #             "possible_values": ["100"]
    #         }, {
    #             "name": "batch_size",
    #             "possible_values": ["10"]
    #         }, {
    #             "name": "n_splits",
    #             "possible_values": ["10"]
    #         }, {
    #             "name": "scoring",
    #             "possible_values": ["roc_auc", "accuracy"]
    #         }]
    #     }]
    # }]
    for workflow in workflows:
        wf_id = Workflow.objects.create(
            run_id=run_id
        ).id
        execute_workflow.delay(workflow, wf_id, run_id)

# def dummy_function():
#     print("New workflow execution started")
#     numberOfMetrics = 7  # int(sys.argv[2])
#     datasetName = os.path.join(BASE_DIR, "Data", "Mylyn--CK.csv")  # sys.argv[1]
#     print("Dataset name is ", datasetName)
#     print("Number of metrics is ", numberOfMetrics)
#     dataset = numpy.loadtxt(datasetName, delimiter=",")
#     X = dataset[:, 0:numberOfMetrics]
#     Y = dataset[:, numberOfMetrics]
#     # X = prepareData(X)
#     estimator = KerasClassifier(build_fn=lambda: create_baseline(numberOfMetrics), nb_epoch=100, batch_size=10, verbose=0)
#     kfold = StratifiedKFold(n_splits=10, shuffle=True)
#     results = cross_val_score(estimator, X, Y, cv=kfold, scoring='roc_auc')
#     print(results)
#     print(results.std())
#     print("Results = ", results.mean())
#     return {"results_mean": results.mean(), "results_std": results.std()}


def get_workflow_description(workflow):
    description = {}
    for phase in workflow:
        desc = {}
        task_name = workflow[phase]["task_name"]
        desc[task_name] = {}
        for param in workflow[phase]["parameters"]:
            parameter_name = param["name"]
            parameter_value = param["value"]
            desc[task_name][parameter_name] = parameter_value
        description[phase] = desc
    return json.dumps(description)
