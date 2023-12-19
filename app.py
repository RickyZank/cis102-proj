######################
# Import libraries
######################

import pandas as pd
import streamlit as st
from PIL import Image

import math
from datetime import datetime

import pandas as pd

import plotly.express as px
import folium
from streamlit_folium import folium_static


######################
# Page Title
######################

# PIL.Image
image = Image.open('airbnblogo.png')

#https://docs.streamlit.io/library/api-reference/media/st.image
st.image(image, width=400)




@st.cache_data
def get_data():
    url = "https://cis102.guihang.org/data/AB_NYC_2019.csv"
    return pd.read_csv(url)
df = get_data()





st.markdown("Welcome to Ricky AirBnB")

boroughs = df['neighbourhood_group'].unique()
#neighborhoods = df['neighbourhood'].unique()
neighborhoods = {borough: df[df['neighbourhood_group'] == borough]['neighbourhood'].unique() for borough in boroughs}

st.title("NYC AirBnB Selection")

st.write("Here are the first few rows of the list of AirBnB: ")

st.dataframe(df.head(10))

# Selecting borough
selected_borough = st.selectbox("Select a borough:", boroughs)
selected_neighborhoods = st.multiselect("Select a neighborhoods:", neighborhoods[selected_borough])

values = st.slider("Price range", float(df.price.min()), 1000., (50., 300.))

# Filter the borough
filtered_data = df[(df['neighbourhood_group'] == selected_borough) &
                   (df['neighbourhood'].isin(selected_neighborhoods)) &
                   (df['price'].between(values[0], values[1]))]

st.write(f"Displaying data for {selected_borough} borough:")

st.write(filtered_data)

#st_ms = st.multiselect("Bruh", selected_neighborhood, default=selected_neighborhood[0])

total_rentals = len(filtered_data)

st.write(f"Total {total_rentals} housing rentals are found in {selected_neighborhoods}, {selected_borough} with prices between &#36;{(values[0])} and &#36;{(values[1])}.")


st.write("---")


toplistings = filtered_data[["name", "neighbourhood", "host_name", "room_type", "latitude", "longitude", "price"]].dropna(how="any").sort_values("price", ascending=False)

if not filtered_data.empty:
    toplistings = filtered_data[["name", "host_name", "neighbourhood", "room_type", "latitude", "longitude", "price"]].dropna(how="any").sort_values("price", ascending=False)

    # If toplistings is not empty
    if not toplistings.empty:
        Top = toplistings.values[0, :]
        m = folium.Map(location=Top[4:6], zoom_start=16)

        tooltip = "Top listings"
        for j in range(min(50, len(toplistings))):
            name, host_name, neighborhood, room_type, lat, lon, price = toplistings.values[j, :]
            popup_text = f"""
            Name: {name}<br>
            Neighborhood: {neighborhood}<br>
            Host name: {host_name}<br>
            Room type: {room_type}<br>
            Price: ${price}
            """
            folium.Marker(
                location=(lat, lon), 
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=f"Price: ${price}"
            ).add_to(m)

        folium_static(m)
    else:
        st.warning("No listings found within the specified criteria.")
else:
    st.warning("No listings found within the specified criteria.")

