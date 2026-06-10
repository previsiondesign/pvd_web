// Prevision Design - Option A: Gallery-Forward

document.addEventListener('DOMContentLoaded', () => {

  // ---- HAMBURGER & NAV OVERLAY ----
  const hamburger = document.querySelector('.hamburger');
  const overlay = document.querySelector('.nav-overlay');
  if (hamburger && overlay) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('open');
      overlay.classList.toggle('open');
      document.body.style.overflow = overlay.classList.contains('open') ? 'hidden' : '';
    });
    overlay.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('open');
        overlay.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }

  // ---- BEFORE/AFTER SLIDER ----
  const slider = document.querySelector('.hero-slider');
  if (slider) {
    const afterImg = slider.querySelector('.after-img');
    const handle = slider.querySelector('.slider-handle');
    let isDragging = false;

    function updateSlider(x) {
      const rect = slider.getBoundingClientRect();
      let pct = ((x - rect.left) / rect.width) * 100;
      pct = Math.max(5, Math.min(95, pct));
      afterImg.style.clipPath = `inset(0 ${100 - pct}% 0 0)`;
      handle.style.left = pct + '%';
    }

    slider.addEventListener('mousedown', (e) => { isDragging = true; updateSlider(e.clientX); });
    window.addEventListener('mousemove', (e) => { if (isDragging) updateSlider(e.clientX); });
    window.addEventListener('mouseup', () => { isDragging = false; });

    slider.addEventListener('touchstart', (e) => { isDragging = true; updateSlider(e.touches[0].clientX); }, { passive: true });
    window.addEventListener('touchmove', (e) => { if (isDragging) updateSlider(e.touches[0].clientX); }, { passive: true });
    window.addEventListener('touchend', () => { isDragging = false; });
  }

  // ---- PORTFOLIO FILTER ----
  const pills = document.querySelectorAll('.pill');
  const items = document.querySelectorAll('.masonry-item');
  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      const filter = pill.dataset.filter;
      pills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      items.forEach(item => {
        item.style.display = (filter === 'all' || item.dataset.category === filter) ? '' : 'none';
      });
    });
  });

  // ---- LIGHTBOX ----
  const lightbox = document.querySelector('.lightbox');
  const lbImg = lightbox?.querySelector('img');
  const lbTitle = lightbox?.querySelector('h4');
  const lbLoc = lightbox?.querySelector('p');
  const lbClose = lightbox?.querySelector('.lightbox-close');

  items.forEach(item => {
    item.addEventListener('click', () => {
      if (!lightbox) return;
      const img = item.querySelector('img');
      const title = item.querySelector('h4')?.textContent || '';
      const loc = item.querySelector('.loc')?.textContent || '';
      lbImg.src = img.src;
      lbImg.alt = title;
      if (lbTitle) lbTitle.textContent = title;
      if (lbLoc) lbLoc.textContent = loc;
      lightbox.classList.add('open');
      document.body.style.overflow = 'hidden';
    });
  });

  if (lbClose) {
    lbClose.addEventListener('click', closeLightbox);
  }
  lightbox?.addEventListener('click', (e) => {
    if (e.target === lightbox) closeLightbox();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeLightbox();
  });

  function closeLightbox() {
    lightbox?.classList.remove('open');
    document.body.style.overflow = '';
  }
});
