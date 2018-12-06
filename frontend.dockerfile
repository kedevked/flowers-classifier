# base image
FROM node:9.6.1

# set working directory
RUN mkdir /usr/src
WORKDIR /usr/src/frontend

# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /usr/src/app/frontend/package.json
RUN npm install
RUN npm install -g @angular/cli@1.7.1

# add app
COPY . /usr/src/frontend

# start app
CMD ng serve --host 0.0.0.0