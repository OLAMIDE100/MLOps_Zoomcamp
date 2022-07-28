import tests.batch
import pandas as pd
from datetime import datetime
from deepdiff import DeepDiff
import pytest


def dt(hour, minute, second=0):
    return datetime(2021, 1, 1, hour, minute, second)



expected_result = [
        ( float('nan'),  float('nan'), pd.Timestamp(dt(1, 2)), pd.Timestamp(dt(1, 10)),8.000000000000002),
        (float(1),float(1),pd.Timestamp(dt(1, 2)),pd.Timestamp(dt(1, 10)),8.000000000000002)       
    ]


@pytest.fixture
def df():
    
    data = [
        (None, None, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2, 0), dt(1, 2, 50)),
        (1, 1, dt(1, 2, 0), dt(2, 2, 1)),        
    ]

    

    columns = ['PUlocationID', 'DOlocationID', 'pickup_datetime', 'dropOff_datetime']
    return pd.DataFrame(data, columns=columns)


def test_prepare_data(df):

    

    t_df = tests.batch.prepare_data(df)

    actual_result = list(t_df.itertuples(index=False,name=None))

    diff = DeepDiff(actual_result,expected_result, significant_digits=1)

    assert 'type_changes' not in diff
    assert 'values_changed' not in diff