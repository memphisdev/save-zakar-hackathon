from zakar.config import RAW_PATH, DataName, Producer, StationName


def main():
    tweets = Producer(StationName.TWEETS, data_name=DataName.TWEETS)
    fire_alerts = Producer(StationName.FIRE_ALERTS, data_name=DataName.FIRE_ALERTS)
    temperature_readings = Producer(
        StationName.TEMPERATURE_READINGS, data_name=DataName.TEMPERATURE_READINGS
    )
    producers = [tweets, fire_alerts, temperature_readings]
    for producer in producers:
        producer.raw_data.to_csv(RAW_PATH / f"{producer.data_name}.csv", index=False)


if __name__ == "__main__":
    main()
