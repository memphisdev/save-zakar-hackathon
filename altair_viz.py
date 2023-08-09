import json
import altair as alt
import streamlit as st
import pandas as pd
from supabase import create_client, Client

st.title("Zakar Island Fire Viz")
# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)

supabase = init_connection()

# Read the event days from the transformed_fire_alerts.json file
with open('transformed_fire_alerts.json', 'r') as file:
    fire_alerts_data = json.load(file)
event_days = sorted(list(set([event["event_day"] for event in fire_alerts_data])))

# Create a slider with event days
selected_day = st.select_slider('Select Event Day', options=event_days)

# Show loading state
with st.spinner('Loading data...'):
    # Fetch temperature data from Supabase
    response = supabase.table('zakar-data').select("*").eq('day', selected_day).execute()
    selected_day_data = response.data

# Create a DataFrame from the data
df = pd.DataFrame(selected_day_data)

# Variables to track fire IDs and fire temperatures
fire_temperatures = []

# Convert geospatial_x and geospatial_y to integers
df['geospatial_x'] = df['geospatial_x'].astype(int)
df['geospatial_y'] = df['geospatial_y'].astype(int)

# Identify coordinates that have fire events and assign IDs
fire_id = 1
for fire_event in fire_alerts_data:
    if fire_event["event_day"] == selected_day:
        for alert in fire_event["fire_alerts"]:
            temperature = df.loc[(df['geospatial_x'] == alert["geospatial_x"]) & (df['geospatial_y'] == alert["geospatial_y"]), 'temperature'].values[0]
            fire_temperatures.append((fire_id, temperature))
            df.loc[(df['geospatial_x'] == alert["geospatial_x"]) & (df['geospatial_y'] == alert["geospatial_y"]), 'is_fire'] = fire_id
            fire_id += 1

df['is_fire'].fillna(False, inplace=True)

# Calculate the average global temperature for the selected day
average_global_temp = df['temperature'].mean()

# Create an Altair chart for normal temperature points
points = alt.Chart(df[df['is_fire'] == False]).mark_circle().encode(
    x='geospatial_x:Q',
    y='geospatial_y:Q',
    color='temperature:Q',
    tooltip=['geospatial_x', 'geospatial_y', 'temperature']
).properties(
    title='Geospatial Coordinates with Temperature',
    width=600,
    height=400
).interactive()

# Mark fire events with fire emoji and tooltips
fire_points = alt.Chart(df[df['is_fire'] != False]).mark_text(text="🔥", size=20).encode(
    x='geospatial_x:Q',
    y='geospatial_y:Q',
    tooltip=['is_fire:Q', 'geospatial_x', 'geospatial_y']
)

# Combine the charts
final_chart = points + fire_points

# Display the chart using Streamlit
st.altair_chart(final_chart)


# Create three columns
col1, col2, col3 = st.columns(3)

# Display metrics in each column
col1.metric(label='Selected Day', value=selected_day)
col2.metric(label='Number of Fires', value=len(fire_temperatures))
col3.metric(label='Average Global Temperature (°C)', value=round(average_global_temp, 2))

# Create a table to display fire event temperatures
fire_temp_table = pd.DataFrame(fire_temperatures, columns=['Fire ID', 'Temperature (°F)'])
fire_temp_table['Temperature (°F)'] = fire_temp_table['Temperature (°F)'].apply(lambda x: round(x, 2))
st.table(fire_temp_table)

# Create a DataFrame to hold the number of fire events per day
fire_frequency_df = pd.DataFrame([(event["event_day"], len(event["fire_alerts"])) for event in fire_alerts_data], columns=['Event Day', 'Number of Fires'])

# Create a line chart to visualize fire frequency over time
fire_frequency_chart = alt.Chart(fire_frequency_df).mark_line(point=True).encode(
    x='Event Day:O',
    y='Number of Fires:Q'
).properties(
    title='Fire Frequency Over Time',
    width=600,
    height=400
)

# Display the chart using Streamlit
st.altair_chart(fire_frequency_chart)
