from lab.executers.base_executor import BaseExecutor
import numpy
import json
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from lab.models.result import Result


class DNNExecutor(BaseExecutor):

    @staticmethod
    def execute(run_id, params):
        x_data = json.loads(Result.objects.get(wf_perm_id=run_id, key="X").value)
        y_data = json.loads(Result.objects.get(wf_perm_id=run_id, key="Y").value)
        numberOfMetrics = len(x_data[0])
        batch_size = int(params["batch_size"])
        nb_epoch = int(params["nb_epoch"])
        n_splits = int(params["n_splits"])
        scoring = params["scoring"]
        estimator = KerasClassifier(
            build_fn=lambda: create_baseline(numberOfMetrics),
            nb_epoch=nb_epoch,
            batch_size=batch_size,
            verbose=0)
        kfold = StratifiedKFold(n_splits=n_splits, shuffle=True)
        results = cross_val_score(
            estimator, numpy.array(x_data), numpy.array(y_data), cv=kfold, scoring=scoring)
        Result.objects.create(
            wf_perm_id=run_id,
            key="MEAN",
            value=results.mean(),
            is_final_result=True,
        )

        Result.objects.create(
            wf_perm_id=run_id,
            key="STD",
            value=results.std(),
            is_final_result=True,
        )


def create_baseline(numberOfMetrics):
    model = Sequential()
    model.add(Dense(10, input_dim=numberOfMetrics, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model
