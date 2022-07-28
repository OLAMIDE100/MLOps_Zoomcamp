import model




def test_prepare_features():

    model_service = model.ModelService(None,None)


    rides = {
            'PULocationID': 10,
            'DOLocationID': 50,
            'trip_distance': 40

            }


    actual_result = model_service.prepare_features(rides)

    expected_result = {
        'PU_DO': "10_50",
        'trip_distance' : 40
    }

    assert actual_result == expected_result


def test_predict():

    model_service = model.ModelService(None,None)


    rides = {
            'PULocationID': 10,
            'DOLocationID': 50,
            'trip_distance': 40

            }


    actual_result = model_service.prepare_features(rides)

    expected_result = {
        'PU_DO': "10_50",
        'trip_distance' : 40
    }

    assert actual_result == expected_result