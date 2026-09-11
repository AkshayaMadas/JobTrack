const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "/app/";
}

const applicationsContainer =
    document.getElementById("applicationsContainer");

const message = document.getElementById("message");
const backButton = document.getElementById("backButton");

backButton.addEventListener("click", function () {
    window.location.href = "/app/recruiter-dashboard.html";
});


async function loadJobs() {
    try {
        const response = await fetch("/jobs/", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const jobs = await response.json();

        if (!response.ok) {
            message.textContent =
                jobs.detail || "Could not load jobs.";
            return;
        }

        applicationsContainer.innerHTML = "";

        if (jobs.length === 0) {
            message.textContent = "No jobs available.";
            return;
        }

        jobs.forEach(function (job) {
            const card = document.createElement("div");

            card.className = "dashboard-card";

            card.innerHTML = `
                <h3>${job.position}</h3>
                <p>
                    <strong>Company:</strong>
                    ${job.company}
                </p>
                <p>
                    <strong>Location:</strong>
                    ${job.location}
                </p>

                <button onclick="viewApplicants(${job.id})">
                    View Applicants
                </button>
            `;

            applicationsContainer.appendChild(card);
        });

        message.textContent = "";

    } catch (error) {
        message.textContent =
            "Could not connect to the server.";
    }
}


async function viewApplicants(jobId) {
    try {
        const response = await fetch(
            `/applications/job/${jobId}`,
            {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const applications = await response.json();

        if (!response.ok) {
            message.textContent =
                applications.detail ||
                "Could not load applicants.";
            return;
        }

        applicationsContainer.innerHTML = "";

        if (applications.length === 0) {
            message.textContent =
                "No applicants for this job yet.";
            return;
        }

        message.textContent =
            `Applicants for Job #${jobId}`;

        applications.forEach(function (application) {
            const card = document.createElement("div");

            card.className = "dashboard-card";

            card.innerHTML = `
                <h3>Application #${application.id}</h3>

                <p>
                    <strong>Candidate ID:</strong>
                    ${application.user_id}
                </p>

                <p>
                    <strong>Job ID:</strong>
                    ${application.job_id}
                </p>

                <p>
                    <strong>Current Status:</strong>
                    ${application.status}
                </p>

                <p>
                    <strong>Resume:</strong>
                    ${application.resume || "Not provided"}
                </p>

                <label for="status-${application.id}">
                    Update Status
                </label>

                <select id="status-${application.id}">
                    <option value="Applied">Applied</option>
                    <option value="Shortlisted">Shortlisted</option>
                    <option value="Interview">Interview</option>
                    <option value="Selected">Selected</option>
                    <option value="Rejected">Rejected</option>
                </select>

                <button onclick="updateStatus(${application.id})">
                    Update Status
                </button>
            `;

            applicationsContainer.appendChild(card);
        });

        applications.forEach(function (application) {
            document.getElementById(
                `status-${application.id}`
            ).value = application.status;
        });

    } catch (error) {
        message.textContent =
            "Could not connect to the server.";
    }
}


async function updateStatus(applicationId) {
    const statusSelect =
        document.getElementById(`status-${applicationId}`);

    const newStatus = statusSelect.value;

    try {
        const response = await fetch(
            `/applications/${applicationId}/status?new_status=${encodeURIComponent(newStatus)}`,
            {
                method: "PUT",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const data = await response.json();

        if (response.ok) {
            alert("Application status updated successfully!");
        } else {
            alert(
                data.detail ||
                "Could not update application status."
            );
        }

    } catch (error) {
        alert("Could not connect to the server.");
    }
}


loadJobs();