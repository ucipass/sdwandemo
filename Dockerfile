FROM python:alpine
COPY sdwan.py /app/
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
# CMD python ./sdwan.py
# ENTRYPOINT ["python"]
# CMD ["-u", "./sdwan.py"]
ENTRYPOINT ["tail"]
CMD ["-f", "/dev/null"]