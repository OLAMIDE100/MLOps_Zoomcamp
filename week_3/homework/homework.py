import pandas as pd
import pickle

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


from prefect.deployments import DeploymentSpec
from prefect.orion.schemas.schedules import IntervalSchedule
from prefect.flow_runners import SubprocessFlowRunner
from prefect.orion.schemas.schedules import CronSchedule
from prefect.task_runners import SequentialTaskRunner


from dateutil.relativedelta import relativedelta
import requests as rq
import datetime


from prefect import flow, task,get_run_logger

@task
def get_paths(date):

    logger = get_run_logger()
    

    paths = []
    
    for i in range(1,3):
    
        new_date = (pd.to_datetime(date) - relativedelta(months=i)).strftime("%Y-%m")
        
        url = f"https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_{new_date}.parquet"
        response = rq.get(url)
        
        path = f"data/fhv_tripdata_{new_date}.parquet"
        
        with open(path, mode='wb') as file:
            file.write(response.content)

        logger.info(f"sucessfully download fhv_tripdata_{new_date}.parquet")
        
        
        paths.append(path)
        
    return paths[0],paths[1]

@task
def read_data(path):
    df = pd.read_parquet(path)
    return df



@task
def prepare_features(df, categorical, train=True):
    logger = get_run_logger()

    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    mean_duration = df.duration.mean()
    if train:
        logger.info(f"The mean duration of training is {mean_duration}")
    else:
        logger.info(f"The mean duration of validation is {mean_duration}")
    
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df



@task
def train_model(df, categorical):
    logger = get_run_logger()

    train_dicts = df[categorical].to_dict(orient='records')
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts) 
    y_train = df.duration.values

    logger.info(f"The shape of X_train is {X_train.shape}")
    logger.info(f"The DictVectorizer has {len(dv.feature_names_)} features")

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_train)
    mse = mean_squared_error(y_train, y_pred, squared=False)
    logger.info(f"The MSE of training is: {mse}")
    return lr, dv


@task
def run_model(df, categorical, dv, lr):
    logger = get_run_logger()
    val_dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(val_dicts) 
    y_pred = lr.predict(X_val)
    y_val = df.duration.values

    mse = mean_squared_error(y_val, y_pred, squared=False)
    logger.info(f"The MSE of validation is: {mse}")
    return


@flow(task_runner=SequentialTaskRunner())
def main_ml_flow(date : str = None):

    if date is None:
        date = datetime.date.today()
       
    
    val_path,train_path = get_paths(date).result()
    

    categorical = ['PUlocationID', 'DOlocationID']

    df_train = read_data(train_path).result()
    df_train_processed = prepare_features(df_train, categorical).result()

    df_val = read_data(val_path).result()
    df_val_processed = prepare_features(df_val, categorical, False).result()

    # train the model
    lr, dv = train_model(df_train_processed, categorical).result()

    with open(f'models/dv-{date}.bin', 'wb') as f_out:
        pickle.dump(dv, f_out)

    with open(f'models/model-{date}.bin', 'wb') as f_out:
        pickle.dump(lr, f_out)

    run_model(df_val_processed, categorical, dv, lr)






DeploymentSpec(
    flow=main_ml_flow,
    name="homework_model_training",
    schedule=CronSchedule(
        cron="0 9 15 * *"),
    flow_runner=SubprocessFlowRunner(),
    tags=["ml"]
)
