/**
 * Dura Navigation - Mobile hamburger menu toggle
 * Include this script on every dura/ page.
 */
(function() {
    var hamburger = document.querySelector('.hamburger');
    var navLinks = document.querySelector('.nav-links');
    if (!hamburger || !navLinks) return;

    hamburger.addEventListener('click', function(e) {
        e.stopPropagation();
        var isOpen = navLinks.classList.toggle('mobile-open');
        hamburger.classList.toggle('active', isOpen);
        hamburger.setAttribute('aria-expanded', String(isOpen));
    });

    // Close on click outside
    document.addEventListener('click', function(e) {
        if (!navLinks.classList.contains('mobile-open')) return;
        if (!e.target.closest('.nav-left') && !e.target.closest('.hamburger')) {
            navLinks.classList.remove('mobile-open');
            hamburger.classList.remove('active');
            hamburger.setAttribute('aria-expanded', 'false');
        }
    });

    // Close on Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && navLinks.classList.contains('mobile-open')) {
            navLinks.classList.remove('mobile-open');
            hamburger.classList.remove('active');
            hamburger.setAttribute('aria-expanded', 'false');
        }
    });

    // Close on nav link click
    navLinks.addEventListener('click', function(e) {
        if (e.target.tagName === 'A') {
            navLinks.classList.remove('mobile-open');
            hamburger.classList.remove('active');
            hamburger.setAttribute('aria-expanded', 'false');
        }
    });
})();
