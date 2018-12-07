# FROM ubuntu:18.04
FROM continuumio/miniconda3

COPY backend /app

RUN conda upgrade conda
RUN conda install -y numpy && \
    conda install -y nb_conda
RUN conda install -y -c pytorch torchvision
RUN conda install -y -c anaconda pip

WORKDIR /app

RUN pip install flask
RUN pip install matplotlib
RUN pip install flask_cors
RUN pip install argparse
RUN pip install Pillow

ENTRYPOINT ["python"]

CMD ["app.py"]
