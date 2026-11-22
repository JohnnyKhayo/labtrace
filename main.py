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
    samples = database.get_all_samples()
    if samples:
        st.dataframe(samples, use_container_width=True)
    else:
        st.info("No samples yet.")

with tab2:
    st.subheader("Add New Sample")
    with st.form("add_form", clear_on_submit=True):
        sample_id = st.text_input("Sample ID")
        sample_type = st.text_input("Sample Type")
        collected_by = st.text_input("Collected By")
        notes = st.text_area("Notes (optional)")
        submitted = st.form_submit_button("Add Sample")

        if submitted:
            from sample import Sample
            sample = Sample(sample_id, sample_type, collected_by, notes=notes)
            error = sample.is_valid()
            if error:
                st.error(error)
            else:
                try:
                    database.add_sample(sample)
                    st.success("Sample added successfully.")
                except Exception as e:
                    st.error(f"Could not add sample: {e}")
              
with tab3:
    st.subheader("Update Sample")
with tab4:
    st.subheader("Delete Sample")
with tab5:
    st.subheader("Summary")