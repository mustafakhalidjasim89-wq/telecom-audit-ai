import streamlit as st
from PIL import Image

st.title("Telecom Audit AI")

uploaded_file = st.file_uploader(
    "Upload Telecom Image",
    type=["jpg","jpeg","png"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Image",
        use_container_width=True
    )

    st.subheader("AI Analysis")

    st.write("""
Equipment:
Generator Controller Panel

Observation:
Operational display is visible.

Detected Values:
- Engine Run Time: 8888h 28m
- Engine Starts: 108

Severity:
Low

Recommendation:
Verify maintenance records and ensure periodic servicing is aligned with engine run hours.
""")
