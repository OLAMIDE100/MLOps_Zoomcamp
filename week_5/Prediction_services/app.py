from crypt import methods
import os
import pickle
import requests



from pymongo import MongoClient

from flask import Flask,jsonify,request


MODEL_FILE = os.getenv('MODEL_FILE', 'lin_reg.bin')

EVIDENTLY_SERVICE_ADDRESS = os.getenv('EVIDENTLY_SERVICE', 'http://127.0.0.1:5000')
MONGODB_ADDRESS = os.getenv("MONGODB_ADDRESS", "mongodb://127.0.0.1:27017")


with open(MODEL_FILE,'rb') as fin:
    transformer,model = pickle.load(fin)

app = Flask('duration')
mongo_client = MongoClient(MONGODB_ADDRESS)
db = mongo_client.get_database('prediction_service')
collection = db.get_collection('data')



def save_to_db(record,Prediction):
    rec = record.copy()
    rec['prediction'] = Prediction
    collection.insert_one(rec) 

def save_to_evidently_services(record,Prediction):
    rec = record.copy()
    rec['prediction'] = Prediction
    requests.post(f"{EVIDENTLY_SERVICE_ADDRESS}/iterate/taxi", json=[rec])


@app.route('/predict',methods=['POST'])
def predict():
    record = request.get_json()
    record['PU_DO'] =  "%s_%s" % (record['PULocationID'],record['DOLocationID'])
    X = transformer.transform([record])
    y_pred = model.predict(X)

    Prediction = float(y_pred)

    result = {
        'duration' : Prediction
    }

    save_to_db(record,Prediction)
    save_to_evidently_services(record,Prediction)

    return jsonify(result)



if __name__ == "__main__":
    app.run(debug=True, host = '0.0.0.0',port=9696)




