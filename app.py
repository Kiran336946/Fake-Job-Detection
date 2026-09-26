from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for, session

from database import get_db_connection, create_tables
from werkzeug.security import generate_password_hash, check_password_hash
from transformers import AutoTokenizer, AutoModelForSequenceClassification 
import torch 
# ========================================================= 
# # FLASK APP 
# # ========================================================= 

app = Flask(__name__) 

app.secret_key = "fake-job-detection-secret-key"

# Create database tables
create_tables()

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

    # -----------------------------------------
    # User must be logged in
    # -----------------------------------------

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "error": "Please login first."
        }), 401

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

                # -----------------------------------------
        # Save analysis in database
        # -----------------------------------------

        connection = get_db_connection()

        connection.execute(
            """
            INSERT INTO analyses
            (
                user_id,
                job_text,
                prediction,
                risk_percentage
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                session["user_id"],
                job_text,
                result,
                risk_percentage
            )
        )

        connection.commit()
        connection.close()

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

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("pages/text_analysis.html")

# ========================================================= 
# # LOGIN PAGE 
# # ========================================================= 
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("pages/login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        return "Please enter email and password."

    connection = get_db_connection()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    connection.close()

    if user is None:
        return "Invalid email or password."

    if not check_password_hash(
        user["password"],
        password
    ):
        return "Invalid email or password."

    # -----------------------------------------
    # Remember the logged-in user
    # -----------------------------------------

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    session["user_email"] = user["email"]

    # -----------------------------------------
    # Go to dashboard
    # -----------------------------------------

    return redirect(
        url_for("dashboard")
    )

# ========================================================= 
# # FEATURES PAGE 
# # ========================================================= 
@app.route("/features") 
def features(): 
    return render_template( "pages/features.html" ) 

# ========================================================= 
# # DASHBOARD PAGE 
# # ========================================================= 
@app.route("/dashboard")
def dashboard():

    # -----------------------------------------
    # Check login
    # -----------------------------------------

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    # -----------------------------------------
    # Get user's analyses
    # -----------------------------------------

    connection = get_db_connection()

    analyses = connection.execute(
        """
        SELECT *
        FROM analyses
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (session["user_id"],)
    ).fetchall()

    connection.close()

    # -----------------------------------------
    # Calculate statistics
    # -----------------------------------------

    total_analyses = len(analyses)

    fraudulent_count = sum(
        1
        for analysis in analyses
        if analysis["prediction"] == "FRAUDULENT"
    )

    legitimate_count = sum(
        1
        for analysis in analyses
        if analysis["prediction"] == "LEGITIMATE"
    )

    # -----------------------------------------
    # Calculate average risk
    # -----------------------------------------

    if total_analyses > 0:

        average_risk = sum(
            analysis["risk_percentage"]
            for analysis in analyses
        ) / total_analyses

    else:

        average_risk = 0

    # -----------------------------------------
    # Open dashboard
    # -----------------------------------------

    return render_template(
        "pages/dashboard.html",

        user_name=session["user_name"],

        user_email=session["user_email"],

        analyses=analyses,

        total_analyses=total_analyses,

        fraudulent_count=fraudulent_count,

        legitimate_count=legitimate_count,

        average_risk=average_risk
    )

# ========================================================= 
# # SIGNUP PAGE 
# # ========================================================= 
@app.route("/signup", methods=["GET", "POST"])
def signup():

    # =====================================================
    # SHOW SIGNUP PAGE
    # =====================================================

    if request.method == "GET":
        return render_template("pages/signup.html")


    # =====================================================
    # GET FORM DATA
    # =====================================================

    name = request.form.get("name", "").strip()

    email = request.form.get("email", "").strip()

    password = request.form.get("password", "")

    confirm_password = request.form.get(
        "confirm_password",
        ""
    )


    # =====================================================
    # CHECK EMPTY FIELDS
    # =====================================================

    if not name or not email or not password or not confirm_password:

        return "Please fill in all fields."


    # =====================================================
    # CHECK PASSWORDS
    # =====================================================

    if password != confirm_password:

        return "Passwords do not match."


    # =====================================================
    # HASH PASSWORD
    # =====================================================

    hashed_password = generate_password_hash(
        password
    )


    # =====================================================
    # CONNECT TO DATABASE
    # =====================================================

    connection = get_db_connection()


    try:

        # =================================================
        # SAVE USER
        # =================================================

        connection.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                hashed_password
            )
        )

        connection.commit()


    except Exception as e:

        connection.close()

        # Email already exists
        if "UNIQUE constraint failed" in str(e):

            return "This email is already registered."

        return "Database error: " + str(e)


    connection.close()


    # =====================================================
    # REDIRECT TO LOGIN PAGE
    # =====================================================

    return redirect(
        url_for("login")
    )


# ========================================================= 
# # CHANGE PASSWORD PAGE 
# # ========================================================= 
@app.route("/change_password", methods=["GET", "POST"])
def change_password():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("pages/change_password.html")

    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not current_password or not new_password or not confirm_password:
        return "Please fill in all fields."

    if new_password != confirm_password:
        return "New passwords do not match."

    connection = get_db_connection()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (session["user_id"],)
    ).fetchone()

    if user is None:
        connection.close()
        return redirect(url_for("login"))

    if not check_password_hash(
        user["password"],
        current_password
    ):
        connection.close()
        return "Current password is incorrect."

    hashed_password = generate_password_hash(
        new_password
    )

    connection.execute(
        """
        UPDATE users
        SET password = ?
        WHERE id = ?
        """,
        (
            hashed_password,
            session["user_id"]
        )
    )

    connection.commit()
    connection.close()

    return redirect(url_for("dashboard"))

# ========================================================= 
# # LOGOUT PAGE 
# # ========================================================= 
@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )

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