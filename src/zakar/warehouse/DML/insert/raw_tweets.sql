insert into raw.tweets (day, geospatial_x, geospatial_y, text)
values (
    %(day)s,
    %(geospatial_x)s,
    %(geospatial_y)s,
    %(text)s
);
