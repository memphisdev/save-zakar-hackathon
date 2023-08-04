create table if not exists raw.fire_alerts (
    fire_alerts_id serial primary key,
    event_day integer not null,
    notification_day integer not null,
    geospatial_x smallint not null,
    geospatial_y smallint not null
);
