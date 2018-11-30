# FROM ubuntu:18.04
FROM continuumio/miniconda3

COPY backend /app

# RUN apt-get -y update && \
#    apt-get -y install wget && \
#    wget https://repo.anaconda.com/archive/Anaconda3-5.3.1-Linux-x86_64.sh

# RUN chmod +x Anaconda3-5.3.1-Linux-x86_64.sh && \
#    ./Anaconda3-5.3.1-Linux-x86_64.sh -b -u && \
#    export PATH=~/anaconda3/bin:$PATH
#    sh ~/.bashrc
#    export PATH=~/anaconda3/bin:$PATH

RUN conda upgrade conda
RUN conda install -y numpy && \
    conda install -y nb_conda
RUN conda install -y pytorch torchvision -c pytorch
RUN conda install -y -c anaconda pip

WORKDIR /app

RUN pip install flask
RUN pip install matplotlib
RUN pip install flask_cors
RUN pip install argparse
RUN pip install Pillow

# RUN pip install -r requirements.txt

ENTRYPOINT python -m flask run
