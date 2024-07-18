FROM node:18-alpine

WORKDIR /frontend-app
COPY package.json /frontend-app/
RUN npm install --omit=dev
COPY . /frontend-app
RUN npm run build


CMD node server.js
