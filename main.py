import streamlit as st
import database
import sqlite3

st.set_page_config(page_title="LabTrace", layout="wide")

database.create_table()

st.title("LabTrace")
st.write("Track lab samples and their status.")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["List", "Add", "Update", "Delete", "Summary"]
)

with tab1:
    st.subheader("All Samples")
    search = st.text_input("Search by Sample ID or Type", "")

    samples = database.get_all_samples()

    if search and search.strip():
        term = search.strip().lower()
        samples = [
            s for s in samples
            if term in str(s.get("sample_id") or "").lower()
            or term in str(s.get("sample_type") or "").lower()
        ]
    
    if samples:
        st.dataframe(samples, use_container_width=True)
    else:
        st.info("No samples found.")

with tab2:
    st.subheader("Add New Sample")
    if "form_key" not in st.session_state:
        st.session_state.form_key = 0
    
    with st.form(key=f"add_form_{st.session_state.form_key}"):

        sample_id = st.text_input(
            "Sample ID",
            placeholder="e.g. SMP-001",
            help="Letters, numbers, and hyphens only")

        sample_type = st.text_input(
            "Sample Type",
            placeholder="e.g. Blood, Urine, Tissue")

        collected_by = st.text_input(
            "Collected By",
            placeholder="Name of person who collected the sample")

        notes = st.text_area(
            "Notes (optional)",
            placeholder="Any additional information")

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

                    st.session_state.form_key += 1
                    st.success("Sample added successfully.")
                    st.rerun()

                except sqlite3.IntegrityError:
                    st.error("A sample with this ID already exists.")
                except Exception:
                    st.error(f"A database error occurred. Please try again")

              
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
            try:
                updated = database.update_sample_status(selected_id, new_status)

                if updated:
                    st.success(f"Status updated to {new_status}")
                    st.rerun()
                else:
                    st.warning(f"Sample not found. No changes were made.")
            except sqlite3.Error:
                st.error("Could not update sample status due to a database error.")
                
with tab4:
    st.subheader("Delete Sample")
    samples = database.get_all_samples()
    if not samples:
        st.info("No samples to delete.")
    else:
        sample_ids = [s["sample_id"] for s in samples]
        selected_id = st.selectbox("Select Sample to Delete", sample_ids, key="delete_select")

        if st.session_state.get("reset_delete_confirm", False):
            st.session_state.delete_confirm = False
            st.session_state.reset_delete_confirm = False

        confirm = st.checkbox("I confirm I want to delete this sample", key="delete_confirm")

        if st.button("Delete Sample", disabled=not confirm):
            try:
                database.delete_sample(selected_id)
                st.session_state.reset_delete_confirm = True
                st.success("Sample deleted.")
                st.rerun()

            except sqlite3.Error:
                st.error("Could not delete sample due to a database error.")

with tab5:
    st.subheader("Summary")

    samples = database.get_all_samples()

    if not samples:
        st.info("No samples yet.")
    else:
        from collections import Counter
        status_counts = Counter(s["status"] for s in samples)
        st.metric("Total Samples", len(samples))
        st.write("**Samples by status:**")

        for status, count in sorted(status_counts.items()):
            st.write(f"**{status}:** {count}")

        st.divider()
        st.caption("LabTrace • Sample tracking tool")