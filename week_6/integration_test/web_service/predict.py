import pickle
from flask import Flask, request,jsonify 


with open('lin_reg.bin','rb') as model_out:
    (transformer,model) = pickle.load(model_out)


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
        'duration' : pred
    }


    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host = '0.0.0.0',port=9696)