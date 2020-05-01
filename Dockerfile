FROM python:alpine3.7
COPY sdwan.py /app/
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
CMD python ./sdwan.py