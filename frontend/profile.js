const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "/app/";
}

const usernameElement = document.getElementById("username");
const roleElement = document.getElementById("role");
const backButton = document.getElementById("backButton");

backButton.addEventListener("click", function () {
    window.location.href = "/app/dashboard.html";
});

async function loadProfile() {
    try {
        const response = await fetch("/users/me", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            usernameElement.textContent =
                data.detail || "Could not load profile.";
            roleElement.textContent = "";
            return;
        }

        usernameElement.textContent = data.username;
        roleElement.textContent = data.role;

    } catch (error) {
        usernameElement.textContent =
            "Could not connect to the server.";
        roleElement.textContent = "";
    }
}

loadProfile();