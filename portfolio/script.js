// ============================================
// INSTITUTIONAL TERMINAL - MINIMAL JS
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize any interactive elements
    initializeTickerScroll();
});

/**
 * Optional: Add a subtle scroll effect to the ticker
 * This creates a "data stream" feel without being distracting
 */
function initializeTickerScroll() {
    const ticker = document.querySelector('.system-ticker');

    if (!ticker) return;

    // Add shadow on scroll to indicate fixed header
    window.addEventListener('scroll', () => {
        if (window.scrollY > 10) {
            ticker.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.5)';
        } else {
            ticker.style.boxShadow = 'none';
        }
    }, { passive: true });
}

/**
 * Optional: Add a "typing" effect to the mission statement on load
 * Uncomment below if you want this effect
 */
// function typeWriter(element, text, speed = 30) {
//     let i = 0;
//     element.textContent = '';
//     function type() {
//         if (i < text.length) {
//             element.textContent += text.charAt(i);
//             i++;
//             setTimeout(type, speed);
//         }
//     }
//     type();
// }
