insert into raw.tweets (day, geospatial_x, geospatial_y, tweet)
values (
    %(day)s,
    %(geospatial_x)s,
    %(geospatial_y)s,
    %(tweet)s
);
