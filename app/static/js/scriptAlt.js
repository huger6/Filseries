document.addEventListener("DOMContentLoaded", function () {
    changePasswordVisibility();
}); 


function changePasswordVisibility() {
    document.querySelector(".passwordInfo").addEventListener("click", function() {
        let passwordField = document.getElementById("password");
        let icon = this.querySelector("i");

        if (passwordField.type === "password") {
            passwordField.type = "text"; //Shows password
            icon.classList.remove("fa-eye-slash");
            icon.classList.add("fa-eye");
        }
        else {
            passwordField.type = "password"; //Hides password
            icon.classList.remove("fa-eye");
            icon.classList.add("fa-eye-slash");
        }
    });
}

