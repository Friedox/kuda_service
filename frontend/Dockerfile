FROM node:18-alpine
WORKDIR /frontend-app
COPY package.json /frontend-app
RUN npm install --omit=dev
RUN npm install -g serve
COPY . /frontend-app
RUN npm run build


CMD serve --cors -l 3001 /frontend-app/build
