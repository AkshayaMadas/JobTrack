const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "/app/";
}

const jobsContainer = document.getElementById("jobsContainer");
const message = document.getElementById("message");

async function loadJobs() {
    try {
        const response = await fetch("/jobs/", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            message.textContent = data.detail || "Could not load jobs.";
            return;
        }

        jobsContainer.innerHTML = "";
        message.textContent = "";

        data.forEach(function (job) {
            const card = document.createElement("div");

            card.className = "dashboard-card";

            card.innerHTML = `
                <h3>${job.position}</h3>
                <p><strong>Company:</strong> ${job.company}</p>
                <p><strong>Location:</strong> ${job.location}</p>
                <p><strong>Status:</strong> ${job.status}</p>
                <p>${job.notes || "No notes available."}</p>

                <button onclick="editJob(${job.id})">
                    Edit
                </button>

                <button onclick="deleteJob(${job.id})">
                    Delete
                </button>
            `;

            jobsContainer.appendChild(card);
        });

    } catch (error) {
        message.textContent = "Could not connect to the server.";
    }
}

function editJob(jobId) {
    window.location.href = `/app/post-job.html?id=${jobId}`;
}

async function deleteJob(jobId) {
    const confirmed = confirm("Are you sure you want to delete this job?");

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(`/jobs/${jobId}`, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            alert("Job deleted successfully!");
            loadJobs();
        } else {
            alert(data.detail || "Could not delete job.");
        }

    } catch (error) {
        alert("Could not connect to the server.");
    }
}

loadJobs();