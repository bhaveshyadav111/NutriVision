# NutriVision — Flask + Keras + Gemini

An attractive food-analysis web app built around your trained 80-class food image classifier.

## Flow

1. Browser uploads a food photo.
2. Flask loads the photo and runs your TensorFlow/Keras model.
3. The top predicted food class + confidence are calculated.
4. The same image and prediction context are sent to Gemini.
5. Gemini returns estimated ingredients, calories, macros and micronutrients.
6. The frontend renders the result as a nutrition dashboard.

## 1. Add your trained model

Copy your model to:

`models/food_model.keras`

or point to it with `MODEL_PATH` in `.env`.

## 2. Replace the class names

Replace the 80 placeholders in `class_names.json` with the EXACT class order used when training the model.

For example:

```json
[
  "pizza",
  "burger",
  "sushi"
]
```

The order is critical: index 0 must correspond to the model's class 0, index 1 to class 1, etc.

## 3. Configure preprocessing

Your inference preprocessing MUST match training.

Common options are in `.env`:

`PREPROCESS=scale` → `image / 255.0`

`PREPROCESS=xception` → Xception `preprocess_input`

`PREPROCESS=mobilenet` → MobileNetV2 `preprocess_input`

`PREPROCESS=resnet` → ResNet50 `preprocess_input`

`PREPROCESS=none` → raw pixel values

Also set `IMG_SIZE` to the image size expected by your model.

## 4. Add Gemini key

Create `.env` from `.env.example` and add your key:

`GEMINI_API_KEY=...`

Do not put the key in `static/app.js` or any HTML file. It must stay server-side.

## 5. Install and run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Then open `http://127.0.0.1:5000`.

## Important nutrition caveat

The nutrition section is an AI estimate from a photograph. It cannot reliably know exact portion weight, recipe, oil quantity, or hidden ingredients. Treat it as an estimate, not a clinical or laboratory measurement.

## Gemini API note

The app uses the official Google Gen AI Python SDK (`google-genai`) and keeps the Gemini call in `gemini_service.py`. The Gemini model name is configurable through `GEMINI_MODEL`, so it can be changed without modifying the frontend.
