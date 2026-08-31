/* =========================================
   FAKE JOB DETECTION
   MAIN JAVASCRIPT
========================================= */


document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log(
            "Fake Job Detection website loaded successfully."
        );

    }
);


/* =========================================
   ACTIVE NAVIGATION
========================================= */

const currentPage =
    window.location.pathname
    .split("/")
    .pop();


const navLinks =
    document.querySelectorAll(
        ".nav-links a"
    );


navLinks.forEach(
    function (link) {

        const linkPage =
            link.getAttribute("href");


        if (
            linkPage === currentPage ||
            (
                currentPage === "" &&
                linkPage === "index.html"
            )
        ) {

            link.classList.add("active");

        }

    }
);


/* =========================================
   BUTTON CLICK
========================================= */

const buttons =
    document.querySelectorAll(
        ".primary-btn, .secondary-btn, .login-btn"
    );


buttons.forEach(
    function (button) {

        button.addEventListener(
            "click",
            function () {

                console.log(
                    "Opening: " +
                    button.innerText
                );

            }
        );

    }
);
const footerPath = location.pathname.includes("/pages/")
  ? "../footer.html"
  : "footer.html";

fetch(footerPath)
  .then(response => response.text())
  .then(data => {
    document.getElementById("footer").innerHTML = data;
  });


  fetch("/footer")
    .then(response => response.text())
    .then(data => {
        document.getElementById("footer").innerHTML = data;
    })
    .catch(error => {
        console.error("Footer loading error:", error);
    });