# About #
Zakar is a distinct island with diverse ecosystems from dense jungles to mind-blowing coral reefs. 
Besides the nice and welcoming citizens, Zaksr is home to rare and endangered species, and we're on a mission to keep them thriving.
The island has been struggling with wildfires in the last few years.  As a small island nation, fires are particularly problematic. 
Importing materials is expensive and takes time, so they must do everything they can to protect their homes, farms, and natural resources.  
Similarly, with a relatively small geographic footprint, smoke can quickly pollute the air, causing health problems.

## How can you help? ##
Your chance to save Zakar is by building Wildfire Early Warning System!

Early warning systems can be implemented in several ways.  Some systems use weather forecasts.  Some systems employ satellite imagery.  Others use on-the-ground temperature and gas sensors.  
Researchers have even explored detecting wildfires from social media activity.

## The Scenario ##

The government of Zakar placed temperature sensors across the island. Their citizens are also very active on social media.  
The government contracted us to develop software to identify fires using temperature readings, social media messages, or both.  
You will receive temperature readings from multiple sensors, tweets tagged with geographic locations, and (delayed) fire notifications.
Your goal is to come up with tools for reliably detecting wildfires from these data before the official fire notifications arrive.

You will be able to receive the messages in real time from Memphis.dev station using one of the Memphis.dev client SDKs. 
Similarly, early warnings will be sent to another Memphis.dev station.  The government has an alerting system in place so that early warnings are sent to the people of Zakar.

A message from a temperature sensor would look like so:
 {
  "sensor_id": 123,
  "sensor_latitude": 25.6,
  "sensor_longitude": 75.4,
  "temperature": 80.2,
  "timestamp": 1281237
}

A message indicating a wildfire event had occurred would look like so:

{
  "event_id": 527,
  "incidence_type": "wildfire",
  "start_timestamp": 1281237,
  "end_timestamp": 1281900,
  "event_region": {
    "min_latitude": 25.6,
    "max_latitude": 27.6,
    "min_longitude": 75.4,
    "max_longitude": 76.0
  }
}

An alert indicating that a fire was put out would look like so:

>{
  "alert_id": 527,
  "event_type": "wildfire",
  "state": "resolved",
  "timestamp": 1281237
}

An alert from your early warning system indicating the first detection of a fire would look like so:

{
  "alert_id": 527,
  "event_type": "wildfire",
  "state": "activated",
  "timestamp": 1281237,
  "event_region": {
    "center_latitude": 25.6,
    "center_longitude": 75.4,
    "radius": 5.0
  }
}

## Possible challenges you may face: ##
Uneven distributions of sensors (because it may not be possible to place sensors everywhere due to cost or geography)
An uneven geographic sampling of tweets (because some areas have denser populations than others)
Unreliable sensor readings (because equipment malfunctions sometimes)
Sensors going offline due to dead batteries or destruction

