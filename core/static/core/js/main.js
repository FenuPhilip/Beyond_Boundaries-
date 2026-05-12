// DarkMatter — Interactive JS

// ── Mobile nav ──
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');
if (hamburger && mobileMenu) {
  hamburger.addEventListener('click', () => {
    mobileMenu.classList.toggle('open');
  });
  document.addEventListener('click', (e) => {
    if (!hamburger.contains(e.target) && !mobileMenu.contains(e.target)) {
      mobileMenu.classList.remove('open');
    }
  });
}

// ── Scroll-reveal ──
const observer = new IntersectionObserver((entries) => {
  entries.forEach(el => {
    if (el.isIntersecting) {
      el.target.classList.add('visible');
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

// ── Navbar scroll effect ──
const navbar = document.querySelector('.navbar');
let lastScroll = 0;
window.addEventListener('scroll', () => {
  const current = window.scrollY;
  if (current > 80) {
    navbar?.classList.add('scrolled');
  } else {
    navbar?.classList.remove('scrolled');
  }
  lastScroll = current;
}, { passive: true });

// ── Particle dots effect on hero ──
function createParticles() {
  const hero = document.querySelector('.hero-bg');
  if (!hero) return;
  for (let i = 0; i < 30; i++) {
    const dot = document.createElement('div');
    dot.style.cssText = `
      position: absolute;
      width: 2px; height: 2px;
      background: #2dff7f;
      border-radius: 50%;
      top: ${Math.random() * 100}%;
      left: ${Math.random() * 100}%;
      opacity: ${Math.random() * 0.4 + 0.05};
      animation: twinkle ${Math.random() * 4 + 2}s ${Math.random() * 4}s ease-in-out infinite;
    `;
    hero.appendChild(dot);
  }
}

// Add twinkle animation
const style = document.createElement('style');
style.textContent = `
  @keyframes twinkle {
    0%, 100% { opacity: 0.05; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.5); }
  }
  .reveal { opacity: 0; transform: translateY(24px); transition: opacity 0.7s ease, transform 0.7s ease; }
  .reveal.visible { opacity: 1; transform: none; }
  .navbar.scrolled { background: rgba(5,6,8,0.98); }
`;
document.head.appendChild(style);

document.addEventListener('DOMContentLoaded', () => {
  createParticles();
  // Stagger reveal
  document.querySelectorAll('.reveal').forEach((el, i) => {
    el.style.transitionDelay = `${i * 0.06}s`;
  });
});

// ── Form: dynamic "other" fields ──
function watchSelect(selectId, targetId) {
  const sel = document.getElementById(selectId);
  const target = document.getElementById(targetId);
  if (!sel || !target) return;
  function toggle() {
    target.style.display = sel.value === 'other' ? 'block' : 'none';
    if (sel.value !== 'other') target.querySelector('input, textarea').value = '';
  }
  sel.addEventListener('change', toggle);
  toggle();
}

document.addEventListener('DOMContentLoaded', () => {
  watchSelect('id_domain', 'domain-other-group');
  watchSelect('id_mentorship_type', 'mentorship-other-group');
  watchSelect('id_primary_domain', 'domain-other-group');
});
