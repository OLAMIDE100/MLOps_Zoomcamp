import pickle
from flask import Flask, request,jsonify 

import mlflow
from mlflow.tracking import MlflowClient
MLFLOW_TRACKING_URI = "sqlite:///homework.db"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)


client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)


run_id = "a21e3fa7d16b4c6891a5563dec6821f6"
logged_model =f"runs:/{run_id}/model"

model = mlflow.pyfunc.load_model(logged_model)


path = client.download_artifacts(run_id=run_id,path="preprocessor/dv.pkl")
print("downloading the dic_vectoriser to path")





with open(path,'rb') as model_out:
    transformer = pickle.load(model_out)


def prepare(ride):
    features = {}

    features['PU_DO'] = "%s_%s" % (ride['PULocationID'],ride['DOLocationID'])

    features['trip_distance'] = ride['trip_distance']

    return features



def predict(ride):

    features = prepare(ride)



    X = transformer.transform(features)

    pred = model.predict(X)

    return float(pred[0])


app = Flask("duration_prediction")


@app.route('/predict',methods=['POST'])
def predict_endpoint():

    ride = request.get_json()

    pred = predict(ride)

    result = {
        'duration' : pred,
        'model_version' : run_id
    }


    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host = '0.0.0.0',port=9696)