FROM mysql:latest

COPY my.cnf /etc/my.cnf

ENV MYSQL_ROOT_PASSWORD pass
COPY ./data.sql /docker-entrypoint-initdb.d/data.sql