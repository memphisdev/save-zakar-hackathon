create table if not exists raw.tweets(
    day integer not null,
    geospatial_x smallint not null,
    geospatial_y smallint not null,
    tweet text not null
);
