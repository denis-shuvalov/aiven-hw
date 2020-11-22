FROM python:3.8.2
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
ADD ./producer /producer
WORKDIR /producer
CMD ["python","-u", "producer.py"]