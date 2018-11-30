FROM ubuntu:18.04

COPY backend /app

RUN apt-get -y update && \
    apt-get -y install wget && \
    wget https://repo.anaconda.com/archive/Anaconda3-5.3.1-Linux-x86_64.sh

RUN chmod +x Anaconda3-5.3.1-Linux-x86_64.sh && \
    ./Anaconda3-5.3.1-Linux-x86_64.sh -b -u

RUN conda upgrade -y conda && \
    conda upgrade -y --all && \
    conda install -y numpy && \
    conda install -y nb_conda && \
    conda install -y pytorch torchvision -c pytorch && \
    apt-get install -y python-pip python-dev build-essential && \
    pip install -y -r requirements.txt

WORKDIR /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]