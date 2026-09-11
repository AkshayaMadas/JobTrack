const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "/app/";
}

const logoutButton = document.getElementById("logoutButton");

logoutButton.addEventListener("click", () => {
    localStorage.removeItem("access_token");
    window.location.href = "/app/";
});

const postJobButton = document.getElementById("postJobButton");

postJobButton.addEventListener("click", () => {
    window.location.href = "/app/post-job.html";
});

const manageJobsButton = document.getElementById("manageJobsButton");

manageJobsButton.addEventListener("click", () => {
    window.location.href = "/app/manage-jobs.html";
});

const applicantsButton = document.getElementById("applicantsButton");

applicantsButton.addEventListener("click", () => {
    window.location.href = "/app/applicants.html";
});