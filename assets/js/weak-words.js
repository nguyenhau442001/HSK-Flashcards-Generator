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
  btn.textContent = starred ? '★ Đã đánh dấu' : '☆ Đánh dấu từ khó';
  btn.classList.toggle('active', starred);
}

function renderWeakWordsList() {
  const container = document.getElementById('weakWordsList');
  if (!container) return;
  const list = loadWeakWords();
  if (!list.length) {
    container.innerHTML = '<div class="sidebar-search-empty">Chưa có từ nào được đánh dấu.</div>';
    return;
  }
  container.innerHTML = list.map(w => `
    <li class="sidebar-search-result weak-word-item" data-hanzi="${w.hanzi}">
      <span class="ssr-hanzi">${w.hanzi}</span>
      <span class="ssr-level">${w.level}</span>
      <button type="button" class="weak-word-remove" data-remove="${w.hanzi}" aria-label="Bỏ đánh dấu ${w.hanzi}">✕</button>
    </li>
  `).join('');
}

function initWeakWordsPanel() {
  const mount = document.getElementById('workstationLeft');
  if (!mount) return;
  const wrap = document.createElement('div');
  wrap.className = 'weak-words-panel';
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
