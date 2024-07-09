FROM nginx:latest

RUN groupadd -r nginx && useradd -r -g nginx nginx

COPY nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]
