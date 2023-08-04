CREATE TABLE IF NOT EXISTS raw.tweets(
    tweet_id SERIAL PRIMARY KEY,
    day INTEGER NOT NULL,
    geospatial_x SMALLINT NOT NULL,
    geospatial_y SMALLINT NOT NULL,
    tweet TEXT NOT NULL,
);