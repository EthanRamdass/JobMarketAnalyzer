# frontend/Dockerfile
FROM nginx:stable-alpine

COPY index.html /usr/share/nginx/html/index.html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

FROM node:18

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install

COPY . .
CMD ["npm", "start"]
