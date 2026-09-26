import streamlit as st
import pandas as pd
import time

from google import genai
from google.genai import types

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

PROMPT = """
You are a telecom field audit expert.

Analyze the image and provide:
- Equipment detected
- Battery status
- Cabinet condition
- Safety issues
- Priority
- Recommendations
"""

def analyze_image(image_bytes):

    for _ in range(5):

        try:

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=[
                    PROMPT,
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type="image/jpeg"
                    )
                ]
            )

            return response.text

        except Exception as e:

            if "503" in str(e):
                time.sleep(10)
                continue

            return str(e)

    return "Gemini busy"


st.title("Telecom Audit AI")

uploaded_files = st.file_uploader(
    "Upload Images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:

    results = []

    if st.button("Analyze"):

        for file in uploaded_files:

            result = analyze_image(
                file.getvalue()
            )

            results.append({
                "Image": file.name,
                "Analysis": result
            })

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
