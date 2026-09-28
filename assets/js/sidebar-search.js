// Left sidebar: debounced instant search across HSK1-6 (2.0) vocab.
let sidebarSearchIndex = null;
let sidebarSearchIndexPromise = null;

const TONE_MARKS = {
  'ā':'a','á':'a','ǎ':'a','à':'a',
  'ē':'e','é':'e','ě':'e','è':'e',
  'ī':'i','í':'i','ǐ':'i','ì':'i',
  'ō':'o','ó':'o','ǒ':'o','ò':'o',
  'ū':'u','ú':'u','ǔ':'u','ù':'u',
  'ǖ':'v','ǘ':'v','ǚ':'v','ǜ':'v','ü':'v',
};
function stripTones(s) {
  return String(s).toLowerCase().replace(/[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]/g, ch => TONE_MARKS[ch] || ch);
}

function buildSidebarSearchIndex() {
  if (sidebarSearchIndexPromise) return sidebarSearchIndexPromise;
  const levelKeys = hskLevelKeys(); // HSK1-6 (2.0) only, excludes topics + HSK30 by design
  sidebarSearchIndexPromise = Promise.all(
    levelKeys.map(key =>
      fetch(LEVELS[key].dataUrl)
        .then(r => r.json())
        .then(words => words.map(w => ({
          hanzi: w.hanzi,
          pinyin: w.pinyin,
          meaning: w.meaning,
          level: LEVELS[key].label,
          pinyinStripped: stripTones(w.pinyin),
        })))
        .catch(() => [])
    )
  ).then(lists => {
    sidebarSearchIndex = lists.flat();
    return sidebarSearchIndex;
  });
  return sidebarSearchIndexPromise;
}

function searchSidebarIndex(query) {
  if (!sidebarSearchIndex || !query.trim()) return [];
  const q = query.trim().toLowerCase();
  const qStripped = stripTones(query);
  return sidebarSearchIndex
    .filter(w =>
      w.hanzi.includes(query.trim()) ||
      w.pinyinStripped.includes(qStripped) ||
      w.meaning.toLowerCase().includes(q)
    )
    .slice(0, 20);
}

function renderSidebarSearchResults(results, container) {
  if (!results.length) {
    container.innerHTML = '<div class="sidebar-search-empty">Không tìm thấy từ nào.</div>';
    container.hidden = false;
    return;
  }
  container.innerHTML = results.map(w => `
    <li class="sidebar-search-result" data-hanzi="${w.hanzi}" tabindex="0">
      <span class="ssr-hanzi">${w.hanzi}</span>
      <span class="ssr-pinyin">${w.pinyin}</span>
      <span class="ssr-level">${w.level}</span>
    </li>
  `).join('');
  container.hidden = false;
}

let sidebarSearchDebounceTimer = null;
function onSidebarSearchInput(value, resultsEl) {
  clearTimeout(sidebarSearchDebounceTimer);
  sidebarSearchDebounceTimer = setTimeout(() => {
    buildSidebarSearchIndex().then(() => {
      const results = searchSidebarIndex(value);
      if (!value.trim()) { resultsEl.hidden = true; resultsEl.innerHTML = ''; return; }
      renderSidebarSearchResults(results, resultsEl);
    });
  }, 300);
}

function initSidebarSearch() {
  const mount = document.getElementById('workstationLeft');
  if (!mount) return;
  const wrap = document.createElement('div');
  wrap.className = 'sidebar-search';
  wrap.innerHTML = `
    <input type="search" id="sidebarSearchInput" class="sidebar-search-input"
      placeholder="Tìm Hán tự, pinyin, nghĩa..." aria-label="Tìm từ vựng">
    <ul id="sidebarSearchResults" class="sidebar-search-results" hidden></ul>
  `;
  mount.appendChild(wrap);

  const input = wrap.querySelector('#sidebarSearchInput');
  const results = wrap.querySelector('#sidebarSearchResults');

  input.addEventListener('input', () => onSidebarSearchInput(input.value, results));
  results.addEventListener('click', e => {
    const li = e.target.closest('.sidebar-search-result');
    if (!li) return;
    const hanzi = li.dataset.hanzi;
    const word = sidebarSearchIndex.find(w => w.hanzi === hanzi);
    if (word) setActiveStudyWord(word);
    results.hidden = true;
  });
}

document.addEventListener('DOMContentLoaded', initSidebarSearch);
