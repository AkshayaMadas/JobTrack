const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "/app/";
}

const logoutButton = document.getElementById("logoutButton");

logoutButton.addEventListener("click", function () {
    localStorage.removeItem("access_token");
    window.location.href = "/app/";
});

const viewJobsButton = document.getElementById("viewJobsButton");

viewJobsButton.addEventListener("click", function () {
    window.location.href = "/app/jobs.html";
});

const viewApplicationsButton =
    document.getElementById("viewApplicationsButton");

viewApplicationsButton.addEventListener("click", function () {
    window.location.href = "/app/applications.html";
});
const viewProfileButton =
    document.getElementById("viewProfileButton");

viewProfileButton.addEventListener("click", function () {
    window.location.href = "/app/profile.html";
});