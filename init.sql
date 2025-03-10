CREATE DATABASE weatherdb;

\c weatherdb

CREATE SCHEMA IF NOT EXISTS weather;

SET search_path TO weather;


CREATE TABLE IF NOT EXISTS weather.sensors (
    id TEXT PRIMARY KEY,
    location POINT,
    type TEXT,
    note TEXT,
    attached TEXT,
    install_date DATE
);

CREATE TABLE IF NOT EXISTS weather.sensordata (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP,
    humidity FLOAT,
    temperature FLOAT,
    sensor TEXT,
    FOREIGN KEY (sensor) REFERENCES weather.sensors(id) ON DELETE CASCADE,
    CONSTRAINT sensor_time_id UNIQUE (time,sensor)
);
