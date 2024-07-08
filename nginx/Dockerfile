FROM nginx:1.15.8

RUN rm /etc/nginx/conf.d/default.conf
COPY project.conf /etc/nginx/conf.d/
COPY fullchain.pem /root/ssl/fullchain.pem
COPY privkey.pem /root/ssl/privkey.pem
