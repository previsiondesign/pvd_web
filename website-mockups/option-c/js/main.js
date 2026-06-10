// PreVision Design - Option C: Narrative Scroll

document.addEventListener('DOMContentLoaded', () => {

  // ---- SCROLL PROGRESS BAR ----
  const progressBar = document.querySelector('.scroll-progress');
  function updateProgress() {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    if (progressBar) progressBar.style.width = pct + '%';
  }

  // ---- DOT NAVIGATION ----
  const dots = document.querySelectorAll('.dot-nav a');
  const sections = document.querySelectorAll('.narrative-section');

  function updateDots() {
    let current = 0;
    sections.forEach((sec, i) => {
      const rect = sec.getBoundingClientRect();
      if (rect.top <= window.innerHeight / 2) current = i;
    });
    dots.forEach((dot, i) => {
      dot.classList.toggle('active', i === current);
    });
  }

  // ---- SCROLL REVEAL ----
  const reveals = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

  reveals.forEach(el => observer.observe(el));

  // ---- TERMINAL LINES ----
  const terminalLines = document.querySelectorAll('.terminal-line');
  const terminalObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const box = entry.target.closest('.terminal-box');
        if (box) {
          const lines = box.querySelectorAll('.terminal-line');
          lines.forEach((line, i) => {
            setTimeout(() => line.classList.add('visible'), i * 200);
          });
        }
        terminalObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });

  // observe only the first terminal line to trigger all
  if (terminalLines.length > 0) {
    terminalObserver.observe(terminalLines[0]);
  }

  // ---- HERO CROSSFADE ----
  const heroImages = document.querySelectorAll('.hero-bg img');
  let currentHero = 0;
  if (heroImages.length > 0) {
    heroImages[0].classList.add('active');
    setInterval(() => {
      heroImages[currentHero].classList.remove('active');
      currentHero = (currentHero + 1) % heroImages.length;
      heroImages[currentHero].classList.add('active');
    }, 4000);
  }

  // ---- SCROLL-DRIVEN BEFORE/AFTER ----
  const baContainer = document.querySelector('.ba-container');
  function updateBeforeAfter() {
    if (!baContainer) return;
    const rect = baContainer.getBoundingClientRect();
    const vh = window.innerHeight;
    // map: when top of container is at bottom of viewport => 0%
    //       when top of container is at top of viewport => 100%
    let pct = 1 - (rect.top / vh);
    pct = Math.max(0, Math.min(1, pct));
    const afterEl = baContainer.querySelector('.ba-after');
    if (afterEl) {
      afterEl.style.clipPath = `inset(0 ${(1 - pct) * 100}% 0 0)`;
    }
  }

  // ---- SCROLL HANDLER ----
  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        updateProgress();
        updateDots();
        updateBeforeAfter();
        ticking = false;
      });
      ticking = true;
    }
  });

  // Initial calls
  updateProgress();
  updateDots();
  updateBeforeAfter();
});
