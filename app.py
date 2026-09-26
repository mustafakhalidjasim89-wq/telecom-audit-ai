import streamlit as st
import pandas as pd
from utils.gemini_analyzer import analyze_image

st.set_page_config(
    page_title="Telecom Audit AI",
    layout="wide"
)

st.title("📡 Telecom Audit AI")

site_id = st.text_input("Site ID")

uploaded_files = st.file_uploader(
    "Upload Site Images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:

    results = []

    if st.button("Analyze All Images"):

        progress = st.progress(0)

        for idx, file in enumerate(uploaded_files):

            result = analyze_image(
                file.getvalue(),
                file.name
            )

            results.append(result)

            progress.progress(
                (idx + 1) / len(uploaded_files)
            )

        df = pd.DataFrame(results)

        st.dataframe(df)

        excel_file = "telecom_audit_report.xlsx"

        df.to_excel(
            excel_file,
            index=False
        )

        with open(excel_file, "rb") as f:
            st.download_button(
                "Download Excel",
                f,
                file_name=excel_file
            )
