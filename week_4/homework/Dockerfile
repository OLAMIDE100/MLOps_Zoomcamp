FROM python:3.8

RUN pip install -U pip
RUN pip install pipenv 
RUN pip3 --no-cache-dir install --upgrade awscli

WORKDIR /app

COPY [ "starter.py","models/lin_reg.bin","Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy




ENV AWS_ACCESS_KEY_ID=Your_AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=YourAWS_SECRET_ACCESS_KEY



RUN aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID; aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY





ENTRYPOINT ["python","./starter.py","2021","4"]