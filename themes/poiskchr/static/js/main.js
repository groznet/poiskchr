// Utility: toggle visibility with ARIA updates
function toggleSection(button, content) {
  const expanded = button.getAttribute('aria-expanded') === 'true';
  button.setAttribute('aria-expanded', String(!expanded));
  if (content) {
    content.classList.toggle('hidden', expanded);
  }
}

// Initialize accordion controls (desktop  mobile)
document.querySelectorAll('[data-accordion-control]').forEach(function (btn) {
  const controlsId = btn.getAttribute('aria-controls');
  const content = controlsId ? document.getElementById(controlsId) : null;
  btn.addEventListener('click', function () { toggleSection(btn, content); });
});

// Mobile drawer behavior
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileDrawer = document.getElementById('mobileDrawer');
const mobileDrawerClose = document.getElementById('mobileDrawerClose');
const drawerPanel = mobileDrawer ? mobileDrawer.querySelector('aside') : null;

function openDrawer() {
  if (!mobileDrawer || !drawerPanel) return;
  mobileDrawer.classList.remove('hidden');
  requestAnimationFrame(function () {
    drawerPanel.classList.remove('-translate-x-full');
  });
}
function closeDrawer() {
  if (!mobileDrawer || !drawerPanel) return;
  drawerPanel.classList.add('-translate-x-full');
  setTimeout(function () { mobileDrawer.classList.add('hidden'); }, 180);
}

if (mobileMenuBtn) mobileMenuBtn.addEventListener('click', openDrawer);
if (mobileDrawerClose) mobileDrawerClose.addEventListener('click', closeDrawer);
if (mobileDrawer) mobileDrawer.addEventListener('click', function (e) {
  if (e.target === mobileDrawer) closeDrawer();
});

// Current year in footer
document.getElementById('year').textContent = new Date().getFullYear();