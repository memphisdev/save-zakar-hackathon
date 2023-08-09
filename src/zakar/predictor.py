# %%
import pickle

import numpy as np

# %%
import pandas as pd

common_cols = ["day", "geospatial_x", "geospatial_y"]
word_predictors = ["forest fire", "firefighter", "stay safe"]
weak_word_predictors = ["remember", "flame", "leave"]


def join_tweets(tweets):
    return tweets.groupby(common_cols)["tweet"].apply(" ".join).reset_index()


# %%
def tweets_when_fire(tweets):
    return (
        tweets[tweets["tweet"].str.contains("|".join(word_predictors))]
        .drop_duplicates()
        .reset_index()
    )


# %%
def tweets_when_no_fire(tweets):
    return tweets[
        ~tweets["tweet"].str.contains("|".join(word_predictors))
    ].reset_index()


# %%
def add_weak_word_predictors(tweets):
    return tweets.assign(
        **{
            word: np.where(tweets["tweet"].str.contains(word), 1, 0)
            for word in weak_word_predictors
        }
    ).drop(columns="tweet")


# %%
def filter_temp(temp, tweets=None):
    filtered_temp = temp.query("temperature >= 110")
    if tweets is None:
        return filtered_temp
    return (
        filtered_temp.merge(
            tweets.pipe(join_tweets).pipe(tweets_when_no_fire),
            # .pipe(add_weak_word_predictors),
            on=common_cols,
            how="left",
        )
        .drop(columns="tweet")
        .dropna()
    )


# %%
def label_hot(temp):
    return temp.assign(very_hot=np.where(temp["temperature"] > 125, 1, 0))


# %%
def count_locs(temp):
    return temp.merge(
        temp[common_cols]
        .rename({"day": "n_occurences"}, axis=1)
        .groupby(["geospatial_x", "geospatial_y"])
        .count()
        .reset_index(),
        how="left",
    )


# %%
def lgbm_prediction(features):
    filename = "lgbm_classifier.pkl"
    model = pickle.load(open(filename, "rb"))
    return features.loc[model.predict(features) == 1, common_cols]


# %%
def fire_prediction(tweets, temperature_readings):
    tweets, temperature_readings = pd.DataFrame(tweets), pd.DataFrame(
        temperature_readings
    )
    alerts = tweets.pipe(join_tweets).pipe(tweets_when_fire)[common_cols]
    temp_filtered = (
        temperature_readings.pipe(filter_temp, tweets)
        .pipe(label_hot)
        .pipe(count_locs)
        .drop(columns=["index"])
    )
    if not temp_filtered.empty:
        alerts = pd.concat([lgbm_prediction(temp_filtered), alerts])

    return alerts.sort_values(common_cols).to_dict(orient="records")


if __file__ == "__main__":
    print()
