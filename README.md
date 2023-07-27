![GitHub README](https://github.com/memphisdev/save-zakar-hackathon/assets/70286779/dc56d45f-8861-49b0-9796-05f33ea8a9d4)

A fictional island nation named Zakar is suffering from wildfires.<br>
Let's help them build an early warning system and save lives and earth!

# Save Zakar Hackathon
In collaboration with [Streamlit](https://github.com/streamlit/streamlit) & [Supabase](https://github.com/supabase),<br>
we are happy to announce Memphis #1 hackathon **#SaveZakar**!<br>

## The story
Wildfires wreak havoc every year.<br>
They take human and animal lives. They destroy agricultural and industrial crops and cause famines.<br>
They damage the environment, contribute to global warming, and generate smoke that pollutes the air.<br>
Their overall impact runs into billions of dollars and includes incalculable harm to people and animals.<br>
<br>
In this hackathon, you are going to build a wildfire early warning system for the fictional island nation of Zakar.

## 🔑  Hackathon key information 
* There are two types of potential submitted projects: early warning system and data visualization.
* You have a week to create one or more of the above projects using a prebuilt sensor system and data, Memphis.dev, and Streamlit.
* The submission deadline is Monday, August 7, 2023.
* The submission can take place at any time during the week.
* The winners will be announced on August 21, 2023.

##  🔥 The challenge
Zakar Island has been struggling with wildfires in the last few years, taking human and animal lives. The fires also destroy homes and agricultural and industrial crops and cause famines.

Zakar's current fire notification system only sends alerts 3 days after a fire has occurred.  That's not enough time to intervene to prevent a fire froms spreading or evacuate people.  To aid the citizens, the government installed temperature sensors and hired you.  Your task is to develop software that uses temperature readings and social media messages to detect wildfires before they spread and generate early-warning alerts.

Read more on the data sensors and the scenario 👉 [here](https://github.com/memphisdev/savezakar/blob/main/scenario.md) 

## Getting Started
To get started with the hackathon, follow these steps:

1. Sign up at the hackathon [main page](https://hackathon.memphis.dev)
1. Create a [Memphis Cloud](https://cloud.memphis.dev/) account.  When you create the account, you'll be asked to create a
   station and user.  Give the station whatever name you would like -- you won't use it.  You will use the user you created, though,
   so make sure to save that.
1. Use this repo as a template to create a new repository.
1. Clone your repository from GitHub.
1. Run the hackathon setup script.  Three stations (`zakar-tweets`, `zakar-temperature-readings`, and `zakar-fire-alerts`) will
   be created and populated with data.
   ```bash
   $ python3 -m venv venv
   $ source venv/bin/activate
   $ pip install -r requirements.txt
   $ python3 setup_hackathon.py --host <host> --username <username> --password <password> --account-id <account-id>
   ```
1. Run the example consumer:
   ```
   $ python example_consumer.py --host <host> --username <username> --password <password> --account-id <account-id>
   ```
1. Get to hacking!

## The Data
You will be access messages in real-time from Memphis.dev stations using one of the Memphis.dev client SDKs.

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

Notifications of past wildfire events are available from the `zakar-fire-alerts` station and look like so:
```json
{
  "event_day": 527,
  "notification_day": 530,
  "geospatial_x": 4,
  "geospatial_y": 5
}
```

## 😎 Some Project Ideas
Please feel free to approach this problem however you want. We'd love to see your creative solutions!
If you need help getting started, we came up with several ideas 💡:

* **Idea #1:** Create a [Streamlit](https://github.com/streamlit/streamlit) dashboard that visualizes the geographic distributions of the temperature readings, tweets, and fire alerts.
* **Idea #2:** Use a Jupyter Notebook to apply statistical outlier detection techniques to the temperature or tweet data.
* **Idea #3**: Train and apply machine learning models for outlier and anomaly detection to the temperature or tweet data.
* **Idea #4:** Ingest the data into Elasticsearch and using its anomaly detection techniques.
* **Idea #5:** Using text embedding models like those from HuggingFace to convert the tweets into vectors and perform clustering or similar to identify outliers.
* **Idea #6:** Create a text classifier for the tweet data to identify fire-related tweets.

## 🏁 Submission
1. Ensure your project is licensed under one of the following: MIT, Apache Software License v2, BSD-2, BSD-3, or Creative Commons.
2. If you are creating an early warning system, have your system generate messages of the following form and send them to a station
  named `zakar-fire-predictions`:
  ```json
  {
    "event_day": 527,
    "geospatial_x": 4,
    "geospatial_y": 5
  }
  ```
3. To submit your project please open an issue in the save-zakar-hackathon repository and follow the instructions. 
4. Create a pull request against the original repository with your project.
5. Finally submit your project via the following [form](https://forms.gle/Hkmk1aLv9FvrZox98).

## 🎁  Prizes 
![Prizes 12](https://github.com/memphisdev/save-zakar-hackathon/assets/107035359/44d04508-cf0b-44dc-a6cc-35cc6cabedc8)

Each project will be judged by the following categories:
* Creativity
* Most informative visualization
* Most accurate solution (For the early warning system)
* Most interesting architecture
* Most interesting algorithm

Besides internal glory, the **best** project will get the perfect gaming package which includes the following:
* SteelSeries Arctis Nova Pro Wireless Multi-System Gaming Headset.
* Logitech G Pro Wireless Gaming Mouse - League of Legends Edition.
* *RARE* Framed Nintendo Game Boy Color GBC Disassembled.
* Tons of swag from Memphis.dev and Streamlit!

The **2nd** best project will receive -  
* Logitech G Pro Wireless Gaming Mouse - League of Legends Edition.
* Tons of swag from Memphis.dev and Streamlit!

The top 10 **Runner ups** will receive an awesome swag pack by Memphis.dev and Streamlit
![Prizes](https://github.com/memphisdev/save-zakar-hackathon/assets/107035359/512d356d-44d5-431b-9618-9ac982cad104)

## FAQ ⁉️
  
### Where do I sign up?
You can sign up on the main hackathon [page](https://www.hackathon.memphis.dev/). 

### When can I submit the project?
Anytime between July 31st to August 7th using this [form](https://forms.gle/Hkmk1aLv9FvrZox98).

### When and where will the winners be announced?
Winners will be announced on August 21st in a virtual event.

### Where should I go if I have any questions?
Join our dedicated [Discord channel](https://discord.gg/EJqN69M6RH).

### What are the judging criteria?
The projects will be judged by the following
* Creativity
* Visualization
* Accuracy (For the early warning system)
* Architecture
* Algorithm

## 🚀 Useful links 
 - [Memphis.dev documentation](https://docs.memphis.dev/memphis/getting-started/readme)
 - [Memphis.dev Cloud Signup](https://cloud.memphis.dev)
 - #SaveZakarHackathon [Discord channel](https://discord.gg/q37A5ZF4yH)
 - [Streamlit documentation](https://docs.streamlit.io/)
 - [Application form](https://www.hackathon.memphis.dev/) 
 - [Submission form](https://forms.gle/Hkmk1aLv9FvrZox98)

<h1>Let's go!!!</h1>
