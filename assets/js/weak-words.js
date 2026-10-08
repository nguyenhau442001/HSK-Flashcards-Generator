// Left sidebar: starred/weak words list, backed by localStorage.
const WEAK_WORDS_KEY = 'hsk_weak_words_v1';

function loadWeakWords() {
  try {
    const raw = localStorage.getItem(WEAK_WORDS_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (e) { return []; }
}

function saveWeakWords(list) {
  try { localStorage.setItem(WEAK_WORDS_KEY, JSON.stringify(list)); } catch (e) {}
}

function isWeakWord(hanzi) {
  return loadWeakWords().some(w => w.hanzi === hanzi);
}

function toggleWeakWord(hanzi, level) {
  if (!hanzi) return false;
  const list = loadWeakWords();
  const existingIndex = list.findIndex(w => w.hanzi === hanzi);
  if (existingIndex >= 0) {
    list.splice(existingIndex, 1);
  } else {
    list.push({ hanzi, level: level || currentLevel || '' });
  }
  saveWeakWords(list);
  renderWeakWordsList();
  updateWeakWordToggleButton();
  return existingIndex < 0; // true if now starred
}

function updateWeakWordToggleButton() {
  const btn = document.getElementById('weakWordToggleBtn');
  if (!btn || !activeStudyWord) return;
  const starred = isWeakWord(activeStudyWord.hanzi);
  const icon = document.getElementById('weakWordToggleIcon');
  if (icon) {
    icon.innerHTML = starred
      ? `<svg width="15" height="15" viewBox="0 0 24 24" fill="#fbbf24" stroke="#fbbf24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>`
      : `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>`;
    btn.title = starred ? 'Bỏ đánh dấu từ khó' : 'Đánh dấu từ khó';
    btn.setAttribute('aria-label', starred ? 'Bỏ đánh dấu từ khó' : 'Đánh dấu từ khó');
  } else {
    btn.textContent = starred ? '★ Đã đánh dấu' : '☆ Đánh dấu từ khó';
  }
  btn.classList.toggle('active', starred);
}

function renderWeakWordsList() {
  const container = document.getElementById('weakWordsList');
  if (!container) return;
  const list = loadWeakWords();
  if (!list.length) {
    const panel = container.closest('.weak-words-panel');
    if (panel) panel.hidden = true;
    container.innerHTML = '';
    return;
  }
  const panel = container.closest('.weak-words-panel');
  if (panel) panel.hidden = false;
  container.innerHTML = list.map(w => `
    <li class="sidebar-search-result weak-word-item" data-hanzi="${w.hanzi}">
      <span class="ssr-hanzi">${w.hanzi}</span>
      <span class="ssr-level">${w.level}</span>
      <button type="button" class="weak-word-remove" data-remove="${w.hanzi}" aria-label="Bỏ đánh dấu ${w.hanzi}">✕</button>
    </li>
  `).join('');
}

function initWeakWordsPanel() {
  const mount = document.body.classList.contains('is-desktop-dock')
    ? document.getElementById('workstationLeft')
    : document.getElementById('mobileDockDialogBody');
  if (!mount) return;
  const wrap = document.createElement('div');
  wrap.className = 'weak-words-panel';
  wrap.id = 'weakWordsPanel';
  wrap.innerHTML = `
    <div class="sidebar-panel-title">Từ khó (đã đánh dấu)</div>
    <ul class="sidebar-search-results weak-words-list" id="weakWordsList"></ul>
  `;
  mount.appendChild(wrap);
  renderWeakWordsList();

  wrap.addEventListener('click', e => {
    const removeBtn = e.target.closest('[data-remove]');
    if (removeBtn) {
      const list = loadWeakWords().filter(w => w.hanzi !== removeBtn.dataset.remove);
      saveWeakWords(list);
      renderWeakWordsList();
      updateWeakWordToggleButton();
      return;
    }
    const item = e.target.closest('.weak-word-item');
    if (item) setActiveStudyWord({ hanzi: item.dataset.hanzi, pinyin: '', meaning: '' });
  });

  onActiveWordChange(updateWeakWordToggleButton);
}

document.addEventListener('DOMContentLoaded', initWeakWordsPanel);
