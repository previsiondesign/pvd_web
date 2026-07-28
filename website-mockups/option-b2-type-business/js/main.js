// Prevision Design - Option B2: Boxed Canvas

// Contact form delivery endpoint (Cloudflare Pages Function -> Resend).
// Set to '' to run the form in mockup mode (validates, shows the success panel,
// sends nothing and says so).
const FORM_ENDPOINT = 'https://clients.previsiondesign.com/api/contact';

// Attachment limits — keep in sync with functions/api/contact.js in the clients repo.
const MAX_FILES = 3;
const MAX_FILE_BYTES = 10 * 1024 * 1024;
const MAX_TOTAL_BYTES = 30 * 1024 * 1024;

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

  // Hero: five 6s series. Frames inside a series hold for their own data-dur
  // (mirroring the _#s in the master filenames), cross-fading between them.
  // Images/video load lazily: current series plus the next one.
  const series = Array.from(document.querySelectorAll('.hero-serie'));
  const tagline = document.querySelector('.hero-tagline');
  const dotsWrap = document.querySelector('.hero-dots');
  const heroEl = document.querySelector('.hero');
  if (series.length && tagline && dotsWrap) {
    const frameTimers = [];
    let current = 0;
    let serieTimer = null;

    const dots = series.map((s, i) => {
      const d = document.createElement('button');
      d.className = 'hero-dot' + (i === 0 ? ' is-active' : '');
      d.setAttribute('aria-label', 'Slide ' + (i + 1));
      d.addEventListener('click', () => { show(i); });
      dotsWrap.appendChild(d);
      return d;
    });

    const durations = series.map((s) =>
      Array.from(s.querySelectorAll('.hero-frame'))
        .reduce((sum, f) => sum + (parseInt(f.dataset.dur, 10) || 1000), 0)
    );

    function load(serie) {
      serie.querySelectorAll('img[data-src], video[data-src]').forEach((el) => {
        el.src = el.dataset.src;
        el.removeAttribute('data-src');
      });
    }

    function clearFrameTimers() {
      while (frameTimers.length) clearTimeout(frameTimers.pop());
    }

    // Step through a series' frames, holding each for its own duration.
    function runFrames(serie) {
      const frames = Array.from(serie.querySelectorAll('.hero-frame'));
      frames.forEach((f, i) => f.classList.toggle('is-shown', i === 0));
      let at = 0;
      frames.slice(0, -1).forEach((f, i) => {
        at += parseInt(f.dataset.dur, 10) || 1000;
        frameTimers.push(setTimeout(() => {
          frames[i].classList.remove('is-shown');
          frames[i + 1].classList.add('is-shown');
        }, at));
      });
      const video = serie.querySelector('video');
      if (video && video.src) {
        try { video.currentTime = 0; video.play(); } catch (err) { /* autoplay blocked */ }
      }
    }

    function show(n) {
      clearFrameTimers();
      clearTimeout(serieTimer);

      if (n !== current) {
        const prev = series[current];
        prev.classList.remove('is-active');
        dots[current].classList.remove('is-active');
        const prevVideo = prev.querySelector('video');
        if (prevVideo) prevVideo.pause();
        current = n;
      }

      const serie = series[current];
      load(serie);
      load(series[(current + 1) % series.length]); // warm the next one
      serie.classList.add('is-active');
      dots[current].classList.add('is-active');
      if (heroEl) heroEl.classList.toggle('is-contain', serie.classList.contains('fit-contain'));

      if (tagline.textContent !== serie.dataset.tagline) {
        tagline.classList.add('is-fading');
        setTimeout(() => {
          tagline.textContent = serie.dataset.tagline;
          tagline.classList.remove('is-fading');
        }, 400);
      }

      runFrames(serie);
      serieTimer = setTimeout(() => show((current + 1) % series.length), durations[current]);
    }

    show(0);
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

    // ---- optional attachments ----
    const fileInput = document.getElementById('files');
    const fileDrop = document.getElementById('file-drop');
    const attachList = document.getElementById('attach-list');
    let attachments = []; // File objects

    const fmtSize = (b) =>
      b >= 1e6 ? (b / 1e6).toFixed(1) + ' MB' : Math.max(1, Math.round(b / 1e3)) + ' KB';

    function renderAttachments() {
      attachList.innerHTML = '';
      attachments.forEach((f, i) => {
        const li = document.createElement('li');
        const nm = document.createElement('span');
        nm.className = 'aname';
        nm.textContent = f.name;
        const sz = document.createElement('span');
        sz.className = 'asize';
        sz.textContent = fmtSize(f.size);
        const rm = document.createElement('button');
        rm.type = 'button';
        rm.className = 'aremove';
        rm.setAttribute('aria-label', 'Remove ' + f.name);
        rm.textContent = '×';
        rm.addEventListener('click', () => {
          attachments.splice(i, 1);
          renderAttachments();
        });
        li.append(nm, sz, rm);
        attachList.appendChild(li);
      });
    }

    function addFiles(list) {
      errorBox.hidden = true;
      for (const f of list) {
        if (attachments.length >= MAX_FILES) {
          errorBox.textContent = `You can attach up to ${MAX_FILES} files — send the form and we'll reply with an upload link for the rest.`;
          errorBox.hidden = false;
          break;
        }
        if (f.size > MAX_FILE_BYTES) {
          errorBox.textContent = `"${f.name}" is larger than 10 MB — send the form and we'll reply with an upload link.`;
          errorBox.hidden = false;
          continue;
        }
        const total = attachments.reduce((n, a) => n + a.size, 0) + f.size;
        if (total > MAX_TOTAL_BYTES) {
          errorBox.textContent = 'Attachments total more than 30 MB — please remove one.';
          errorBox.hidden = false;
          continue;
        }
        attachments.push(f);
      }
      renderAttachments();
    }

    if (fileDrop && fileInput) {
      fileDrop.addEventListener('click', () => fileInput.click());
      fileDrop.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fileInput.click(); }
      });
      fileInput.addEventListener('change', () => { addFiles(fileInput.files); fileInput.value = ''; });
      ['dragenter', 'dragover'].forEach((ev) =>
        fileDrop.addEventListener(ev, (e) => { e.preventDefault(); fileDrop.classList.add('drag'); })
      );
      ['dragleave', 'drop'].forEach((ev) =>
        fileDrop.addEventListener(ev, (e) => { e.preventDefault(); fileDrop.classList.remove('drag'); })
      );
      fileDrop.addEventListener('drop', (e) => addFiles(e.dataTransfer.files));
    }

    const toBase64 = (file) =>
      new Promise((resolve, reject) => {
        const r = new FileReader();
        r.onload = () => resolve(String(r.result).split(',')[1] || '');
        r.onerror = () => reject(new Error('read failed'));
        r.readAsDataURL(file);
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
      btn.textContent = attachments.length ? 'Uploading…' : 'Sending…';

      if (FORM_ENDPOINT) {
        try {
          payload.files = await Promise.all(
            attachments.map(async (f) => ({
              name: f.name,
              type: f.type,
              size: f.size,
              data: await toBase64(f),
            }))
          );
          const res = await fetch(FORM_ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
            body: JSON.stringify(payload),
          });
          if (!res.ok) {
            let msg = '';
            try { msg = (await res.json()).error || ''; } catch { /* non-JSON */ }
            // 503 = endpoint deployed but no mail key yet; don't show internals.
            if (res.status === 503) msg = 'The form isn’t live yet.';
            throw new Error(msg || 'bad status ' + res.status);
          }
        } catch (err) {
          btn.disabled = false;
          btn.textContent = 'Send Inquiry';
          errorBox.textContent =
            (err && err.message && !/bad status/.test(err.message) ? err.message + ' ' : '') +
            'Please try again, or email info@previsiondesign.com directly.';
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
