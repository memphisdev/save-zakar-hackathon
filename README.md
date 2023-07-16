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
* There are two types of potential submitted projects: early warning system and data visualization
* You have a week to create one or more of the above projects using a prebuilt sensor system and data, Memphis.dev, and Streamlit
* The submission deadline is Monday, August 7, 2023
* The submission can take place at any time during the week
* The winners will be announced on August 21, 2023

## 🎁  Prizes 
Each project will be judged by the following categories:
* Creativity
* Most informative visualization
* Most accurate solution (For the early warning system)
* Most interesting architecture
* Most interesting algorithm

Besides internal glory, the **best** project will get the perfect gaming package which includes the following:
* SteelSeries Arctis Nova Pro Wireless Multi-System Gaming Headset
* Logitech G Pro Wireless Gaming Mouse - League of Legends Edition
* *RARE* Framed Nintendo Game Boy Color GBC Disassembled
* Tons of swag from Memphis.dev and Streamlit!

The **2nd** best project will receive -  
* Logitech G Pro Wireless Gaming Mouse - League of Legends Edition
* Tons of swag from Memphis.dev and Streamlit!

The top 10 **Runner ups** will receive an awesome swag pack by Memphis.dev and Streamlit
![Prizes](https://github.com/memphisdev/save-zakar-hackathon/assets/107035359/512d356d-44d5-431b-9618-9ac982cad104)

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
1. [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this repository on GitHub.
1. Clone your forked repository from GitHub.
1. Run the hackathon setup script.  Three stations (`zakar-tweets`, `zakar-temperature-readings`, and `zakar-fire-alerts`) will
   be created and populated with data.
   ```bash
   $ python3 -m venv venv
   $ source venv/bin/activate
   $ pip install -r requirements.txt
   $ python3 setup_hackathon.py --host <host> --username <username> --password <password> --account-id <account-id>
   ```
1. Check out our example notebook:
1. Run the example consumer:
   ```
   $ python example_consumer.py --host <host> --username <username> --password <password> --account-id <account-id>
   ```
1. Get to hacking!

## 😎 Some examples 
Please feel free to approach this problem however you want. We'd love to see your creative solutions!
If you need help getting started, we came up with several ideas 💡:

* **Idea #1:** Create a [Streamlit](https://github.com/streamlit/streamlit) dashboard that visualizes the geographic distributions of the temperature readings, tweets, and fire alerts.
* **Idea #2:** Use a Jupyter Notebook to apply statistical outlier detection techniques to the temperature or tweet data.
* **Idea #3**: Train and apply machine learning models for outlier and anomaly detection to the temperature or tweet data.
* **Idea #4:** Ingest the data into Elasticsearch and using its anomaly detection techniques.
* **Idea #5:** Using text embedding models like those from HuggingFace to convert the tweets into vectors and perform clustering or similar to identify outliers.
* **Idea #6:** Create a text classifier for the tweet data to identify fire-related tweets.

## 🏁 Submission
* License your project under one of the following: MIT, Apache Software License v2, BSD-2, BSD-3, or Creative Commons.
* Create a README.md file with instructiosn for running your project.
* Submit your project via the following [form](https://forms.gle/Hkmk1aLv9FvrZox98)

## FAQ ⁉️
  
### Where do I sign up?
You can sign up on the main hackathon [page](https://www.hackathon.memphis.dev/). 

### When can I submit the project?
Anytime between July 31st to August 7th using this [form](https://docs.google.com/forms/d/e/1FAIpQLSecz9jV_bhVaC4zodhbD7QFqQYo_V9B8w9skJlLHOhI6WrWlw/viewform).

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
 - #SaveZakarHackathon Discord channel
 - [Streamlit documentation](https://docs.streamlit.io/)
 - Tutorial Videos

<h1>Let's go!!!</h1>
