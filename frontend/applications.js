const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "/app/";
}

const applicationsContainer =
    document.getElementById("applicationsContainer");

const message = document.getElementById("message");

const backButton = document.getElementById("backButton");

backButton.addEventListener("click", function () {
    window.location.href = "/app/dashboard.html";
});


async function loadApplications() {

    try {

        const response = await fetch("/applications/", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            message.textContent =
                data.detail || "Could not load applications.";
            return;
        }

        message.textContent = "";

        if (data.length === 0) {
            message.textContent = "You haven't applied for any jobs yet.";
            return;
        }

        data.forEach(function (application) {

            const card = document.createElement("div");

            card.className = "dashboard-card";

            card.innerHTML = `
                <h3>Application #${application.id}</h3>

                <p>
                    <strong>Job ID:</strong>
                    ${application.job_id}
                </p>

                <p>
                    <strong>Status:</strong>
                    ${application.status}
                </p>

                <p>
                    <strong>Resume:</strong>
                    ${application.resume || "Not provided"}
                </p>
            `;

            applicationsContainer.appendChild(card);
        });

    } catch (error) {

        message.textContent =
            "Could not connect to the server.";
    }
}

loadApplications();