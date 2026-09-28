// Right sidebar: color-coded S/V/O/M sentence breakdown + grammar note.
let grammarStarterData = null;
let grammarStarterDataPromise = null;

function loadGrammarStarterData() {
  if (grammarStarterDataPromise) return grammarStarterDataPromise;
  grammarStarterDataPromise = fetch('database/grammar/starter_sentences.json')
    .then(r => r.json())
    .then(data => { grammarStarterData = data; return data; })
    .catch(() => { grammarStarterData = []; return []; });
  return grammarStarterDataPromise;
}

const GRAMMAR_ROLE_LABELS = { S: 'Chủ ngữ', V: 'Vị ngữ', O: 'Tân ngữ', M: 'Bổ nghĩa' };

function renderGrammarEntry(entry, container) {
  if (!entry) {
    container.innerHTML = '<div class="sidebar-search-empty">Chưa có phân tích ngữ pháp cho từ này.</div>';
    return;
  }
  const rolesHtml = entry.roles.map(r =>
    `<span class="grammar-role grammar-role-${r.type}" title="${GRAMMAR_ROLE_LABELS[r.type] || r.type}">${r.text}</span>`
  ).join('');
  container.innerHTML = `
    <div class="grammar-sentence">${rolesHtml}</div>
    <div class="grammar-note-card">
      <div class="grammar-note-pattern">${entry.grammar_point.pattern}</div>
      <div class="grammar-note-text">${entry.grammar_point.note}</div>
    </div>
  `;
}

function updateGrammarBreakdown(word) {
  const container = document.getElementById('grammarBreakdownBody');
  if (!container) return;
  if (!word) {
    renderGrammarEntry(null, container);
    return;
  }
  if (!grammarStarterData) {
    renderGrammarEntry(null, container);
    loadGrammarStarterData().then(() => {
      const currentWord = typeof activeStudyWord !== 'undefined' ? activeStudyWord : null;
      if (currentWord && currentWord.hanzi === word.hanzi) {
        updateGrammarBreakdown(currentWord);
      }
    });
    return;
  }
  const entry = grammarStarterData.find(e => e.hanzi === word.hanzi);
  renderGrammarEntry(entry, container);
}

function initGrammarBreakdown() {
  const mount = document.getElementById('workstationRight');
  if (!mount) return;
  const wrap = document.createElement('div');
  wrap.className = 'grammar-breakdown-panel';
  wrap.innerHTML = `
    <div class="sidebar-panel-title">Phân tích ngữ pháp</div>
    <div id="grammarBreakdownBody"></div>
  `;
  mount.appendChild(wrap);

  // Register listener first so any early activeStudyWord changes are captured
  onActiveWordChange(updateGrammarBreakdown);

  // Load data, then re-read the CURRENT activeStudyWord (not a stale value)
  // and render it. This ensures we show the correct entry even if
  // setActiveStudyWord() fires before the dataset loads.
  loadGrammarStarterData().then(() => {
    const currentWord = typeof activeStudyWord !== 'undefined' ? activeStudyWord : null;
    updateGrammarBreakdown(currentWord);
  });
}

document.addEventListener('DOMContentLoaded', initGrammarBreakdown);
