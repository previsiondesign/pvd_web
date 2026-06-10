// PreVision Design - Option B2: Boxed Canvas

document.addEventListener('DOMContentLoaded', () => {
  // Sticky header shadow
  const header = document.querySelector('.site-header');
  if (header) {
    window.addEventListener('scroll', () => {
      header.classList.toggle('scrolled', window.scrollY > 40);
    });
  }

  // Mobile nav toggle
  const toggle = document.querySelector('.mobile-toggle');
  const nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      toggle.classList.toggle('open');
      nav.classList.toggle('open');
    });
    nav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        toggle.classList.remove('open');
        nav.classList.remove('open');
      });
    });
  }

  // Hero slideshow: cycle slides, sync tagline to the active slide
  const slides = Array.from(document.querySelectorAll('.hero-slide'));
  const tagline = document.querySelector('.hero-tagline');
  const dotsWrap = document.querySelector('.hero-dots');
  if (slides.length > 1 && tagline && dotsWrap) {
    let current = 0;
    let timer = null;
    const dots = slides.map((s, i) => {
      const d = document.createElement('button');
      d.className = 'hero-dot' + (i === 0 ? ' is-active' : '');
      d.setAttribute('aria-label', 'Slide ' + (i + 1));
      d.addEventListener('click', () => { show(i); restart(); });
      dotsWrap.appendChild(d);
      return d;
    });
    function show(n) {
      if (n === current) return;
      slides[current].classList.remove('is-active');
      dots[current].classList.remove('is-active');
      current = n;
      slides[current].classList.add('is-active');
      dots[current].classList.add('is-active');
      tagline.classList.add('is-fading');
      setTimeout(() => {
        tagline.textContent = slides[current].dataset.tagline;
        tagline.classList.remove('is-fading');
      }, 400);
    }
    function restart() {
      clearInterval(timer);
      timer = setInterval(() => show((current + 1) % slides.length), 5000);
    }
    restart();
  }
});
