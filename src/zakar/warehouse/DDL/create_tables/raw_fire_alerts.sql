CREATE TABLE IF NOT EXISTS raw.fire_alerts(
    fire_alerts_id SERIAL PRIMARY KEY,
    event_day INTEGER NOT NULL,
    notification_day INTEGER NOT NULL,
    geospatial_x SMALLINT NOT NULL,
    geospatial_y SMALLINT NOT NULL,
);