from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import pickle
import re
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)


# ============================================================
# MODEL PATHS
# ============================================================

MODEL_PATH = os.path.join("model", "fake_job_lstm_model.h5")
TOKENIZER_PATH = os.path.join("model", "tokenizer.pkl")
THRESHOLD_PATH = os.path.join("model", "threshold.pkl")

MAX_SEQUENCE_LENGTH = 200

# Default threshold
FRAUD_THRESHOLD = 0.80


# ============================================================
# TEXT CLEANING
# MUST MATCH TRAINING CODE
# ============================================================

def clean_text(text):
    text = str(text)

    # Remove URLs
    text = re.sub(r'http\S+|www\S+', ' ', text)

    # Keep only English letters and spaces
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    # Convert to lowercase
    text = text.lower()

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# ============================================================
# LOAD MODEL
# ============================================================

print("\n========================================")
print("Loading Fake Job Detection Model")
print("========================================")


# Check files exist
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model file not found: {os.path.abspath(MODEL_PATH)}"
    )

if not os.path.exists(TOKENIZER_PATH):
    raise FileNotFoundError(
        f"Tokenizer file not found: {os.path.abspath(TOKENIZER_PATH)}"
    )


# Print absolute paths
print("\nMODEL PATH:")
print(os.path.abspath(MODEL_PATH))

print("\nTOKENIZER PATH:")
print(os.path.abspath(TOKENIZER_PATH))

print("\nTHRESHOLD PATH:")
print(os.path.abspath(THRESHOLD_PATH))


# ------------------------------------------------------------
# Load tokenizer
# ------------------------------------------------------------

print("\nLoading tokenizer...")

with open(TOKENIZER_PATH, "rb") as f:
    tokenizer = pickle.load(f)

print("Tokenizer loaded successfully!")


# ------------------------------------------------------------
# Load Keras model
# ------------------------------------------------------------

print("\nLoading H5 model...")

model = load_model(MODEL_PATH)

print("H5 model loaded successfully!")


# ------------------------------------------------------------
# Load threshold
# ------------------------------------------------------------

FRAUD_THRESHOLD = 0.80

print("\nUsing fraud threshold:", FRAUD_THRESHOLD)


print("\n========================================")
print("Model initialization complete!")
print("========================================\n")


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# ANALYZE JOB
# ============================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        # ----------------------------------------------------
        # Get JSON data
        # ----------------------------------------------------

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "error": "No data received"
            }), 400


        # ----------------------------------------------------
        # Get job text
        # ----------------------------------------------------

        job_text = data.get("job_text", "").strip()

        if not job_text:

            return jsonify({
                "success": False,
                "error": "Job text is required"
            }), 400


        # ----------------------------------------------------
        # Display input
        # ----------------------------------------------------

        print("\n========================================")
        print("Analyzing Job Description")
        print("========================================")

        print("\nOriginal text:")
        print(job_text)


        # ----------------------------------------------------
        # Clean text
        # SAME AS TRAINING
        # ----------------------------------------------------

        cleaned_text = clean_text(job_text)

        print("\nCleaned text:")
        print(cleaned_text)


        # ----------------------------------------------------
        # Tokenization
        # ----------------------------------------------------

        sequence = tokenizer.texts_to_sequences(
            [cleaned_text]
        )

        print("\nTokenized sequence:")
        print(sequence)


        # ----------------------------------------------------
        # Padding
        # ----------------------------------------------------

        padded_sequence = pad_sequences(
            sequence,
            maxlen=MAX_SEQUENCE_LENGTH,
            padding="post",
            truncating="post"
        )

        print("\nInput shape:")
        print(padded_sequence.shape)


        # ----------------------------------------------------
        # Model prediction
        # ----------------------------------------------------

        prediction = model.predict(
            padded_sequence,
            verbose=0
        )

        print("\nRaw prediction:")
        print(prediction)


        probability = float(
            prediction[0][0]
        )

        print(
            "\nProbability:",
            probability
        )


        # ----------------------------------------------------
        # Classification
        # ----------------------------------------------------

        if probability >= FRAUD_THRESHOLD:

            result = "FRAUDULENT"

        else:

            result = "LEGITIMATE"


        # ----------------------------------------------------
        # Risk percentage
        # ----------------------------------------------------

        risk_percentage = round(
            probability * 100,
            2
        )


        print(
            "Threshold:",
            FRAUD_THRESHOLD
        )

        print(
            "Result:",
            result
        )

        print(
            "Risk Percentage:",
            risk_percentage
        )

        print("========================================\n")


        # ----------------------------------------------------
        # Send response to frontend
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "prediction": result,

            "probability": round(
                probability,
                6
            ),

            "risk_percentage": risk_percentage,

            "threshold": FRAUD_THRESHOLD

        })


    except Exception as e:

        print("\nERROR:")
        print(str(e))

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ============================================================
# OTHER EXISTING ROUTES
# ============================================================

@app.route("/about")
def about():

    return render_template(
        "pages/about.html"
    )


@app.route("/how_it_work")
def how_it_work():

    return render_template(
        "pages/how_it_work.html"
    )


@app.route("/text_analysis")
def text_analysis():

    return render_template(
        "pages/text_analysis.html"
    )


@app.route("/login")
def login():

    return render_template(
        "pages/login.html"
    )


@app.route("/features")
def features():

    return render_template(
        "pages/features.html"
    )


@app.route("/signup")
def signup():

    return render_template(
        "pages/signup.html"
    )


@app.route("/footer")
def footer():

    return send_from_directory(
        "templates",
        "footer.html"
    )


# ============================================================
# RUN FLASK
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )

