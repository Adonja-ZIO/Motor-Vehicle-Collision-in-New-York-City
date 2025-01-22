# Import necessary libraries
import streamlit as st  # For building the web app
import pandas as pd  # For data manipulation
import numpy as np  # For numerical operations
import pydeck as pdk  # For geographical visualization
import plotly.express as px  # For creating interactive plots

# Path to the dataset
DATA_URL = ("Motor_Vehicle_Collisions_-_Crashes.csv")

# Set the title and description of the Streamlit app
st.title("Motor Vehicle Collision in New York City")
st.markdown("This application is a Streamlit dashboard that can be used "
            "to analyze motor vehicle collisions in NYC 🗽💥🚗")

# Function to load data
@st.cache_data  # Cache the data to improve performance
def load_data(nrows):
    # Load the dataset, parsing date and time into a single column
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[["CRASH_DATE", "CRASH_TIME"]])
    # Remove rows with missing latitude and longitude
    data.dropna(subset=["LATITUDE", "LONGITUDE"], inplace=True)
    # Convert column names to lowercase
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    # Rename the combined date/time column
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data

# Load a subset of data (first 100,000 rows)
data = load_data(100000)
original_data = data  # Keep a copy of the original data for later use

# Display the header and map for locations with the most injuries
st.header("Where are the most people injured in NYC?")
# Slider to filter data by the number of injured persons
injured_people = st.slider("Number of Persons injured in vehicle collisions", 0, 19)
# Show a map of locations where the number of injured persons meets the threshold
st.map(data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))

# Display the header for collisions based on time
st.header("How many collisions occur at a given time of day?")
# Slider to filter data by the hour of the day
hour = st.slider("Hour to look at", 0, 23)
# Filter the data to include only collisions within the selected hour
data = data[data['date/time'].dt.hour == hour]

# Display the time range being analyzed
st.markdown("Vehicle collisions between %i:00 and %i:00" % (hour, (hour+1) % 24))
# Calculate the midpoint for map centering
midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))
# Show a 3D map with collision density
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",  # Map style
    initial_view_state={  # Initial view settings
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(  # Create a HexagonLayer for density visualization
            "HexagonLayer",
            data=data[["date/time", 'latitude', 'longitude']],
            get_position=['longitude', 'latitude'],
            radius=100,  # Radius of hexagons
            extruded=True,  # Enable 3D visualization
            pickable=True,  # Allow interactivity
            elevation_scale=4,  # Elevation scale
            elevation_range=[0, 1000],  # Elevation range
        ),
    ]
))

# Display a breakdown of collisions by minute within the selected hour
st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour+1) % 24))
# Filter data for the selected hour range
filtered = data[
    (data['date/time'].dt.hour >= hour) & (data["date/time"].dt.hour < (hour+1))
]
# Create a histogram of crashes by minute
hist = np.histogram(filtered["date/time"].dt.minute, bins=60, range=(0, 60))[0]
# Prepare data for the bar chart
chart_data = pd.DataFrame({'minute': range(60), 'crashes': hist})
# Create a bar chart using Plotly Express
fig = px.bar(chart_data, x='minute', y='crashes', hover_data=["minute", 'crashes'], height=400)
# Display the bar chart
st.write(fig)

# Display the header for top dangerous streets
st.header("Top 5 dangerous streets by affected type")
# Dropdown to select the affected type of people
select = st.selectbox('Affected type of people', ['Pedestrians', 'Cyclists', 'Motorists'])
# Show the top 5 streets based on the selected type
if select == 'Pedestrians':
    st.write(original_data.query("injured_pedestrians >= 1")[["on_street_name", "injured_pedestrians"]]
             .sort_values(by=["injured_pedestrians"], ascending=False)
             .dropna(how='any')[:5])
elif select == 'Cyclists':
    st.write(original_data.query("injured_cyclists >= 1")[["on_street_name", "injured_cyclists"]]
             .sort_values(by=["injured_cyclists"], ascending=False)
             .dropna(how='any')[:5])
else:
    st.write(original_data.query("injured_motorists >= 1")[["on_street_name", "injured_motorists"]]
             .sort_values(by=["injured_motorists"], ascending=False)
             .dropna(how='any')[:5])

# Checkbox to display raw data
if st.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data)
