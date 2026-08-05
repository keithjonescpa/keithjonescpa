
// Mobile nav toggle
const toggle = document.getElementById('menuToggle');
const navList = document.getElementById('navList');
if (toggle) {
  toggle.addEventListener('click', () => {
    const open = navList.style.display === 'flex';
    navList.style.display = open ? 'none' : 'flex';
    // Keep assistive tech informed; the visual state alone is not announced.
    toggle.setAttribute('aria-expanded', String(!open));
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

// Wage garnishment estimator (CCPA Title III general limit).
// Runs only on the calculator page. IRS levies use different rules and are
// intentionally not estimated here.
const garnishCalc = document.getElementById('garnishCalc');
if (garnishCalc) {
  const result = document.getElementById('garnishResult');
  // Weekly-equivalent multiples of the minimum wage per pay period (30x weekly).
  const FLOOR_MULTIPLE = { weekly: 30, biweekly: 60, semimonthly: 65, monthly: 130 };
  const PERIOD_LABEL = {
    weekly: 'weekly',
    biweekly: 'every-two-weeks',
    semimonthly: 'twice-monthly',
    monthly: 'monthly',
  };
  const usd = (n) => n.toLocaleString('en-US', { style: 'currency', currency: 'USD' });

  garnishCalc.addEventListener('submit', (e) => {
    e.preventDefault();
    const data = new FormData(garnishCalc);
    const freq = data.get('frequency');
    const disposable = parseFloat(data.get('disposable'));
    const minWage = parseFloat(data.get('minwage'));

    if (!FLOOR_MULTIPLE[freq] || !isFinite(disposable) || disposable < 0 || !isFinite(minWage) || minWage < 0) {
      result.textContent = 'Enter a pay frequency, disposable earnings, and minimum wage to see an estimate.';
      return;
    }

    const protectedFloor = FLOOR_MULTIPLE[freq] * minWage;   // 30x weekly min wage, scaled to the pay period
    const cap25 = disposable * 0.25;                          // 25% of disposable earnings
    const capOverFloor = Math.max(0, disposable - protectedFloor);
    const maxGarnish = Math.max(0, Math.min(cap25, capOverFloor));
    const keep = disposable - maxGarnish;

    const lead = maxGarnish <= 0
      ? `Based on these numbers, an ordinary creditor generally <strong>cannot garnish</strong> your ${PERIOD_LABEL[freq]} pay—your disposable earnings are at or below the protected floor of ${usd(protectedFloor)}.`
      : `The most a general creditor could garnish from this ${PERIOD_LABEL[freq]} paycheck is about <strong>${usd(maxGarnish)}</strong>, leaving you about <strong>${usd(keep)}</strong>.`;

    result.innerHTML =
      `<p>${lead}</p>` +
      `<p class='small'>This is the lesser of 25% of disposable earnings (${usd(cap25)}) and the amount above the protected floor of ${usd(protectedFloor)} (30&times; the minimum wage, scaled to your pay period).</p>` +
      `<p class='small'>An IRS wage levy, child support, or a student-loan garnishment can take a different amount. This estimate is for education only—not legal or tax advice.</p>`;
  });
}
