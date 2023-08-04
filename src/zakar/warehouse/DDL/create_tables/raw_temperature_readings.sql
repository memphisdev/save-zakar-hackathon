create table if not exists raw.temperature_readings(
    temperature_readings_id serial primary key,
    geospatial_x smallint not null,
    geospatial_y smallint not null,
    temperature smallint not null,
    day integer not null
);
