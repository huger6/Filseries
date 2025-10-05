
document.addEventListener("DOMContentLoaded", function () {
    checkLoginOnHome();
    leftButtonsDrop();
    navBarDropdowns();
});  

async function checkLogin() {
    try {
        const res = await fetch("/is_user_logged_in", { credentials: "same-origin" });
        const data = await res.json();
        return { loggedIn: data.loggedIn, username: data.username || null };
    } catch {
        return { loggedIn: false, username: null };
    }
}

function leftButtonsDrop() {
    const dropdowns = document.querySelectorAll(".dropdown-watch");
    
    dropdowns.forEach((dropdown) => {
        const button = dropdown.querySelector(".dropdown-button");
        
        button.addEventListener("click", function (event) {
            event.stopPropagation(); //Evita que se feche automaticamente
            //Altera o estado atual
            dropdown.classList.toggle("open");
        });
    });
    //Fechar dropdowns ao clicar fora
    document.addEventListener("click", function (event) {
        dropdowns.forEach((dropdown) => {
            if (dropdown.contains(event.target)) {
                dropdown.classList.remove("open");
                sessionStorage.setItem("leftButtonsDrop", false);
            }
        })
    });
}

function navBarDropdowns() {
    const notificationButton = document.getElementById("notifications");
    const userButton = document.getElementById("user");
    
    const notificationSymbol = notificationButton.querySelector(".notifications-symbol");
    const userSymbol = userButton.querySelector(".user-symbol");
    
    const notificationDropdown = notificationButton.querySelector(".notifications-dropdown");
    const userDropdown = userButton.querySelector(".user-dropdown");
    
    document.addEventListener("click", function (event) {
        let clickedInside = false;
        
        //Open notifications
        if (notificationButton.contains(event.target)) {
            clickedInside = true;
            notificationDropdown.classList.toggle("open");
            notificationSymbol.classList.toggle("open");
            userDropdown.classList.remove("open");
            userSymbol.classList.remove("open");
        }
        //Open user
        if (userButton.contains(event.target)) {
            clickedInside = true;
            if (sessionStorage.getItem("USER_IS_LOGGED") === "true") {
                userDropdown.classList.toggle("open");
                userSymbol.classList.toggle("open");
                notificationDropdown.classList.remove("open");
                notificationSymbol.classList.remove("open");
            }
            else {
                window.location.replace(loginUrl);
            }
        }
        
        //Fechar todos os dropdowns antes de abrir outro
        if (!clickedInside) {
            notificationDropdown.classList.remove("open");
            notificationSymbol.classList.remove("open");
            userDropdown.classList.remove("open");
            userSymbol.classList.remove("open");
        }
    });
}


function checkLoginOnHome() {
    async function runCheck() {
        const user = await checkLogin();
        
        if (user.loggedIn === true) {
            sessionStorage.setItem("USER_IS_LOGGED", "true");
            sessionStorage.setItem("user-id", user.username);
        }
        else {
            sessionStorage.setItem("USER_IS_LOGGED", "false");
            sessionStorage.setItem("user-id", null);
        }
    }
    
    if (window.location.pathname === homeUrl) {
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", runCheck);
        }
        else {
            runCheck();
        }
    }
}

