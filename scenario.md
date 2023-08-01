![1660x498 (600x180) (1)](https://github.com/memphisdev/save-zakar-hackathon/assets/107035359/4b035dc3-75ce-44a4-902c-a5200bf7a79c)


# 🔥 Save the Island of Zakar! 🔥 #
Zakar is a distinct island with diverse ecosystems from dense jungles to mind-blowing coral reefs.<br>
Besides the nice and welcoming citizens, Zakar is home to rare and endangered species, and we're on a mission to keep them thriving.<br>
The island has been struggling with wildfires in the last few years.  As a small island nation, fires are particularly problematic.<br>
Importing materials is expensive and takes time, so they must do everything they can to protect their homes, farms, and natural resources.<br>
Similarly, with a relatively small geographic footprint, smoke can quickly pollute the air, causing health problems.

## How can you help? ##
Your chance to save Zakar is by building one or more of the following:

* An ML-powered early warning system that detects temperature or social media anomalies to generate early alerts before a wildfire spreads.
* Build a real-time dashboard to visualize the temperature or tweet data in a human-readable manner.

## The Scenario ##

The government of Zakar placed temperature sensors across the island, and luckily their citizens are also very active on social media.  
The government contracted us to develop software to identify fires using temperature readings, social media messages, or both.  
You will receive temperature readings from multiple sensors, tweets tagged with geographic locations, and (delayed) fire notifications.<br>
Your goal is to come up with tools for reliably detecting wildfires from these data before the official fire notifications arrive.

## The Data 
You will be able to receive the messages in real-time from Memphis.dev stations using one of the Memphis.dev client SDKs.<br> 
Similarly, early warnings will be sent to another Memphis.dev station.

Temperature readings are available from the `zakar-temperature-readings` station and look like so:

```json
 {
  "geospatial_x": 4,
  "geospatial_y": 5,
  "temperature": 80.2,
  "day": 23
}
```

Micro-blog posts are available from the `zakar-tweets` station and look like so:

```json
{
  "day": 728,
  "geospatial_x": 4,
  "geospatial_y": 5,
  "text": "Its gettin hot in here (so hot). I am gettin so hot, I wanna take my clothes off"
}
```

Notifications of past wildfire events are available from the `zakar-past-fire-alerts` station and look like so:
```json
{
  "event_day": 527,
  "notification_day": 530,
  "geospatial_x": 4,
  "geospatial_y": 5
}
```

You should generate early warning messages in the following format and send them to the `zakar-fire-alerts` station:

```json
{
  "event_day": 527,
  "geospatial_x": 4,
  "geospatial_y": 5
}
```

## Possible challenges you may face:
* Uneven distributions of sensors (because it may not be possible to place sensors everywhere due to cost or geography).<br>
* An uneven geographic sampling of tweets (because some areas have denser populations than others).<br>
* Unreliable sensor readings (because equipment malfunctions sometimes).<br>
* Sensors going offline due to dead batteries or destruction.

## ⭐ Getting Started - Part 2 - Choose a path
### 1. Build an early-warning system (Anomaly detection) 🔥
![Anomaly path](https://github.com/memphisdev/save-zakar-hackathon/assets/107035359/2a6afd69-ee64-42d7-82e3-41cecf8fd091)


To read the data from Memphis, you would need to consume the data from Memphis stations using a service called `consumer`.<br>
For your convenience, we provided a consumer code example within this repo called `consumer_example.py` + `mongodb_example.py`
```
$ python example_consumer.py --host <memphis_hostname> --username <client_type_username> --password <client_type_password> --account-id <memphis_account_id>
```

### 2. Visualize the data 🔥
![Data Visualization Path (2)](https://github.com/memphisdev/save-zakar-hackathon/assets/107035359/7c7efcd0-f393-4830-a167-f9e064f316cd)


To read the data from Memphis, you would need to consume the data from Memphis stations using a service called `consumer` and store it in a [Streamlit-supported database](https://docs.streamlit.io/knowledge-base/tutorials/databases) (For example, Supabase) for further visualization through Streamlit.<br>
Please pay attention that for the visualization path, it is mandatory to use Streamlit (Community cloud).

For your convenience, we provided a consumer code example within this repo called `consumer_example.py` + `mongodb_example.py`
```
$ python example_consumer.py --host <memphis_hostname> --username <client_type_username> --password <client_type_password> --account-id <memphis_account_id>
```

## FAQ ⁉️
###  Is it possible to repeat already sent messages?
You can either use a different consumer name (so a different consumer is created) or delete the consumer and recreate it.

### Is the data always going to be the same? (or be streaming new data live)?
There won't be changes in the datasets.

