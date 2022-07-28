import pandas as pd
from datetime import datetime
import helper
import int_batch

def save_read_data(year,month,num):

    def dt(hour, minute, second=0):
        return datetime(2021, 1, 1, hour, minute, second)


    data = [
        (None, None, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2, 0), dt(1, 2, 50)),
        (1, 1, dt(1, 2, 0), dt(2, 2, 1)),        
    ]

        

    columns = ['PUlocationID', 'DOlocationID', 'pickup_datetime', 'dropOff_datetime']

    df_input = pd.DataFrame(data, columns=columns)

    options = {
        'client_kwargs': {
            'endpoint_url': "http://localhost:4566"
        }
    }

    
    
    if num == 1:

        input_file = helper.main(year,month,num)

        df_input.to_parquet(
            input_file,
            engine='pyarrow',
            compression=None,
            index=False,
            storage_options=options
        )
      
        return "successfully added file to s3 bucket"

    else:
        input_file = helper.main(year,month,1)

        df_input.to_parquet(
            input_file,
            engine='pyarrow',
            compression=None,
            index=False,
            storage_options=options
        )

        output_file = helper.main(year,month,2)

        int_batch.main(year,month,input_file,output_file,storage_options=options)



       



if __name__ == "__main__":
    save_read_data(2021,1,2)
