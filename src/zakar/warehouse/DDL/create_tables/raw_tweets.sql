create table if not exists raw.tweets (
    tweet_id serial primary key,
    day integer not null,
    geospatial_x smallint not null,
    geospatial_y smallint not null,
    text text not null
);
