// Workstation right sidebar tab switcher: groups Stroke order, Context (companion + grammar),
// and Memory curve into compact, zero-scroll tabs on desktop.

function initSidebarTabs() {
  const isDesktop = document.body.classList.contains('is-desktop-dock');
  const mount = isDesktop ? document.getElementById('workstationRight') : null;
  if (!mount) return;

  if (document.getElementById('sidebarStudyTabs')) return;

  const savedTab = localStorage.getItem('hsk_sidebar_tab') || 'stroke';

  const nav = document.createElement('nav');
  nav.id = 'sidebarStudyTabs';
  nav.className = 'sidebar-study-tabs';
  nav.setAttribute('role', 'tablist');
  nav.setAttribute('aria-label', 'Chế độ xem các tiện ích từ vựng');
  nav.innerHTML = `
    <button type="button" class="sidebar-study-tab" data-tab="stroke" role="tab" aria-selected="false" title="Luyện thứ tự nét & viết chữ Hán">
      <span class="sidebar-tab-icon">✍️</span>
      <span class="sidebar-tab-label">Nét chữ</span>
    </button>
    <button type="button" class="sidebar-study-tab" data-tab="companion" role="tab" aria-selected="false" title="Câu ví dụ, ngữ pháp & từ liên quan">
      <span class="sidebar-tab-icon">📖</span>
      <span class="sidebar-tab-label">Ngữ cảnh</span>
    </button>
    <button type="button" class="sidebar-study-tab" data-tab="curve" role="tab" aria-selected="false" title="Dự đoán khả năng ghi nhớ (Ebbinghaus)">
      <span class="sidebar-tab-icon">📈</span>
      <span class="sidebar-tab-label">Ghi nhớ</span>
    </button>
    <button type="button" class="sidebar-study-tab sidebar-study-tab--all" data-tab="all" role="tab" aria-selected="false" title="Xem tất cả các thẻ cùng lúc">
      <span class="sidebar-tab-icon">📑</span>
      <span class="sidebar-tab-label">Tất cả</span>
    </button>
  `;

  mount.insertBefore(nav, mount.firstChild);

  function setActiveTab(tabKey, save = true) {
    const validTabs = ['stroke', 'companion', 'curve', 'all'];
    const active = validTabs.includes(tabKey) ? tabKey : 'stroke';
    document.body.dataset.sidebarTab = active;

    const tabs = nav.querySelectorAll('.sidebar-study-tab');
    tabs.forEach(btn => {
      const isMatch = btn.dataset.tab === active;
      btn.classList.toggle('active', isMatch);
      btn.setAttribute('aria-selected', isMatch ? 'true' : 'false');
    });

    if (save) {
      try { localStorage.setItem('hsk_sidebar_tab', active); } catch (e) {}
    }
  }

  nav.addEventListener('click', (e) => {
    const btn = e.target.closest('.sidebar-study-tab');
    if (btn && btn.dataset.tab) {
      setActiveTab(btn.dataset.tab, true);
    }
  });

  nav.addEventListener('keydown', (e) => {
    const tabs = Array.from(nav.querySelectorAll('.sidebar-study-tab'));
    const currentIdx = tabs.findIndex(t => t.classList.contains('active'));
    if (currentIdx === -1) return;

    if (e.key === 'ArrowRight') {
      e.preventDefault();
      const nextIdx = (currentIdx + 1) % tabs.length;
      tabs[nextIdx].focus();
      setActiveTab(tabs[nextIdx].dataset.tab, true);
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      const prevIdx = (currentIdx - 1 + tabs.length) % tabs.length;
      tabs[prevIdx].focus();
      setActiveTab(tabs[prevIdx].dataset.tab, true);
    }
  });

  setActiveTab(savedTab, false);
}

window.setSidebarStudyTab = function(tabKey) {
  const nav = document.getElementById('sidebarStudyTabs');
  if (!nav) return;
  const targetBtn = nav.querySelector(`[data-tab="${tabKey}"]`);
  if (targetBtn) targetBtn.click();
};

document.addEventListener('DOMContentLoaded', initSidebarTabs);
