import streamlit as st
from google import genai
from PIL import Image
import io
import pandas as pd

# -------------------------------------------------
# Gemini Client
# -------------------------------------------------

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# -------------------------------------------------
# Image Analysis Function
# -------------------------------------------------

def analyze_image(image_bytes):

    image = Image.open(io.BytesIO(image_bytes))

    prompt = """
    You are a senior telecom field audit engineer.

    Analyze the image and provide:

    1. Equipment Detected
    2. Cabinet Status
    3. Battery Status
    4. Power System Observations
    5. Safety Issues
    6. Housekeeping Issues
    7. Severity (Low/Medium/High)
    8. Recommended Corrective Actions

    Return the result in a professional telecom audit format.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, image]
    )

    return response.text


# -------------------------------------------------
# Streamlit UI
# -------------------------------------------------

st.set_page_config(
    page_title="Telecom Audit AI",
    layout="wide"
)

st.title("📡 Telecom Audit AI")

site_id = st.text_input("Site ID")

uploaded_file = st.file_uploader(
    "Upload Site Photo",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    st.image(uploaded_file, width=600)

    if st.button("Analyze"):

        with st.spinner("Analyzing image..."):

            result = analyze_image(
                uploaded_file.getvalue()
            )

        st.success("Analysis Complete")

        st.markdown(result)

        report_df = pd.DataFrame({
            "Site ID": [site_id],
            "Remarks": [result]
        })

        excel_file = "telecom_audit_report.xlsx"

        report_df.to_excel(
            excel_file,
            index=False
        )

        with open(excel_file, "rb") as f:
            st.download_button(
                "📥 Download Excel Report",
                f,
                file_name=excel_file
            )
