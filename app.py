from flask import Flask, request, jsonify, render_template, send_from_directory 
from transformers import AutoTokenizer, AutoModelForSequenceClassification 
import torch 
# ========================================================= 
# # FLASK APP 
# # ========================================================= 

app = Flask(__name__) 
# ========================================================= 
# # HUGGING FACE MODEL 
# # ========================================================= 
MODEL_NAME = "rehan-ml/scamshield-scam-detector" 
print("\n========================================") 
print("Loading ScamShield model...") 
print("========================================") 

# Load tokenizer 
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME) 

# Load model 
model = AutoModelForSequenceClassification.from_pretrained( MODEL_NAME ) 

# Set model to evaluation mode 
model.eval() 

print("ScamShield model loaded successfully!") 
print("Model labels:", model.config.id2label) 
print("========================================\n") 

# ========================================================= 
# # MODEL PREDICTION 
# # ========================================================= 
def predict_job(job_text): 
    # ----------------------------------------------------- 
    # # Convert job text into tokens 
    # # ----------------------------------------------------- 
    inputs = tokenizer( job_text, return_tensors="pt", truncation=True, max_length=512 ) 

    # ----------------------------------------------------- 
    # # Run the model 
    # # ----------------------------------------------------- 
    with torch.no_grad(): outputs = model(**inputs) 

    # ----------------------------------------------------- 
    # Convert model output into probabilities 
    # # ----------------------------------------------------- 
    probabilities = torch.softmax( outputs.logits, dim=1 ) 

    # ----------------------------------------------------- 
    # Based on the model: 
    # # Index 0 = Safe # Index 1 = Scam 
    # # ----------------------------------------------------- 
    safe_probability = probabilities[0][0].item() 
    scam_probability = probabilities[0][1].item() 

    # ----------------------------------------------------- 
    # # Classification 
    # # ----------------------------------------------------- 
    if scam_probability >= 0.50: 
        result = "FRAUDULENT" 
    else: 
        result = "LEGITIMATE" 

    # Convert scam probability to percentage 
    risk_percentage = round( scam_probability * 100, 2 ) 

    return ( result, scam_probability, safe_probability, risk_percentage ) 

# ========================================================= 
# # HOME PAGE 
# # ========================================================= 
@app.route("/") 
def home(): 
    return render_template("index.html") 

# ========================================================= 
# # ANALYZE JOB 
# # ========================================================= 
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        # -------------------------------------------------
        # Get JSON data sent by JavaScript
        # -------------------------------------------------
        data = request.get_json()

        # -------------------------------------------------
        # Check if data exists
        # -------------------------------------------------
        if not data:
            return jsonify({"success": False, "error": "No data received."}), 400

        # -------------------------------------------------
        # Get job text
        # -------------------------------------------------
        job_text = data.get("job_text", "").strip()

        # -------------------------------------------------
        # Check if text is empty
        # -------------------------------------------------
        if not job_text:
            return jsonify({"success": False, "error": "Job text is required."}), 400

        print("\n========================================")
        print("Analyzing Job Description")
        print("========================================")
        print("Text length:", len(job_text))
        print("Running ScamShield model...")

        # -------------------------------------------------
        # Run model prediction
        # -------------------------------------------------
        (result, scam_probability, safe_probability, risk_percentage) = predict_job(job_text)

        # -------------------------------------------------
        # Print result in PowerShell
        # -------------------------------------------------
        print("Prediction:", result)
        print("Safe probability:", round(safe_probability * 100, 2), "%")
        print("Scam probability:", round(scam_probability * 100, 2), "%")
        print("========================================\n")

        # -------------------------------------------------
        # Send result to frontend
        # -------------------------------------------------
        return jsonify({
            "success": True,
            "prediction": result,                              # Scam probability as decimal
            "probability": round(scam_probability, 6),         # Risk percentage for website
            "risk_percentage": risk_percentage,                # Safe probability
            "safe_probability": round(safe_probability, 6),    # Scam probability
            "scam_probability": round(scam_probability, 6)
        })

    except Exception as e:
        print("\nERROR:")
        print(str(e))
        return jsonify({"success": False, "error": str(e)}), 500
# ========================================================= 
# # ABOUT PAGE 
# # ========================================================= 
@app.route("/about") 
def about(): 
    return render_template( "pages/about.html" ) 

# ========================================================= 
# # HOW IT WORKS PAGE 
# # ========================================================= 
@app.route("/how_it_work") 
def how_it_work(): 
    return render_template( "pages/how_it_work.html" ) 

# ========================================================= 
# # TEXT ANALYSIS PAGE 
# # ========================================================= 
@app.route("/text_analysis") 
def text_analysis(): 
    return render_template( "pages/text_analysis.html" ) 

# ========================================================= 
# # LOGIN PAGE 
# # ========================================================= 
@app.route("/login") 
def login(): 
    return render_template( "pages/login.html" ) 

# ========================================================= 
# # FEATURES PAGE 
# # ========================================================= 
@app.route("/features") 
def features(): 
    return render_template( "pages/features.html" ) 

# ========================================================= 
# # SIGNUP PAGE 
# # ========================================================= 
@app.route("/signup") 
def signup(): 
    return render_template( "pages/signup.html" ) 

# ========================================================= 
# # FOOTER 
# # ========================================================= 
@app.route("/footer") 
def footer(): 
    return send_from_directory( "templates", "footer.html" ) 

# ========================================================= 
# # RUN FLASK 
# # ========================================================= 
if __name__ == "__main__": 
    app.run( debug=True )