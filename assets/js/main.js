document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const sidebar = document.querySelector('.sidebar');
    const content = document.querySelector('.main-content');

    hamburger.addEventListener('click', function() {
        hamburger.classList.toggle('active');
        sidebar.classList.toggle('active');
    });

    // Close menu when clicking outside
    content.addEventListener('click', function() {
        if (sidebar.classList.contains('active')) {
            hamburger.classList.remove('active');
            sidebar.classList.remove('active');
        }
    });
});