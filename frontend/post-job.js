const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "/app/";
}

const postJobForm = document.getElementById("postJobForm");
const message = document.getElementById("message");
const logoutButton = document.getElementById("logoutButton");

const urlParams = new URLSearchParams(window.location.search);
const jobId = urlParams.get("id");

logoutButton.addEventListener("click", function () {
    localStorage.removeItem("access_token");
    window.location.href = "/app/";
});

async function loadJob() {
    if (!jobId) {
        return;
    }

    try {
        const response = await fetch(`/jobs/${jobId}`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const job = await response.json();

        if (!response.ok) {
            message.textContent = job.detail || "Could not load job.";
            return;
        }

        document.getElementById("company").value = job.company;
        document.getElementById("position").value = job.position;
        document.getElementById("location").value = job.location;
        document.getElementById("status").value = job.status;
        document.getElementById("notes").value = job.notes || "";

        document.querySelector("h2").textContent = "Edit Job";

    } catch (error) {
        message.textContent = "Could not connect to the server.";
    }
}

postJobForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const company = document.getElementById("company").value;
    const position = document.getElementById("position").value;
    const location = document.getElementById("location").value;
    const status = document.getElementById("status").value;
    const notes = document.getElementById("notes").value;

    const jobData = {
        company: company,
        position: position,
        location: location,
        status: status,
        notes: notes
    };

    try {
        const url = jobId ? `/jobs/${jobId}` : "/jobs/";
        const method = jobId ? "PUT" : "POST";

        const response = await fetch(url, {
            method: method,
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(jobData)
        });

        const data = await response.json();

        if (response.ok) {
            message.textContent = jobId
                ? "Job updated successfully!"
                : "Job posted successfully!";

            if (!jobId) {
                postJobForm.reset();
            }
        } else {
            message.textContent =
                data.detail || "Could not save the job.";
        }

    } catch (error) {
        message.textContent = "Could not connect to the server.";
    }
});

loadJob();