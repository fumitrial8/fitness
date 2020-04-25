FROM python:3.6
RUN apt-get update && apt-get install -y \
    default-jdk \
    build-essential \
    gfortran \
    libblas-dev \
    liblapack-dev \
    libxft-dev \
    swig \
    && rm -rf /var/lib/apt/lists/*
VOLUME /fitness
WORKDIR /fitness

COPY . /fitness

RUN pip3 install --upgrade pyzmq --install-option="--zmq=bundled"
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade -r requirements.txt

EXPOSE 5000
# CMD ["python3", "run.py"]
ENTRYPOINT python3 run.py --ip=0.0.0.0 --allow-root