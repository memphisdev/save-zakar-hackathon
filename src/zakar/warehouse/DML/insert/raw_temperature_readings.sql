insert into raw.temperature_readings (geospatial_x, geospatial_y, day, temperature)
values (
    %(geospatial_x)s,
    %(geospatial_y)s,
    %(day)s,
    %(temperature)s
);
