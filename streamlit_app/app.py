import pandas as pd
import streamlit as st
from helpers import FastAPIClient, Styling

client = FastAPIClient()

# Streamlit UI
st.title("Supply Management Dashboard")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Home", "Databeses", "Search Database by value", "Search Database by strings"],
)

# Display content based on navigation choice
if page == "Home":
    Styling.render_home_page()
elif page == "Databeses":
    Styling.render_databases_page(client)
elif page == "Search Database by value":
    Styling.render_value_search_page(client)
elif page == "Search Database by strings":
    Styling.render_string_search_page(client)

footer = """
    <div style="background-color: lightgrey; padding: 10px; 
                position: fixed; left: 0; bottom: 0; width: 100%; 
                text-align: center;">
        <p>Contact us at <a href="mailto:gt2253@cumc.columbia.edu">Gergo</a></p>
    </div>
    """
st.markdown(footer, unsafe_allow_html=True)
