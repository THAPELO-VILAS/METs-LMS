// const enrollButtons = document.querySelectorAll('.btn');

// enrollButtons.forEach(button => {
//     button.addEventListener('click', () => {
//         alert("Thank you for enrolling! (Functionality to connect with backend coming next)");
//     });
// });

// document.querySelector("form")?.addEventListener("submit", function(e) {
//     e.preventDefault();

//     // Simulate login
//     localStorage.setItem("user", "logged_in");

//     window.location.href = "dashboard.html";
// });

// // Logout functionality
// document.getElementById("logoutBtn")?.addEventListener("click", function(e) {
//     e.preventDefault();

//     // Clear session (for now simulated)
//     localStorage.removeItem("user");

//     alert("You have been logged out");

//     // Redirect to login page
//     window.location.href = "login.html";
// });


// ==========================
// ENROLL BUTTONS (Courses only)
// ==========================
const enrollButtons = document.querySelectorAll('.enroll-btn');

enrollButtons.forEach(button => {
    button.addEventListener('click', () => {
        alert("Thank you for enrolling! (Backend coming next)");
    });
});


// ==========================
// LOGIN FUNCTIONALITY
// ==========================
const loginForm = document.querySelector("#loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", function(e) {
        e.preventDefault();

        // Simulate login
        localStorage.setItem("user", "logged_in");

        window.location.href = "dashboard.html";
    });
}


// ==========================
// LOGOUT FUNCTIONALITY
// ==========================
// const logoutBtn = document.getElementById("logoutBtn");

// if (logoutBtn) {
//     logoutBtn.addEventListener("click", function(e) {
//         e.preventDefault();

//         localStorage.removeItem("user");

//         alert("You have been logged out");

//         window.location.href = "login.html";
//     });
// }

document.addEventListener("DOMContentLoaded", function () {

    // ==========================
    // LOGOUT FUNCTIONALITY
    // ==========================
    const logoutBtn = document.getElementById("logoutBtn");

    if (logoutBtn) {
        logoutBtn.addEventListener("click", function(e) {
            e.preventDefault();

            localStorage.removeItem("user");

            alert("You have been logged out");

            window.location.href = "login.html";
        });
    }

});

document.addEventListener("DOMContentLoaded", () => {

    // Get all course enroll buttons
    const enrollButtons = document.querySelectorAll(".enroll-btn");

    enrollButtons.forEach(button => {
        button.addEventListener("click", (e) => {
            e.preventDefault();

            // Check if user is logged in
            const user = localStorage.getItem("user");
            if (!user) {
                alert("Please login first to enroll in a course");
                window.location.href = "login.html";
                return;
            }

            // Get course name from card
            const courseCard = e.target.closest(".course-card");
            const courseName = courseCard.querySelector("h3").innerText;

            // Save enrolled courses
            let enrolledCourses = JSON.parse(localStorage.getItem("enrolledCourses")) || [];
            if (!enrolledCourses.includes(courseName)) {
                enrolledCourses.push(courseName);
                localStorage.setItem("enrolledCourses", JSON.stringify(enrolledCourses));
                alert(`You have successfully enrolled in "${courseName}"!`);
            } else {
                alert(`You are already enrolled in "${courseName}".`);
            }

            // Optionally redirect to dashboard
            window.location.href = "dashboard.html";
        });
    });

});

document.addEventListener("DOMContentLoaded", () => {
    const myCoursesList = document.getElementById("myCoursesList");
    const enrolledCourses = JSON.parse(localStorage.getItem("enrolledCourses")) || [];

    if (myCoursesList) {
        if (enrolledCourses.length === 0) {
            myCoursesList.innerHTML = "<li>No courses enrolled yet.</li>";
        } else {
            enrolledCourses.forEach(course => {
                const li = document.createElement("li");
                li.textContent = course;
                myCoursesList.appendChild(li);
            });
        }
    }
});