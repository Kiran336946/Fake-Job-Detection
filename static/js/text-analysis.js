// const analyzeBtn = document.getElementById("analyzeBtn");
// const clearBtn = document.getElementById("clearBtn");
// const jobText = document.getElementById("jobText");

// const resultTitle = document.getElementById("resultTitle");
// const resultMessage = document.getElementById("resultMessage");
// const riskScore = document.getElementById("riskScore");
// const riskProgress = document.getElementById("riskProgress");
// const warningList = document.getElementById("warningList");


// analyzeBtn.addEventListener("click", async function () {

//     const text = jobText.value.trim();

//     if (text === "") {
//         alert("Please paste a job description first.");
//         return;
//     }

//     try {

//         const response = await fetch("http://127.0.0.1:5000/analyze", {
//             method: "POST",

//             headers: {
//                 "Content-Type": "application/json"
//             },

//             body: JSON.stringify({
//                 job_text: text
//             })
//         });

//         const data = await response.json();

//         if (!response.ok) {
//             alert(data.error || "Something went wrong.");
//             return;
//         }

//         console.log("Backend Response:", data);

//         resultTitle.innerText = "Backend Connected";

//         resultMessage.innerText =
//             "Your job description was successfully sent to the Fake Job Detection backend.";

//         riskScore.innerText = "--%";

//         riskProgress.style.width = "0%";

//         warningList.innerHTML = "";

//         const item = document.createElement("div");
//         item.className = "warning-item";
//         item.innerText = "✓ Job text received by backend successfully.";

//         warningList.appendChild(item);

//     } catch (error) {

//         console.error("Backend Error:", error);

//         alert(
//             "Backend connection failed. Make sure Flask server is running."
//         );
//     }

// });


// clearBtn.addEventListener("click", function () {

//     jobText.value = "";

//     resultTitle.innerText = "Waiting for Analysis";

//     resultMessage.innerText =
//         'Enter a job description and click "Analyze Job" to get a result.';

//     riskScore.innerText = "--%";

//     riskProgress.style.width = "0%";

//     warningList.innerHTML = "";

// });


const analyzeBtn = document.getElementById("analyzeBtn");
const clearBtn = document.getElementById("clearBtn");
const jobText = document.getElementById("jobText");

const resultTitle = document.getElementById("resultTitle");
const resultMessage = document.getElementById("resultMessage");
const riskScore = document.getElementById("riskScore");
const riskProgress = document.getElementById("riskProgress");
const warningList = document.getElementById("warningList");


/* =========================================================
   ANALYZE JOB
========================================================= */

analyzeBtn.addEventListener("click", async function () {

    const text = jobText.value.trim();

    if (text === "") {
        alert("Please paste a job description first.");
        return;
    }

    // Disable button while analyzing
    analyzeBtn.disabled = true;
    analyzeBtn.innerText = "⏳ Analyzing...";

    // Show analyzing status
    resultTitle.innerText = "Analyzing...";
    resultMessage.innerText =
        "Our AI model is analyzing the job description.";

    riskScore.innerText = "--%";
    riskProgress.style.width = "0%";
    warningList.innerHTML = "";


    try {

        /* =====================================================
           SEND JOB TEXT TO FLASK
        ===================================================== */

        const response = await fetch("/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                job_text: text
            })
        });


        const data = await response.json();

        console.log("Backend Response:", data);


        /* =====================================================
           HANDLE BACKEND ERROR
        ===================================================== */

        if (!response.ok || !data.success) {

            alert(data.error || "Something went wrong.");

            resultTitle.innerText = "Analysis Failed";
            resultMessage.innerText =
                data.error || "Unable to analyze the job description.";

            return;
        }


        /* =====================================================
           GET MODEL RESULT
        ===================================================== */

        const prediction = data.prediction;
        const probability = data.probability;
        const riskPercentage = data.risk_percentage;


        console.log("Prediction:", prediction);
        console.log("Probability:", probability);
        console.log("Risk:", riskPercentage);


        /* =====================================================
           DISPLAY RISK SCORE
        ===================================================== */

        riskScore.innerText =
            riskPercentage.toFixed(2) + "%";

        riskProgress.style.width =
            riskPercentage + "%";


        /* =====================================================
           FRAUDULENT RESULT
        ===================================================== */

        if (prediction === "FRAUDULENT") {

            resultTitle.innerText =
                "⚠️ Potentially Fraudulent";

            resultMessage.innerText =
                "Our AI model detected patterns commonly associated with fraudulent job postings. Please verify the employer before sharing personal information.";

            warningList.innerHTML = "";

            const warnings = [
                "⚠ High-risk job posting detected.",
                "🔍 Suspicious patterns were detected.",
                "🛡 Verify the employer before applying.",
                "⚠ Do not share sensitive personal or financial information."
            ];

            warnings.forEach(function (warning) {

                const item = document.createElement("div");

                item.className = "warning-item";

                item.innerText = warning;

                warningList.appendChild(item);

            });

        }


        /* =====================================================
           LEGITIMATE RESULT
        ===================================================== */

        else {

            resultTitle.innerText =
                "✅ Likely Legitimate";

            resultMessage.innerText =
                "Our AI model did not detect strong patterns commonly associated with fraudulent job postings.";

            warningList.innerHTML = "";

            const messages = [
                "✓ No major fraud indicators detected.",
                "🔍 Job description appears relatively safe.",
                "🛡 Always verify the employer before applying."
            ];

            messages.forEach(function (message) {

                const item = document.createElement("div");

                item.className = "warning-item";

                item.innerText = message;

                warningList.appendChild(item);

            });

        }


    } catch (error) {

        console.error("Backend Error:", error);

        resultTitle.innerText =
            "Connection Error";

        resultMessage.innerText =
            "Unable to connect to the Fake Job Detection server.";

        riskScore.innerText = "--%";

        riskProgress.style.width = "0%";

        warningList.innerHTML = "";

        alert(
            "Backend connection failed. Make sure Flask server is running."
        );

    }


    /* =====================================================
       ENABLE BUTTON AGAIN
    ===================================================== */

    analyzeBtn.disabled = false;
    analyzeBtn.innerText = "🔍 Analyze Job";

});


/* =========================================================
   CLEAR BUTTON
========================================================= */

clearBtn.addEventListener("click", function () {

    jobText.value = "";

    resultTitle.innerText =
        "Waiting for Analysis";

    resultMessage.innerText =
        'Enter a job description and click "Analyze Job" to get a result.';

    riskScore.innerText =
        "--%";

    riskProgress.style.width =
        "0%";

    warningList.innerHTML = "";

});