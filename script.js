document.addEventListener('DOMContentLoaded', () => {
  const mobileToggle = document.getElementById('mobileToggle');
  const navMenu = document.getElementById('navMenu');

  const setMenuOpen = (open) => {
    if (!navMenu || !mobileToggle) return;
    navMenu.classList.toggle('open', open);
    mobileToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  };

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', () => {
      setMenuOpen(!navMenu.classList.contains('open'));
    });

    navMenu.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => setMenuOpen(false));
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') setMenuOpen(false);
    });
  }

  const sections = document.querySelectorAll('main section[id]');
  const navLinks = document.querySelectorAll('.nav-link[href^="#"]');

  if (sections.length && navLinks.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const activeId = entry.target.id;
        navLinks.forEach((link) => {
          link.classList.toggle('active', link.getAttribute('href') === `#${activeId}`);
        });
      });
    }, {
      root: null,
      rootMargin: '-20% 0px -60% 0px',
      threshold: 0
    });

    sections.forEach((section) => observer.observe(section));
  }

  document.querySelectorAll('.share-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const url = btn.getAttribute('data-url') || window.location.href;
      const label = btn.querySelector('.share-label');
      if (!navigator.clipboard || !label) return;

      try {
        await navigator.clipboard.writeText(url);
      } catch {
        return;
      }

      const original = label.textContent;
      label.textContent = 'Copied link';
      window.setTimeout(() => {
        label.textContent = original;
      }, 2500);
    });
  });
});
