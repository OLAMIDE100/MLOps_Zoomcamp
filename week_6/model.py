import os
import json
import pickle





def load_model(model_path):
    MODEL_FILE = os.getenv('MODEL_FILE',model_path )
    with open(MODEL_FILE, 'rb') as f_in:
        dv, model = pickle.load(f_in)

    return dv,model


class ModelService():
    def __init__(self,model,transformer):
        self.model = model
        self.transformer = transformer

    def prepare_features(self,ride):
        features = {}
        features['PU_DO'] ="%s_%s"%(ride['PULocationID'],ride['DOLocationID'])
        features['trip_distance'] = ride['trip_distance']
        
        return features

    def predict(self,features):
        x_pred = self.transformer.transform(features)
        pred = self.model.predict(x_pred)
        return float(pred[0])

def init(model_path):
    transformer,model = load_model(model_path)

  
    model_service = ModelService(model=model,transformer=transformer)

    return model_service
