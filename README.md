# 🍽️ NutriVision — AI Food Analyzer

> **Identify your food. Understand your nutrition.**

NutriVision is an AI-powered food recognition app that identifies dishes from images and provides nutritional information and macronutrients.

## ✨ Features

* 🧠 **80 Food Categories**
* 🔥 **InceptionResNetV2** with Transfer Learning & Fine-Tuning
* 📸 Food image classification
* 📊 Prediction confidence
* 🥗 Nutrition & macronutrients using **Gemini API**
* 🌐 Flask web application

## 🛠️ Tech Stack

`Python` `TensorFlow` `Keras` `Flask` `NumPy` `Pillow` `Hugging Face` `Gemini API`

## 🔄 How It Works

```text
📸 Food Image
      ↓
🧠 InceptionResNetV2
      ↓
🍛 Dish Prediction
      ↓
🤖 Gemini API
      ↓
🥗 Nutrition & Macros
```

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/NutriVision.git
cd NutriVision
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add API keys

Create a `.env` file:

```env
HF_TOKEN=your_huggingface_token
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Start the app

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

## 🔐 Environment Variables

Create `.env.example`:

```env
HF_TOKEN=
GEMINI_API_KEY=
```

⚠️ **Never commit your `.env` file or API keys to GitHub.**

The trained model is hosted on **Hugging Face** and downloaded by the application.

## 👨‍💻 Author

**Bhavesh Yadav**

[GitHub](https://github.com/bhaveshyadav111)
