FROM mysql:8.0.36
COPY ./database/ /docker-entrypoint-initdb.d/
ENV MYSQL_DATABASE starstoneapp
ENV MYSQL_PORT 3306
ENV MYSQL_ROOT_HOST %
ENV MYSQL_ALLOW_EMPTY_PASSWORD true