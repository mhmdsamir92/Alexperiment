Alexperiment
============

An application helps you to run many experiments with different parameters in parallel. You just need to feed into 
application your experiment flow and parameters (using a web service) and you can track the results of your experiment
using a unique identifier will be provided by the application

just calling a post service like the following::

    
    POST /alexperiment/start_alexperiment HTTP/1.1
    Host: localhost:8000
    Authorization: ApiKey admin:ABC123
    Content-Type: application/json
    Cache-Control: no-cache
    Postman-Token: 1deb1b8c-9c8e-4117-b2eb-8f02f3a45de8

    {
    "workflows": [{
            "DataPhase": [{
                "task_name": "Data",
                "parameters": [{
                    "name": "path",
                    "possible_values": ["/home/mohamedsamir/Alexperiment/Data/Mylyn--CK.csv"]
                }]
            }],
            "ClassificationPhase": [{
                "task_name": "DNN",
                "parameters": [{
                    "name": "nb_epoch",
                    "possible_values": ["100"]
                }, {
                    "name": "batch_size",
                    "possible_values": ["10"]
                }, {
                    "name": "n_splits",
                    "possible_values": ["10"]
                }, {
                    "name": "scoring",
                    "possible_values": ["roc_auc", "accuracy"]
                }]
            }]
        }]
    }


will initiate a new run for you and an id will be provided to get the results of your run.
The response of this service will be like the following::

    {
        "run_id": 18
    }

To get the results of your run you can call the following GET service::

    GET /alexperiment/run_results?id=18 HTTP/1.1
    Host: localhost:9002
    Authorization: ApiKey admin:ABC123
    Content-Type: application/json
    Cache-Control: no-cache
    Postman-Token: ecb48c20-a480-4625-9f30-d2e9854cf1d8

The output of this service will be something like this::

    {
        "results": [
            [
                {
                    "description": {
                        "DataPhase": {
                            "Data": {
                                "path": "/home/mohamedsamir/Alexperiment/Data/Mylyn--CK.csv"
                            }
                        },
                        "ClassificationPhase": {
                            "DNN": {
                                "nb_epoch": "100",
                                "batch_size": "10",
                                "n_splits": "10",
                                "scoring": "roc_auc"
                            }
                        }
                    },
                    "results": {
                        "MEAN": "0.4273460688086292",
                        "STD": "0.0661907786255272"
                    }
                },
                {
                    "description": {
                        "DataPhase": {
                            "Data": {
                                "path": "/home/mohamedsamir/Alexperiment/Data/Mylyn--CK.csv"
                            }
                        },
                        "ClassificationPhase": {
                            "DNN": {
                                "nb_epoch": "100",
                                "batch_size": "10",
                                "n_splits": "10",
                                "scoring": "accuracy"
                            }
                        }
                    },
                    "results": {
                        "MEAN": "0.79163271776175",
                        "STD": "0.051743500958311144"
                    }
                }
            ]
        ]
    }



Tests
------
WIP


Deployment
----------

WIP



Docker
^^^^^^

WIP


:License: MIT
