/* =========================================
   LOGIN PAGE
========================================= */

const loginForm =
    document.getElementById("loginForm");

const loginMessage =
    document.getElementById("loginMessage");


if (loginForm) {

    loginForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();


            const email =
                document.getElementById("email").value.trim();

            const password =
                document.getElementById("password").value.trim();


            /* Check fields */

            if (email === "" || password === "") {

                loginMessage.innerText =
                    "Please enter your email and password.";

                return;

            }


            /* Demo Login */

            loginMessage.innerText =
                "Login successful! Welcome to Fake Job Detection.";

        }
    );

}


/* =========================================
   FORGOT PASSWORD
========================================= */

const forgotPassword =
    document.getElementById("forgotPassword");


if (forgotPassword) {

    forgotPassword.addEventListener(
        "click",
        function (event) {

            event.preventDefault();

            alert(
                "Password recovery will be available soon."
            );

        }
    );

}