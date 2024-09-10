CREATE DATABASE carcollector;

CREATE USER car_admin WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE carcollector TO car_admin;