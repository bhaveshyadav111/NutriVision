import streamlit as st
import keras
from PIL import Image
from categories import category
from keras.applications.inception_resnet_v2 import preprocess_input
import numpy as np
import os
import json
from huggingface_hub import hf_hub_download
from dotenv import load_dotenv
from google import genai


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="NutriVision",
    page_icon="🍽️",
    layout="centered"
)


# -----------------------------
# Load Environment Variables
# -----------------------------

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY environment variable is not set.")
    st.stop()


# -----------------------------
# Load Model
# -----------------------------

@st.cache_resource
def load_model():

    model_path = hf_hub_download(
        repo_id="Bhavesh540/NutriVision",
        filename="FoodDetection.keras"
    )

    return keras.models.load_model(model_path)


model = load_model()

categories = category()

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# -----------------------------
# Gemini Nutrition Function
# -----------------------------

def get_nutrition(food_name):

    prompt = f"""
You are a nutrition information assistant.

The food classification model identified the dish as:

{food_name}

Give an estimated nutrition profile for ONE typical serving of this dish.

Return ONLY valid JSON.
Do not use markdown.
Do not add explanations.

Use exactly this structure:
{{
    "serving": "description of serving",
    "calories": 0,
    "protein": 0,
    "carbs": 0,
    "fat": 0,
    "fiber": 0
}}

Rules:

- calories must be in kcal
- protein must be in grams
- carbs must be in grams
- fat must be in grams
- fiber must be in grams
- use reasonable estimates
- numbers must be numeric values, not strings
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        text = response.text.strip()

        # Remove markdown code fences if Gemini returns them
        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        nutrition = json.loads(text)

        return nutrition

    except Exception as e:

        print("Gemini error:", e)

        return {
            "serving": "Not available",
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0,
            "fiber": 0
        }


# -----------------------------
# Prediction Function
# -----------------------------

def predict_food(image):

    image = image.convert("RGB")

    image = image.resize((256, 256))

    image = keras.utils.img_to_array(image)

    image = preprocess_input(image)

    image = np.expand_dims(image, axis=0)

    prediction = model.predict(image, verbose=0)

    max_prob_index = np.argmax(prediction[0])

    predicted_food = categories[max_prob_index]

    confidence = float(prediction[0][max_prob_index])

    return predicted_food, confidence


# -----------------------------
# UI
# -----------------------------

st.title("🍽️ NutriVision")

st.subheader("AI Food Recognition & Nutrition Analyzer")

st.write(
    "Upload an image of food and NutriVision will identify the dish "
    "and estimate its nutritional information."
)


uploaded_file = st.file_uploader(
    "Upload a food image",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Image",
        width="stretch"
    )

    if st.button("🔍 Analyze Food", type="primary"):

        with st.spinner("Analyzing food..."):

            # Food prediction
            predicted_food, confidence = predict_food(image)

            # Nutrition prediction
            nutrition = get_nutrition(predicted_food)

        st.success("Analysis complete!")

        # -------------------------
        # Prediction Result
        # -------------------------

        st.subheader("🍴 Food Detected")

        st.write(f"### {predicted_food}")

        st.progress(
            min(confidence, 1.0),
            text=f"Confidence: {confidence * 100:.2f}%"
        )

        # -------------------------
        # Nutrition
        # -------------------------

        st.subheader("🥗 Estimated Nutrition")

        st.write(
            f"**Serving:** {nutrition.get('serving', 'Not available')}"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Calories",
                f"{nutrition.get('calories', 0)} kcal"
            )

            st.metric(
                "Protein",
                f"{nutrition.get('protein', 0)} g"
            )

            st.metric(
                "Carbs",
                f"{nutrition.get('carbs', 0)} g"
            )

        with col2:
            st.metric(
                "Fat",
                f"{nutrition.get('fat', 0)} g"
            )

            st.metric(
                "Fiber",
                f"{nutrition.get('fiber', 0)} g"
            )