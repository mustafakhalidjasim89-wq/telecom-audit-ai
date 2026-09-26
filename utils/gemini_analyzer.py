import streamlit as st
import time

from google import genai
from google.genai import types

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

PROMPT = """
You are a telecom field audit expert.

Analyze image and return exactly:

Equipment:
Battery Status:
Cabinet Condition:
Safety Issues:
Priority:
Recommendations:
"""

def analyze_image(image_bytes, image_name):

    for attempt in range(5):

        try:

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    PROMPT,
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type="image/jpeg"
                    )
                ]
            )

            return {
                "Image": image_name,
                "Analysis": response.text
            }

        except Exception as e:

            if "503" in str(e):
                time.sleep(10)
                continue

            return {
                "Image": image_name,
                "Analysis": str(e)
            }

    return {
        "Image": image_name,
        "Analysis": "Gemini Busy"
    }
