const analyzeBtn = document.getElementById("analyzeBtn");
const clearBtn = document.getElementById("clearBtn");
const jobText = document.getElementById("jobText");

const resultTitle = document.getElementById("resultTitle");
const resultMessage = document.getElementById("resultMessage");
const riskScore = document.getElementById("riskScore");
const riskProgress = document.getElementById("riskProgress");
const warningList = document.getElementById("warningList");


analyzeBtn.addEventListener("click", async function () {

    const text = jobText.value.trim();

    if (text === "") {
        alert("Please paste a job description first.");
        return;
    }

    try {

        const response = await fetch("http://127.0.0.1:5000/analyze", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                job_text: text
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error || "Something went wrong.");
            return;
        }

        console.log("Backend Response:", data);

        resultTitle.innerText = "Backend Connected";

        resultMessage.innerText =
            "Your job description was successfully sent to the Fake Job Detection backend.";

        riskScore.innerText = "--%";

        riskProgress.style.width = "0%";

        warningList.innerHTML = "";

        const item = document.createElement("div");
        item.className = "warning-item";
        item.innerText = "✓ Job text received by backend successfully.";

        warningList.appendChild(item);

    } catch (error) {

        console.error("Backend Error:", error);

        alert(
            "Backend connection failed. Make sure Flask server is running."
        );
    }

});


clearBtn.addEventListener("click", function () {

    jobText.value = "";

    resultTitle.innerText = "Waiting for Analysis";

    resultMessage.innerText =
        'Enter a job description and click "Analyze Job" to get a result.';

    riskScore.innerText = "--%";

    riskProgress.style.width = "0%";

    warningList.innerHTML = "";

});