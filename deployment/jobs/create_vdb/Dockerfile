FROM python:latest

COPY \
    ./requirements.tx[t] \
    .

RUN pip install -r requirements.txt

# Copy everything else
COPY . .


CMD [ "python", "./main.py"]

