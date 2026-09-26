import streamlit as st

st.title("Telecom Audit AI")

uploaded_file = st.file_uploader(
    "Upload Telecom Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    st.image(uploaded_file)
    st.success("Image uploaded")
