import model
import json



model_path = './lin_reg.bin'


def test_predict(model_path):

    model_service = model.init(model_path)



    rides = {
            'PULocationID': 10,
            'DOLocationID': 50,
            'trip_distance': 40

            }

    features = model_service.prepare_features(rides)

    x_pred = model_service.predict(features)

    return x_pred



print(test_predict(model_path))

