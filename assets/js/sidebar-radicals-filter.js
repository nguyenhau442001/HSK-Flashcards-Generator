// Compact desktop entry point into the searchable 214-radical directory.
// Below 1280px the same entry lives in the "Công cụ" menu instead (.primary-menu-radical-lookup).
function initSidebarRadicalsFilter() {
  if (!document.body.classList.contains('is-desktop-dock')) return;
  const mount = document.getElementById('workstationLeft');
  if (!mount) return;

  const wrap = document.createElement('section');
  wrap.className = 'sidebar-radicals-filter';
  wrap.innerHTML = `
    <div class="sidebar-panel-title">Tra cứu bộ thủ</div>
    <p class="sidebar-radical-summary">50 bộ cơ bản và 214 bộ Khang Hy, có thể tìm theo chữ hoặc nghĩa.</p>
    <button type="button" class="sidebar-radical-directory-btn" onclick="openRadicalDirectory()">
      Mở danh sách 214 bộ <span aria-hidden="true">→</span>
    </button>
  `;
  mount.appendChild(wrap);
}

document.addEventListener('DOMContentLoaded', initSidebarRadicalsFilter);
