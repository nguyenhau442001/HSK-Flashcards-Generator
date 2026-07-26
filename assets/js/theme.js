// Manual light/dark theme selection.
function toggleTheme() {
  const current = document.documentElement.dataset.theme ||
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  const next = current === 'dark' ? 'light' : 'dark';
  localStorage.setItem('hsk_theme', next);
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('theme-transition');
    setTimeout(() => document.documentElement.classList.remove('theme-transition'), 200);
  }
  document.documentElement.dataset.theme = next;
  document.getElementById('themeToggle').textContent = next === 'dark' ? '☀️' : '🌙';
}
(function () {
  const effective = document.documentElement.dataset.theme ||
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  document.getElementById('themeToggle').textContent = effective === 'dark' ? '☀️' : '🌙';
})();
