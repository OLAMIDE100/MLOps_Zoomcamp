import os


def get_input_path(year, month):
    default_input_pattern = "s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    return input_pattern.format(year=year, month=month)


def get_output_path(year, month):
    default_output_pattern = "s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern.format(year=year, month=month)


def main(year, month,num):
    input_file = get_input_path(year, month)
    output_file = get_output_path(year, month)
    
    if num == 1:
        return input_file
    elif num== 2:
        return output_file
    else:
        return "input number between 1 and 2, with 1 for input and 2 for output"
