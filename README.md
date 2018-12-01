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

        pip3 install -r requirements.txt

- run the server

        python -m flask run

To make predictions, the server needs to have the file `checkpoint.pth` saved from a flower classifier model written in pytorch

### dockerfile to launch the server

- build the image

        docker build . -t server

- run the container

        docker run -d -p 5000:5000 server

