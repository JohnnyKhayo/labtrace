import streamlit as st
import database
import sqlite3


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
    search = st.text_input("Search by Sample ID or Type", "")

    samples = database.get_all_samples()

    if search:
        search = search.lower()
        samples = [
            s for s in samples
            if search in s["sample_id"].lower() or search in s["sample_type"].lower()
        ]

    
    if samples:
        st.dataframe(samples, use_container_width=True)
    else:
        st.info("No samples found.")

with tab2:
    st.subheader("Add New Sample")
    with st.form("add_form", clear_on_submit=True):
        sample_id = st.text_input(
            "Sample ID",
            placeholder="e.g. SMP-001",
            help="Letters, numbers, and hyphens only"
        )
        sample_type = st.text_input(
            "Sample Type",
            placeholder="e.g. Blood, Urine, Tissue"
        )
        collected_by = st.text_input(
            "Collected By",
            placeholder="Name of person who collected the sample"
        )
        notes = st.text_area(
            "Notes (optional)",
            placeholder="Any additional information"
        )
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
                except sqlite3.IntegrityError:
                    st.error("A sample with this ID already exists.")
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
    samples = database.get_all_samples()
    if not samples:
        st.info("No samples to delete.")
    else:
        sample_ids = [s["sample_id"] for s in samples]
        selected_id = st.selectbox("Select Sample to Delete", sample_ids, key="delete_select")

        confirm = st.checkbox("I confirm I want to delete this sample")
        if st.button("Delete Sample", disabled=not confirm):
            database.delete_sample(selected_id)
            st.success("Sample deleted.")
            st.rerun()

with tab5:
    st.subheader("Summary")
    samples = database.get_all_samples()
    if not samples:
        st.info("No samples yet.")
    else:
        from collections import Counter
        status_counts = Counter(s["status"] for s in samples)
        st.write("**Samples by status:**")
        st.write(dict(status_counts))
        st.metric("Total Samples", len(samples))


        st.divider()
st.caption("LabTrace • Sample tracking tool")