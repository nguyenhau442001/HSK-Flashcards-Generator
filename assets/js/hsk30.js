// HSK 3.0 level picker: version switcher + dynamic grid, reusing the LEVELS/selectLevel pipeline.
let pickerVersion = '2.0';

function setPickerVersion(version) {
  pickerVersion = version;
  document.getElementById('pickerVersionTab20').classList.toggle('active', version === '2.0');
  document.getElementById('pickerVersionTab30').classList.toggle('active', version === '3.0');
  document.getElementById('pickerVersionTab20').setAttribute('aria-selected', String(version === '2.0'));
  document.getElementById('pickerVersionTab30').setAttribute('aria-selected', String(version === '3.0'));
  document.getElementById('levelGrid20').style.display = version === '2.0' ? '' : 'none';
  document.getElementById('levelGrid30').style.display = version === '3.0' ? '' : 'none';
  if (version === '3.0') renderHsk30Grid();
}

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
    const pct = cfg.total > 0 ? (known / cfg.total * 100) : 0;
    const shortLabel = 'HSK' + key.replace('hsk30_', '');
    return `
      <button class="level-card ${cfg.available ? '' : 'disabled'}" type="button" data-level="${key}"
        aria-label="${cfg.label}" ${cfg.available ? `onclick="selectLevel('${key}')"` : 'disabled'}>
        <div class="lvl-num">${shortLabel}</div>
        <div class="lvl-label">${cfg.band}</div>
        ${cfg.available
          ? `<div class="lvl-count">${cfg.total} từ</div>
             <div class="lvl-mastery-track"><div class="lvl-mastery-fill" style="width:${pct}%"></div></div>
             <div class="lvl-mastery-text">${known} / ${cfg.total} đã nhớ</div>`
          : `<div class="lvl-soon">Sắp có</div>`}
      </button>`;
  }).join('');
}
