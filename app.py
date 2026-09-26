import streamlit as st
import pandas as pd
import json
import base64

from PIL import Image
from openai import OpenAI

st.set_page_config(
    page_title="Telecom Audit AI",
    layout="wide"
)

st.title("Telecom Audit AI")

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


def analyze_image(image_bytes):

    base64_image = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    prompt = """
You are a Senior Telecom Field Auditor.

Analyze this image.

Identify:

- Equipment Type
- Vendor
- Visible Readings
- Observation
- Severity
- Recommendation

Return ONLY JSON:

{
    "equipment":"",
    "vendor":"",
    "visible_readings":"",
    "observation":"",
    "severity":"",
    "recommendation":""
}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url":
                            f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        temperature=0.1
    )

    return response.choices[0].message.content


uploaded_file = st.file_uploader(
    "Upload Telecom Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(
        image,
        use_container_width=True
    )

    if st.button("Analyze Image"):

        with st.spinner("Analyzing..."):

            result = analyze_image(
                uploaded_file.getvalue()
            )

        st.subheader("AI Result")

        st.code(result)

        try:

            data = json.loads(result)

            df = pd.DataFrame([data])

            st.dataframe(df)

            excel_file = "Telecom_Report.xlsx"

            df.to_excel(
                excel_file,
                index=False
            )

            with open(
                excel_file,
                "rb"
            ) as f:

                st.download_button(
                    label="Download Excel",
                    data=f,
                    file_name=excel_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        except Exception:

            st.error(
                "JSON parse failed"
            )
