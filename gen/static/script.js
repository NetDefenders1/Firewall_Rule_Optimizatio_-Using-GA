document.addEventListener('DOMContentLoaded', function() {
    console.log("Custom JavaScript Loaded");

    const uploadFile = document.querySelector('input[type="file"]');
    if (uploadFile) {
        uploadFile.addEventListener('change', function() {
            alert('File uploaded successfully!');
        });
    }
});
