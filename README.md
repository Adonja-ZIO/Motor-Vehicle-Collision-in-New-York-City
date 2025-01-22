# NYC Motor Vehicle Collisions Dashboard

## Overview

This project is a Streamlit application designed to analyze motor vehicle collisions in New York City. It provides interactive visualizations and insights into collision patterns, helping users explore data based on injuries, time of day, and affected individuals.

---

## Features

### Data Filtering:
- Filter collisions by the number of injured persons.
- Explore collision data based on specific hours of the day.

### Interactive Maps:
- View a map of collision locations where injuries occurred.
- Explore a 3D HexagonLayer map visualizing collision density.

### Collision Breakdown:
- Analyze the frequency of collisions by minute within a selected hour.
- Interactive bar chart for minute-level breakdown.

### Dangerous Streets:
- Identify the top 5 most dangerous streets for pedestrians, cyclists, or motorists.

### Raw Data Access:
- Option to view the raw dataset used in the analysis.

---

## Installation

### Prerequisites
- Python 3.9 or later
- Streamlit library

### Required Python Libraries:
- pandas
- numpy
- pydeck
- plotly

### Setup

1. Clone the repository or download the source files.
2. Place the dataset `Motor_Vehicle_Collisions_-_Crashes.csv` in the same directory as the script.
3. Install the required libraries using pip:
   ```bash
   pip install streamlit pandas numpy pydeck plotly
