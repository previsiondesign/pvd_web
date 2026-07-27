// Prevision Design - Option B2: Boxed Canvas

// Contact form delivery endpoint. Leave empty and the form runs in mockup mode
// (validates, shows the success panel, sends nothing). Set it to a form service
// or serverless endpoint that accepts a JSON POST to go live.
const FORM_ENDPOINT = '';

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

  // Hero slideshow: cycle slides, sync tagline to the active slide.
  // Slides marked .has-ba run a before/after sequence when shown:
  // 1s on the before image, 1s crossfade, then hold the after image.
  const slides = Array.from(document.querySelectorAll('.hero-slide'));
  const tagline = document.querySelector('.hero-tagline');
  const dotsWrap = document.querySelector('.hero-dots');
  if (slides.length > 1 && tagline && dotsWrap) {
    let current = 0;
    let timer = null;
    let baTimer = null;
    const dots = slides.map((s, i) => {
      const d = document.createElement('button');
      d.className = 'hero-dot' + (i === 0 ? ' is-active' : '');
      d.setAttribute('aria-label', 'Slide ' + (i + 1));
      d.addEventListener('click', () => { show(i); restart(); });
      dotsWrap.appendChild(d);
      return d;
    });
    function runBeforeAfter(slide) {
      clearTimeout(baTimer);
      if (!slide.classList.contains('has-ba')) return;
      slide.classList.remove('ba-shown');
      baTimer = setTimeout(() => {
        if (slide.classList.contains('is-active')) slide.classList.add('ba-shown');
      }, 1000);
    }
    function show(n) {
      if (n === current) return;
      const prev = slides[current];
      prev.classList.remove('is-active');
      dots[current].classList.remove('is-active');
      // reset the outgoing slide's before/after state once it has faded out
      setTimeout(() => {
        if (!prev.classList.contains('is-active')) prev.classList.remove('ba-shown');
      }, 1300);
      current = n;
      slides[current].classList.add('is-active');
      dots[current].classList.add('is-active');
      runBeforeAfter(slides[current]);
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
    runBeforeAfter(slides[0]);
    restart();
  }

  // Contact form (contact.html)
  const form = document.getElementById('contact-form');
  if (form) {
    const errorBox = document.getElementById('form-error');
    const success = document.getElementById('form-success');
    const demoNote = document.getElementById('demo-note');
    const btn = document.getElementById('submit-btn');

    const clearInvalid = (el) => el.classList.remove('invalid');
    form.querySelectorAll('input, textarea').forEach((el) => {
      el.addEventListener('input', () => clearInvalid(el));
    });

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      errorBox.hidden = true;

      // Validate required fields + email shape.
      const required = ['name', 'email', 'message'];
      let firstBad = null;
      for (const id of required) {
        const el = document.getElementById(id);
        const empty = !el.value.trim();
        el.classList.toggle('invalid', empty);
        if (empty && !firstBad) firstBad = el;
      }
      const email = document.getElementById('email');
      if (!firstBad && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
        email.classList.add('invalid');
        firstBad = email;
        errorBox.textContent = 'Please enter a valid email address so we can reply.';
        errorBox.hidden = false;
        email.focus();
        return;
      }
      if (firstBad) {
        errorBox.textContent = 'Please fill in the required fields marked with *.';
        errorBox.hidden = false;
        firstBad.focus();
        return;
      }

      // Silently drop bot submissions that fill the hidden field.
      if (document.getElementById('website').value) return;

      const payload = {
        name: document.getElementById('name').value.trim(),
        email: email.value.trim(),
        company: document.getElementById('company').value.trim(),
        phone: document.getElementById('phone').value.trim(),
        project: document.getElementById('project').value.trim(),
        services: [...form.querySelectorAll('input[name="services"]:checked')].map((c) => c.value),
        message: document.getElementById('message').value.trim(),
      };

      btn.disabled = true;
      btn.textContent = 'Sending…';

      if (FORM_ENDPOINT) {
        try {
          const res = await fetch(FORM_ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
            body: JSON.stringify(payload),
          });
          if (!res.ok) throw new Error('bad status ' + res.status);
        } catch (err) {
          btn.disabled = false;
          btn.textContent = 'Send Inquiry';
          errorBox.textContent = 'Sorry — that didn’t go through. Please email info@previsiondesign.com instead.';
          errorBox.hidden = false;
          return;
        }
      } else {
        demoNote.hidden = false; // mockup mode: be explicit that nothing was sent
      }

      form.hidden = true;
      success.hidden = false;
      success.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  }
});
