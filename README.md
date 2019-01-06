# flower-classifier-app

## description 

The app predicts a flower’s name. An image of flower is uploaded and sent to the server. The server randomly selects saved models and try to predict the flower’s name using each model selected. The most predicted name is returned to the user.

The saved models come from the model saved during the last project of Pytorch Udacity Challenge. The user has the possibility to upload his model. If the model is successfully uploaded, an Id is sent to the email the user has used to upload his model. When trying to predict a flower’s name, the user has either the possibility to give a model id or not. If the Id is given, only the prediction of the model with the corresponding Id on the server will be used. 

Here is the live version of the [app](kedevked.github.io/flowers-classifier/index.html)

## frontend

### description
The frontend is written in angular. A flower is uploaded to the backend and the most likely flower's name is returned. A model can be uploaded as well.

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

        pip -r install requirements.txt

- run the server

        python -m flask run

To make predictions, the server needs to have the file `checkpoint.pth` saved from a flower classifier model written in pytorch

### docker-compose to launch the project

- install [docker compose](https://docs.docker.com/compose/install/) if not yet installed.

- run docker-compose

        docker-compose up

