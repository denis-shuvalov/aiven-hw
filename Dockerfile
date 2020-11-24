FROM python:3.8.2
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
ADD . /aiven-hw
WORKDIR /aiven-hw
EXPOSE 8080
CMD ["make", "run"]