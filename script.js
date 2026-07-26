document.addEventListener('DOMContentLoaded', () => {
  // Mobile Nav Toggle
  const mobileToggle = document.getElementById('mobileToggle');
  const navMenu = document.getElementById('navMenu');

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', () => {
      navMenu.classList.toggle('open');
    });
  }

  // Smooth Scroll Active Link Highlight
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link');

  const observerOptions = {
    root: null,
    rootMargin: '-20% 0px -60% 0px',
    threshold: 0
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const activeId = entry.target.getAttribute('id');
        navLinks.forEach((link) => {
          link.classList.remove('active');
          if (link.getAttribute('href') === `#${activeId}`) {
            link.classList.add('active');
          }
        });
      }
    });
  }, observerOptions);

  sections.forEach((section) => observer.observe(section));

  // Essay Tab Switching
  const tabBtns = document.querySelectorAll('.tab-btn');
  const essayCards = document.querySelectorAll('.essay-card');

  tabBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');

      tabBtns.forEach((b) => b.classList.remove('active'));
      essayCards.forEach((c) => c.classList.remove('active'));

      btn.classList.add('active');
      const targetCard = document.getElementById(targetId);
      if (targetCard) {
        targetCard.classList.add('active');
      }
    });
  });

  // Share / Copy Link Helper
  const shareBtns = document.querySelectorAll('.share-btn');
  shareBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      const essayTitle = btn.getAttribute('data-title') || 'Essay';
      const url = window.location.href;

      if (navigator.clipboard) {
        navigator.clipboard.writeText(url).then(() => {
          const originalText = btn.innerHTML;
          btn.innerHTML = `<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg> Copied Link!`;
          setTimeout(() => {
            btn.innerHTML = originalText;
          }, 2500);
        });
      }
    });
  });
});
