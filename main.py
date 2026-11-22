import streamlit as st
import database


# ensures the table exists
database.create_table()

st.set_page_config(page_title="LabTrace", layout="wide")
st.title("LabTrace")
st.write("Track lab samples and their status.")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["List", "Add", "Update", "Delete", "Summary"]
)

with tab1:
    st.subheader("All Samples")
with tab2:
    st.subheader("Add New Sample")
with tab3:
    st.subheader("Update Sample")
with tab4:
    st.subheader("Delete Sample")
with tab5:
    st.subheader("Summary")