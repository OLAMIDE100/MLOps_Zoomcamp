import pickle
import pandas as pd
import sys







with open('./lin_reg.bin', 'rb') as f_in:
    dv, lr = pickle.load(f_in)




categorical = ['PUlocationID', 'DOlocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


def ride_duration_prediction(year,month):
    output_file = f's3://nyc-duration-prediction-mide/homework/taxi_type=fhv/year={year:04d}/month={month:02d}.parquet'
    input_file = f'https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_{year:04d}-{month:02d}.parquet'
    df = read_data(input_file)

    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    print(y_pred.mean())

    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    result_df = pd.DataFrame()
    result_df['ride_id'] = df['ride_id']
    result_df['Prediction'] = y_pred

   


    result_df.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )

def run():
  
    year = int(sys.argv[1]) # 2021
    month = int(sys.argv[2]) # 3

    ride_duration_prediction(year,month)


if __name__ == '__main__':
    run()




