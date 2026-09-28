// Left sidebar: compact 214-radicals quick filter grouped by stroke count.
let sidebarRadicalsCache = {}; // key: `${set}_${strokeCount}` -> array of radical entries

function fetchSidebarRadicalStroke(set, strokeCount) {
  const cacheKey = `${set}_${strokeCount}`;
  if (sidebarRadicalsCache[cacheKey]) return Promise.resolve(sidebarRadicalsCache[cacheKey]);
  return fetch(radicalStrokeUrl(set, strokeCount))
    .then(r => r.json())
    .then(list => { sidebarRadicalsCache[cacheKey] = list; return list; })
    .catch(() => []);
}

function renderSidebarRadicalExamples(radical, container) {
  if (!radical.examples || !radical.examples.length) {
    container.innerHTML = '<div class="sidebar-search-empty">Bộ thủ này chưa có ví dụ.</div>';
    return;
  }
  container.innerHTML = radical.examples.map(ex => `
    <li class="sidebar-search-result" data-hanzi="${ex.hanzi}" tabindex="0">
      <span class="ssr-hanzi">${ex.hanzi}</span>
      <span class="ssr-pinyin">${ex.pinyin}</span>
      <span class="ssr-level">${ex.meaning}</span>
    </li>
  `).join('');
}

function initSidebarRadicalsFilter() {
  const mount = document.getElementById('workstationLeft');
  if (!mount) return;
  const wrap = document.createElement('div');
  wrap.className = 'sidebar-radicals-filter';
  const maxStroke = RADICAL_STROKE_COUNTS.kangxi214;
  const chips = Array.from({ length: maxStroke }, (_, i) => i + 1)
    .map(n => `<button type="button" class="sidebar-stroke-chip" data-stroke="${n}">${n}</button>`)
    .join('');
  wrap.innerHTML = `
    <div class="sidebar-panel-title">214 Bộ thủ</div>
    <div class="sidebar-stroke-chips">${chips}</div>
    <ul class="sidebar-search-results sidebar-radicals-grid" id="sidebarRadicalsGrid"></ul>
    <ul class="sidebar-search-results" id="sidebarRadicalExamples" hidden></ul>
  `;
  mount.appendChild(wrap);

  const grid = wrap.querySelector('#sidebarRadicalsGrid');
  const examplesList = wrap.querySelector('#sidebarRadicalExamples');

  wrap.querySelectorAll('.sidebar-stroke-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      wrap.querySelectorAll('.sidebar-stroke-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const n = Number(chip.dataset.stroke);
      fetchSidebarRadicalStroke('kangxi214', n).then(list => {
        grid.hidden = false;
        examplesList.hidden = true;
        grid.innerHTML = list.map(r => `
          <li class="sidebar-search-result" data-radical="${r.radical}" tabindex="0">
            <span class="ssr-hanzi">${r.radical}</span>
            <span class="ssr-pinyin">${r.pinyin}</span>
            <span class="ssr-level">${r.meaning}</span>
          </li>
        `).join('');
        grid.dataset.strokeList = JSON.stringify(list);
      });
    });
  });

  grid.addEventListener('click', e => {
    const li = e.target.closest('.sidebar-search-result[data-radical]');
    if (!li) return;
    const list = JSON.parse(grid.dataset.strokeList || '[]');
    const radical = list.find(r => r.radical === li.dataset.radical);
    if (radical) renderSidebarRadicalExamples(radical, examplesList);
    examplesList.hidden = false;
  });

  examplesList.addEventListener('click', e => {
    const li = e.target.closest('.sidebar-search-result[data-hanzi]');
    if (!li) return;
    setActiveStudyWord({ hanzi: li.dataset.hanzi, pinyin: '', meaning: '' });
  });
}

document.addEventListener('DOMContentLoaded', initSidebarRadicalsFilter);
