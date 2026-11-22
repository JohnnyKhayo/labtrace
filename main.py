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
    st.subheader("Update Sample Status")
    samples = database.get_all_samples()
    if not samples:
        st.info("No samples to update.")
    else:
        sample_ids = [s["sample_id"] for s in samples]
        selected_id = st.selectbox("Select Sample", sample_ids)
        from sample import Sample
        new_status = st.selectbox("New Status", Sample.STATUSES)

        if st.button("Update Status"):
            database.update_sample_status(selected_id, new_status)
            st.success(f"Status updated to {new_status}")
            st.rerun()
            
with tab4:
    st.subheader("Delete Sample")
with tab5:
    st.subheader("Summary")