
// Mobile nav toggle
const toggle = document.getElementById('menuToggle');
const navList = document.getElementById('navList');
if (toggle) {
  toggle.addEventListener('click', () => {
    if (navList.style.display === 'flex') {
      navList.style.display = 'none';
    } else {
      navList.style.display = 'flex';
    }
  });
}

// Basic client-side validation + mailto fallback
const form = document.getElementById('contactForm');
if (form) {
  form.addEventListener('submit', (e)=>{
    e.preventDefault();
    const data = new FormData(form);
    const name = data.get('name');
    const email = data.get('email');
    const phone = data.get('phone') || '';
    const message = data.get('message');
    const body = encodeURIComponent(`Name: ${name}
Email: ${email}
Phone: ${phone}

Message:
${message}`);
    window.location.href = `mailto:keith@keithjones.cpa?subject=Free Strategy Call Request&body=${body}`;
  });
}
