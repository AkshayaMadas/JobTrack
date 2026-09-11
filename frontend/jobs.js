const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "/app/";
}

const jobsContainer = document.getElementById("jobsContainer");
const message = document.getElementById("message");
const backButton = document.getElementById("backButton");
const searchInput = document.getElementById("searchInput");

let allJobs = [];

backButton.addEventListener("click", function () {
    window.location.href = "/app/dashboard.html";
});


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
            message.textContent =
                data.detail || "Could not load jobs.";
            return;
        }

        allJobs = data;
        displayJobs(allJobs);

    } catch (error) {
        message.textContent =
            "Could not connect to the server.";
    }
}


function displayJobs(jobs) {

    jobsContainer.innerHTML = "";

    if (jobs.length === 0) {
        message.textContent = "No matching jobs found.";
        return;
    }

    message.textContent = "";

    jobs.forEach(function (job) {

        const card = document.createElement("div");
        card.className = "dashboard-card";

        card.innerHTML = `
            <h3>${job.position}</h3>

            <p><strong>Company:</strong> ${job.company}</p>

            <p><strong>Location:</strong> ${job.location}</p>

            <p><strong>Status:</strong> ${job.status}</p>

            <p>${job.notes || "No additional notes."}</p>

            <button onclick="applyForJob(${job.id})">
                Apply
            </button>
        `;

        jobsContainer.appendChild(card);
    });
}


searchInput.addEventListener("input", function () {

    const searchText =
        searchInput.value.toLowerCase().trim();

    const filteredJobs = allJobs.filter(function (job) {

        return (
            job.position.toLowerCase().includes(searchText) ||
            job.company.toLowerCase().includes(searchText) ||
            job.location.toLowerCase().includes(searchText)
        );

    });

    displayJobs(filteredJobs);
});


async function applyForJob(jobId) {

    try {

        const response = await fetch("/applications/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                job_id: jobId
            })
        });

        const data = await response.json();

        if (response.ok) {
            alert("Application submitted successfully!");
        } else {
            alert(data.detail || "Could not submit application.");
        }

    } catch (error) {
        alert("Could not connect to the server.");
    }
}


loadJobs();