// HSK 3.0 level picker: version switcher + dynamic grid, reusing the LEVELS/selectLevel pipeline.
const PICKER_VERSION_STORAGE_KEY = 'hsk_picker_version';
let pickerVersion = '2.0';

function getInitialPickerVersion() {
  try {
    const params = new URLSearchParams(window.location.search);
    const paramVer = params.get('version');
    if (paramVer === '2.0' || paramVer === '3.0') return paramVer;
  } catch (e) {}
  try {
    const saved = localStorage.getItem(PICKER_VERSION_STORAGE_KEY);
    if (saved === '2.0' || saved === '3.0') return saved;
  } catch (e) {}
  return '2.0';
}

function setPickerVersion(version) {
  pickerVersion = version;
  try {
    localStorage.setItem(PICKER_VERSION_STORAGE_KEY, version);
  } catch (e) {}
  const selector = document.getElementById('pickerVersionSelect');
  if (selector) selector.value = version;
  const g20 = document.getElementById('levelGrid20');
  const g30 = document.getElementById('levelGrid30');
  if (g20) g20.style.display = version === '2.0' ? '' : 'none';
  if (g30) g30.style.display = version === '3.0' ? '' : 'none';
  if (version === '3.0') renderHsk30Grid();
}

document.addEventListener('DOMContentLoaded', () => {
  const initVer = getInitialPickerVersion();
  if (initVer && initVer !== '2.0') {
    setPickerVersion(initVer);
  }
});

function hsk30KnownCount(level) {
  const data = readSavedLevelProgress(level);
  return Object.values(data).filter(status => status === 'known').length;
}

function renderHsk30Grid() {
  const grid = document.getElementById('levelGrid30');
  if (!grid) return;

  // Same card layout as the HSK 2.0 grid; one row per band (Sơ / Trung / Cao cấp).
  grid.innerHTML = hsk30LevelKeys().map(key => {
    const cfg = LEVELS_HSK30[key];
    const known = hsk30KnownCount(key);
    const pct = cfg.total > 0 ? Math.round(known / cfg.total * 100) : 0;
    const complete = known >= cfg.total;
    const isLearning = known > 0 && !complete;
    const statusClass = complete ? ' is-complete' : isLearning ? ' is-learning' : '';
    const statusText = complete ? 'Đã hoàn thành' : isLearning ? 'Đang học' : 'Chưa học';
    const shortLabel = 'HSK' + key.replace('hsk30_', '');
    return `
      <button class="level-card ${cfg.available ? '' : 'disabled'}${complete ? ' is-complete-level' : ''}" type="button" data-level="${key}"
        aria-label="${cfg.label}" ${cfg.available ? `onclick="selectLevel('${key}')"` : 'disabled'}>
        <div class="level-card-top">
          <div class="level-card-heading"><div class="lvl-num">${shortLabel}</div><span class="level-status-badge${statusClass}">${cfg.available ? statusText : 'Sắp có'}</span></div>
          <div class="level-card-meta" title="${cfg.sharedVocabularyGroup ? 'HSK 3.0 cấp ' + cfg.sharedVocabularyGroup + ': danh sách từ vựng dùng chung' : ''}"><span class="lvl-label">${cfg.band}</span><span aria-hidden="true">·</span><span class="lvl-count">${cfg.total.toLocaleString('vi-VN')} từ</span></div>
        </div>
        ${cfg.available
          ? `<div class="level-card-progress">
               <div class="level-card-progress-heading"><strong class="lvl-percent-value">${pct}%</strong><span class="lvl-today-count">+0 từ hôm nay</span></div>
               <div class="lvl-mastery-track"><div class="lvl-mastery-fill" style="width:${pct}%"></div></div>
             </div>
             <div class="lvl-mastery-text">${known.toLocaleString('vi-VN')} / ${cfg.total.toLocaleString('vi-VN')} đã nhớ</div>`
          : `<div class="lvl-soon">Nội dung đang được chuẩn bị</div>`}
      </button>`;
  }).join('');
}
