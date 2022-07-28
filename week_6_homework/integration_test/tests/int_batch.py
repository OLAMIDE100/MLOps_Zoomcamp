import sys
import pickle
import pandas as pd


def prepare_data(df):

    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    return df

def read_data(filename,categorical,storage_options):

    df = pd.read_parquet(filename,storage_options=storage_options,engine='pyarrow')
    
    t_df = prepare_data(df)

    t_df[categorical] = t_df[categorical].fillna(-1).astype('int').astype('str')

    return t_df

def main(year,month,input_file,output_file,storage_options):

    with open('model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)

    print("successfully losded the model and transformer")


    categorical = ['PUlocationID', 'DOlocationID']

    df = read_data(input_file,categorical,storage_options)

    print('successfully transformed the data to dataframe')

    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')


    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)


    print('predicted mean duration:', y_pred.sum())

    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred

    df_result.to_parquet(output_file, engine='pyarrow', index=False,storage_options=storage_options)

