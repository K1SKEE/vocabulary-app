FROM node:latest as build

WORKDIR /app

COPY . /app

RUN npm install && \
    npm run build

FROM nginx:latest

COPY --from=build /app/build /usr/share/nginx/html

RUN rm /etc/nginx/conf.d/default.conf

COPY /nginx/nginx.conf /etc/nginx/conf.d

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]