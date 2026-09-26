import streamlit as st
import pandas as pd
import fitz
import io
import time

from PIL import Image
from google import genai
from google.genai import types

# ====================================================
# CONFIG
# ====================================================

st.set_page_config(
    page_title="Telecom Audit AI",
    layout="wide"
)

# ====================================================
# GEMINI
# ====================================================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

MODEL_NAME = "gemini-3.8-flash"

PROMPT = """
You are a Senior Telecom Field Audit Engineer.

Analyze this telecom site image and provide:

1. Equipment Detected
2. Cabinet Type
3. Cabinet Condition
4. Battery Type
5. Battery Condition
6. Rectifier Status
7. Power Issues
8. Safety Issues
9. Housekeeping Issues
10. Severity (Low / Medium / High)
11. Recommended Corrective Action

Provide a professional telecom engineer assessment.
"""

# ====================================================
# IMAGE OPTIMIZATION
# ====================================================

def optimize_image(image_bytes):

    img = Image.open(io.BytesIO(image_bytes))

    if img.mode != "RGB":
        img = img.convert("RGB")

    img.thumbnail((1600, 1600))

    buffer = io.BytesIO()

    img.save(
        buffer,
        format="JPEG",
        quality=85
    )

    return buffer.getvalue()

# ====================================================
# PDF TO IMAGES
# ====================================================

def pdf_to_images(pdf_bytes):

    images = []

    pdf = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    for page_num in range(len(pdf)):

        page = pdf[page_num]

        pix = page.get_pixmap(
            matrix=fitz.Matrix(1.5, 1.5),
            alpha=False
        )

        img = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        buffer = io.BytesIO()

        img.save(
            buffer,
            format="JPEG",
            quality=85
        )

        images.append({
            "page": page_num + 1,
            "bytes": buffer.getvalue()
        })

    return images

# ====================================================
# GEMINI ANALYSIS
# ====================================================

def analyze_image(image_bytes):

    image_bytes = optimize_image(image_bytes)

    for attempt in range(5):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[
                    PROMPT,
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type="image/jpeg"
                    )
 
