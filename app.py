from flask import Flask, render_template, request
import keras
from PIL import Image
from categories import category
from keras.applications.inception_resnet_v2 import preprocess_input
import numpy as np
import os
import json
from huggingface_hub import login, upload_folder,hf_hub_download

# login()

# # Push your model files
# upload_folder(folder_path="/home/hemant/code/NutriVision/models", repo_id="Bhavesh540/NutriVision", repo_type="model")

# Download Model
model_path = hf_hub_download(
    repo_id='Bhavesh540/NutriVision',
    filename='FoodDetection.keras'
)

from dotenv import load_dotenv
load_dotenv()

from google import genai


app = Flask(__name__)

categories = category()

model = keras.models.load_model(
    model_path
)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY environment variable is not set."
    )

client = genai.Client(
    api_key=GEMINI_API_KEY
)

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

        # Remove possible markdown formatting
        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        nutrition = json.loads(text)

        return nutrition

    except Exception as e:

        print("Gemini error:", e)

        # Fallback values if Gemini fails
        return {
            "serving": "Not available",
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0,
            "fiber": 0
        }

@app.route("/")
@app.route("/home")
def home():

    return render_template(
        "index.html",
        food=None,
        confidence=None,
        nutrition=None
    )

@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return "No image uploaded", 400
    
    image_file = request.files["image"]

    if image_file.filename == "":
        return "No image selected", 400
    
    # convert from Image to PIL 

    image = Image.open(image_file).convert("RGB")

    image = image.resize((256, 256))

    image = keras.utils.img_to_array(image)

    pre_image = preprocess_input(image)

    pre_image = np.expand_dims(pre_image,axis=0) # one batch
    prediction = model.predict(pre_image)

    max_prob_index = np.argmax(prediction[0])

    predicted_food = categories[max_prob_index]
    confidence = float(prediction[0][max_prob_index])

    confidence_percentage = confidence * 100


    print("--------------------------------")
    print("Predicted food:", predicted_food)
    print("Confidence:", confidence_percentage)
    print("--------------------------------")

    nutrition = get_nutrition(
        predicted_food
    )

    return render_template(
        "index.html",
        food=predicted_food,
        confidence=confidence_percentage,
        nutrition=nutrition
    )

if __name__ == "__main__":

    app.run(
        debug=True
    )