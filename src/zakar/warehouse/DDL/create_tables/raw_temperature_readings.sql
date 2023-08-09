create table if not exists raw.temperature_readings(
    day integer not null,
    geospatial_x smallint not null,
    geospatial_y smallint not null,
    temperature smallint not null
);
