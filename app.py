# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.after_request
# def add_cors_headers(response):
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     response.headers["Access-Control-Allow-Headers"] = "Content-Type"
#     response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
#     return response
# @app.route("/")
# def home():
#     return "Fake Job Detection Backend Working!"


# @app.route("/analyze", methods=["POST"])
# def analyze():
#     data = request.get_json()

#     job_text = data.get("job_text", "")

#     if not job_text:
#         return jsonify({
#             "error": "Job text is required"
#         }), 400

#     return jsonify({
#         "message": "Job text received successfully",
#         "job_text": job_text
#     })


# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, jsonify, render_template, send_from_directory

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    job_text = data.get("job_text", "")

    if not job_text:
        return jsonify({"error": "Job text is required"}), 400

    return jsonify({
        "message": "Job text received successfully",
        "job_text": job_text
    })

# =========================
# OTHER PAGES
# =========================
@app.route("/about")
def about():
    return render_template("pages/about.html")


@app.route("/how_it_work")
def how_it_work():
    return render_template("pages/how_it_work.html")


@app.route("/text_analysis")
def text_analysis():
    return render_template("pages/text_analysis.html")


@app.route("/login")
def login():
    return render_template("pages/login.html")

@app.route("/features")
def features():
    return render_template("pages/features.html")


@app.route("/signup")
def signup():
    return render_template("pages/signup.html")


@app.route("/footer")
def footer():
    return send_from_directory("templates", "footer.html")



if __name__ == "__main__":
    app.run(debug=True)