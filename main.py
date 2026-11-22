import streamlit as st
import database


# ensures the table exists
database.create_table()

st.set_page_config(page_title="LabTrace", layout="wide")
st.title("LabTrace")
st.write("Track lab samples and their status.")