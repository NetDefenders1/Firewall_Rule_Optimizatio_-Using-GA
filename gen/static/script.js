document.addEventListener('DOMContentLoaded', function() {
    console.log("Custom JavaScript Loaded");

    const uploadFile = document.querySelector('input[type="file"]');
    if (uploadFile) {
        uploadFile.addEventListener('change', function() {
            alert('File uploaded successfully!');
        });
    }
});document.addEventListener('DOMContentLoaded', function() {
    console.log("Custom JavaScript Loaded");

    const uploadFile = document.querySelector('input[type="file"]');
    if (uploadFile) {
        uploadFile.addEventListener('change', function() {
            alert('File uploaded successfully!');
        });
    }

    // Add event listener for the recover password functionality
    const auth = getAuth();
    const repass = document.getElementById("repass");
    repass.addEventListener("click", function() {
        const email = document.getElementById('email').value;
        if (email) {
            sendPasswordResetEmail(auth, email)
                .then(() => {
                    alert("Password reset email sent");
                })
                .catch((error) => {
                    alert("Error: " + error.message);
                });
        } else {
            alert("Please enter your email address first");
        }
    });
});

