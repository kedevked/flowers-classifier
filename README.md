# flower-classifier-app

## frontend

### description
The frontend is written in angular. A flower is uploaded to the backend and the most likely flower's name is returned

### development

- change directory

        cd frontend

- install all the dependencies

        npm install

- serve the frontend
     
        npm start

## backend

### description
The backend is written with the server flask. The prediction are made using pytorch.

### development

- change directory

        cd backend

- install all the dependencies

- run the server

        python -m flask run

To make predictions, the server needs to have the file `checkpoint.pth` saved from a flower classifier model written in pytorch

### docker-compose to launch the project

- install [docker compose](https://docs.docker.com/compose/install/) if not yet installed.

- run docker-compose

        docker-compose up

