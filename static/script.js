document.addEventListener("DOMContentLoaded", function () {
    // Trigger fade-in effect for elements with the 'fade-in' class
    var fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach(function(element) {
        element.classList.add('show');
    });
});