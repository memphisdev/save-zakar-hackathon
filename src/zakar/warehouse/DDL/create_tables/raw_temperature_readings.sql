CREATE TABLE IF NOT EXISTS raw.temperature_readings(
    temperature_readings_id SERIAL PRIMARY KEY,
    geospatial_x SMALLINT NOT NULL,
    geospatial_y SMALLINT NOT NULL,
    temperature SMALLINT NOT NULL,
    day INTEGER NOT NULL,
);