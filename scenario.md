![GitHub README](https://github.com/memphisdev/save-zakar-hackathon/assets/70286779/608ddd4f-4b71-484f-8d10-ebed3622d13e)


# Save the Island of Zakar! #
Zakar is a distinct island with diverse ecosystems from dense jungles to mind-blowing coral reefs.<br>
Besides the nice and welcoming citizens, Zakar is home to rare and endangered species, and we're on a mission to keep them thriving.<br>
The island has been struggling with wildfires in the last few years.  As a small island nation, fires are particularly problematic.<br>
Importing materials is expensive and takes time, so they must do everything they can to protect their homes, farms, and natural resources.<br>
Similarly, with a relatively small geographic footprint, smoke can quickly pollute the air, causing health problems.

## How can you help? ##
Your chance to save Zakar is by building one or more of the following:

* A ML-powered early warning system that detects temperature or social media anomalies to generate early alerts before a wildfire spreads.
* Build a real-time dashboard to visualize the temperature or tweet data in a human-readable manner.

## The Scenario ##

The government of Zakar placed temperature sensors across the island. Their citizens are also very active on social media.  
The government contracted us to develop software to identify fires using temperature readings, social media messages, or both.  
You will receive temperature readings from multiple sensors, tweets tagged with geographic locations, and (delayed) fire notifications.
Your goal is to come up with tools for reliably detecting wildfires from these data before the official fire notifications arrive. As mentioned in the previous paragraph.

## The Data 
You will be able to receive the messages in real-time from Memphis.dev stations using one of the Memphis.dev client SDKs. 
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
Uneven distributions of sensors (because it may not be possible to place sensors everywhere due to cost or geography)
An uneven geographic sampling of tweets (because some areas have denser populations than others)
Unreliable sensor readings (because equipment malfunctions sometimes)
Sensors going offline due to dead batteries or destruction

## Getting started
### Initialization
1. Clone the hackathon repo to your local machine
2. Create a Memphis.dev account [here](https://cloud.memphis.dev)
3. Run the simulator to start receiving sensors data *instructions*
4. Create a Memphis.dev consumer that will collect ingested data and pour it into Supabase or any other database of your choice

### For early-warning system (Anomaly detection)
![Anomaly Detection Path](https://github.com/memphisdev/save-zakar-hackathon/assets/107035359/aa9f2438-bf97-437c-b2ff-6764eebf8577)

### For visualization projects
![Data Visualization Path](https://github.com/memphisdev/save-zakar-hackathon/assets/107035359/1c38a786-0f84-4b7e-acc4-cba6417fe2f1)




