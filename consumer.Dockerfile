FROM python:3.8.2
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
ADD ./consumer /consumer
WORKDIR /consumer
CMD ["python","-u", "consumer.py"]