/**
 * HSK 4 Reading & Analysis Module (Đọc hiểu & Phân tích ngữ pháp HSK 4)
 * Based on official Hanban/CTI standard mock test materials.
 */

let readingAnalysisData = null;
let readingAnalysisDataPromise = null;
let readingCategory = 'all'; // 'all' | 'sentence_building' | 'sentence_logic' | 'cloze' | 'paragraph'
let readingTestFilter = 'all'; // 'all' | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10
let readingFilteredList = [];
let readingCurrentIndex = 0;
let readingActiveMode = 'breakdown'; // 'breakdown' | 'practice'

// Display Preferences
let readingPrefs = {
  pinyin: true,
  hanviet: true,
  meaning: true,
  highlight: true,
  speechSpeed: 1.0,
  dictationMode: false
};

// Practice State for Current Entry
let practiceBuilderSlots = [];
let practiceBuilderBank = [];
let practiceSolved = false;
let practiceSelectedOption = null;
let practiceFeedback = null;

// Initialize Preferences from localStorage
try {
  const saved = localStorage.getItem('hsk4_reading_prefs');
  if (saved) {
    readingPrefs = Object.assign(readingPrefs, JSON.parse(saved));
  }
} catch (e) {}

function saveReadingPrefs() {
  try {
    localStorage.setItem('hsk4_reading_prefs', JSON.stringify(readingPrefs));
  } catch (e) {}
}

/**
 * Load Reading Analysis dataset
 */
async function ensureReadingAnalysisLoaded() {
  if (readingAnalysisData && readingAnalysisData.length) return readingAnalysisData;
  if (readingAnalysisDataPromise) return readingAnalysisDataPromise;

  readingAnalysisDataPromise = fetch('database/reading/hsk4_reading_analysis.json')
    .then(r => {
      if (!r.ok) throw new Error('Không thể tải cơ sở dữ liệu Đọc hiểu HSK 4.');
      return r.json();
    })
    .then(data => {
      readingAnalysisData = data;
      return data;
    })
    .catch(err => {
      console.error(err);
      readingAnalysisData = [];
      return [];
    });

  return readingAnalysisDataPromise;
}

/**
 * Filter pool according to selected category and test
 */
function updateReadingFilteredList() {
  if (!readingAnalysisData || !readingAnalysisData.length) {
    readingFilteredList = [];
    return;
  }
  readingFilteredList = readingAnalysisData.filter(item => {
    const matchCat = (readingCategory === 'all' || item.category === readingCategory);
    const matchTest = (readingTestFilter === 'all' || item.test_id === readingTestFilter);
    return matchCat && matchTest;
  });
  if (readingCurrentIndex >= readingFilteredList.length) {
    readingCurrentIndex = 0;
  }
}

/**
 * Main entry point when user navigates to Reading Tab
 */
async function startReadingAnalysis() {
  const container = document.getElementById('screenReadingAnalysis');
  if (!container) return;

  container.style.display = '';
  await ensureReadingAnalysisLoaded();
  updateReadingFilteredList();
  renderReadingAnalysisScreen();
}

/**
 * Change Category Filter
 */
function setReadingCategory(cat) {
  readingCategory = cat;
  updateReadingFilteredList();
  readingCurrentIndex = 0;
  resetPracticeState();
  renderReadingAnalysisScreen();
}

/**
 * Change Mock Test Filter ('all' | 1 | 2 | ... | 10)
 */
function setReadingTestFilter(testId) {
  readingTestFilter = testId;
  updateReadingFilteredList();
  readingCurrentIndex = 0;
  resetPracticeState();
  renderReadingAnalysisScreen();
}

/**
 * Switch Active Sub-mode: 'breakdown' | 'practice'
 */
function setReadingActiveMode(mode) {
  readingActiveMode = mode;
  renderReadingAnalysisScreen();
}

/**
 * Jump to next / prev question
 */
function nextReadingQuestion() {
  if (readingCurrentIndex < readingFilteredList.length - 1) {
    readingCurrentIndex++;
    resetPracticeState();
    renderReadingAnalysisScreen();
  }
}

function prevReadingQuestion() {
  if (readingCurrentIndex > 0) {
    readingCurrentIndex--;
    resetPracticeState();
    renderReadingAnalysisScreen();
  }
}

function jumpToReadingIndex(idx) {
  idx = parseInt(idx, 10);
  if (!isNaN(idx) && idx >= 0 && idx < readingFilteredList.length) {
    readingCurrentIndex = idx;
    resetPracticeState();
    renderReadingAnalysisScreen();
  }
}

function resetPracticeState() {
  practiceSolved = false;
  practiceSelectedOption = null;
  practiceFeedback = null;
  const entry = readingFilteredList[readingCurrentIndex];
  if (!entry) return;

  if (entry.practice) {
    if (entry.practice.scrambled_chunks) {
      practiceBuilderBank = entry.practice.scrambled_chunks.slice();
      practiceBuilderSlots = [];
    } else if (entry.practice.scrambled_items) {
      practiceBuilderBank = entry.practice.scrambled_items.slice();
      practiceBuilderSlots = [];
    }
  }
}

/**
 * Toggle Display Elements
 */
function toggleReadingPinyin() {
  readingPrefs.pinyin = !readingPrefs.pinyin;
  saveReadingPrefs();
  renderReadingAnalysisScreen();
}

function toggleReadingHanViet() {
  readingPrefs.hanviet = !readingPrefs.hanviet;
  saveReadingPrefs();
  renderReadingAnalysisScreen();
}

function toggleReadingMeaning() {
  readingPrefs.meaning = !readingPrefs.meaning;
  saveReadingPrefs();
  renderReadingAnalysisScreen();
}

function toggleReadingHighlight() {
  readingPrefs.highlight = !readingPrefs.highlight;
  saveReadingPrefs();
  renderReadingAnalysisScreen();
}

function toggleReadingDictation() {
  readingPrefs.dictationMode = !readingPrefs.dictationMode;
  saveReadingPrefs();
  renderReadingAnalysisScreen();
}

function toggleReadingSpeed() {
  readingPrefs.speechSpeed = readingPrefs.speechSpeed === 1.0 ? 0.75 : 1.0;
  saveReadingPrefs();
  const speedBtn = document.getElementById('readingSpeedBtn');
  if (speedBtn) speedBtn.textContent = `Tốc độ: ${readingPrefs.speechSpeed}x`;
}

/**
 * Audio TTS Playback
 */
function playReadingSentenceAudio(entry) {
  if (!entry || !entry.zh) return;
  const btn = document.getElementById('readingPlayAudioBtn');
  if (typeof speakText === 'function') {
    speakText(entry.zh, btn, readingPrefs.speechSpeed);
  }
}

/**
 * Render the whole Reading & Analysis UI
 */
function renderReadingAnalysisScreen() {
  const container = document.getElementById('screenReadingAnalysis');
  if (!container) return;

  if (!readingFilteredList.length) {
    container.innerHTML = `
      <div class="reading-analysis-container">
        <p style="text-align:center; padding: 40px 0; color: var(--text-secondary);">
          Đang tải dữ liệu Đọc hiểu & Phân tích ngữ pháp HSK 4...
        </p>
      </div>
    `;
    return;
  }

  const currentEntry = readingFilteredList[readingCurrentIndex];

  // Initialize practice items if not already done
  if (practiceBuilderBank.length === 0 && practiceBuilderSlots.length === 0) {
    resetPracticeState();
  }

  container.innerHTML = `
    <div class="reading-analysis-container">
      <!-- HEADER -->
      <header class="reading-header">
        <div class="reading-header-top">
          <div class="reading-title-group">
            <h2 class="reading-title">📖 Đọc hiểu & Phân tích ngữ pháp HSK 4</h2>
            <span class="reading-standard-badge">Chuẩn Hanban / CTI</span>
          </div>
          <div class="reading-header-actions">
            <span class="reading-counter-badge">${readingCurrentIndex + 1} / ${readingFilteredList.length} câu</span>
          </div>
        </div>

        <!-- TEST FILTERS -->
        <div class="reading-test-filters" role="group" aria-label="Lọc theo Đề thi">
          <span class="reading-filter-label">Đề thi:</span>
          <button type="button" class="reading-test-btn ${readingTestFilter === 'all' ? 'active' : ''}" onclick="setReadingTestFilter('all')">
            Tất cả đề
          </button>
          ${[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(t => {
            const countInTest = readingAnalysisData.filter(d => d.test_id === t).length;
            if (countInTest === 0) return '';
            return `
              <button type="button" class="reading-test-btn ${readingTestFilter === t ? 'active' : ''}" onclick="setReadingTestFilter(${t})">
                Đề ${t} (${countInTest})
              </button>
            `;
          }).join('')}
        </div>

        <!-- CATEGORY FILTERS -->
        <div class="reading-category-filters" role="group" aria-label="Lọc theo dạng đề thi">
          <button type="button" class="reading-cat-btn ${readingCategory === 'all' ? 'active' : ''}" onclick="setReadingCategory('all')">
            🌟 Tất cả (${readingAnalysisData.filter(d => readingTestFilter === 'all' || d.test_id === readingTestFilter).length})
          </button>
          <button type="button" class="reading-cat-btn ${readingCategory === 'sentence_building' ? 'active' : ''}" onclick="setReadingCategory('sentence_building')">
            🧩 Xếp câu (${readingAnalysisData.filter(d => d.category === 'sentence_building' && (readingTestFilter === 'all' || d.test_id === readingTestFilter)).length})
          </button>
          <button type="button" class="reading-cat-btn ${readingCategory === 'sentence_logic' ? 'active' : ''}" onclick="setReadingCategory('sentence_logic')">
            🔀 Sắp xếp đoạn A-B-C (${readingAnalysisData.filter(d => d.category === 'sentence_logic' && (readingTestFilter === 'all' || d.test_id === readingTestFilter)).length})
          </button>
          <button type="button" class="reading-cat-btn ${readingCategory === 'cloze' ? 'active' : ''}" onclick="setReadingCategory('cloze')">
            📝 Điền từ ngữ cảnh (${readingAnalysisData.filter(d => d.category === 'cloze' && (readingTestFilter === 'all' || d.test_id === readingTestFilter)).length})
          </button>
          <button type="button" class="reading-cat-btn ${readingCategory === 'paragraph' ? 'active' : ''}" onclick="setReadingCategory('paragraph')">
            📑 Đoạn văn chuyên sâu (${readingAnalysisData.filter(d => d.category === 'paragraph' && (readingTestFilter === 'all' || d.test_id === readingTestFilter)).length})
          </button>
        </div>
      </header>

      <!-- MODE SELECTOR TABS -->
      <nav class="reading-mode-tabs" aria-label="Chế độ học">
        <button type="button" class="reading-mode-tab ${readingActiveMode === 'breakdown' ? 'active' : ''}" onclick="setReadingActiveMode('breakdown')">
          👁️ Phân tích chuyên sâu (Breakdown)
        </button>
        <button type="button" class="reading-mode-tab ${readingActiveMode === 'practice' ? 'active' : ''}" onclick="setReadingActiveMode('practice')">
          🎯 Thực chiến tương tác (Practice)
        </button>
      </nav>

      <!-- MAIN CARD -->
      <section class="reading-main-card" aria-label="Câu đọc hiểu chính">
        <!-- TOP META & DISPLAY CONTROLS -->
        <div class="reading-card-topbar">
          <div class="reading-source-tag">
            <span>📚 ${currentEntry.source || 'HSK 4 Chuẩn'}</span>
            <span class="reading-exam-pill">${currentEntry.exam_part || ''}</span>
          </div>

          <div class="reading-toggles">
            <button type="button" class="reading-toggle-btn ${readingPrefs.pinyin ? 'active' : ''}" onclick="toggleReadingPinyin()" title="Ẩn/Hiện Pinyin">
              Pinyin
            </button>
            <button type="button" class="reading-toggle-btn ${readingPrefs.hanviet ? 'active' : ''}" onclick="toggleReadingHanViet()" title="Ẩn/Hiện Hán - Việt">
              Hán - Việt
            </button>
            <button type="button" class="reading-toggle-btn ${readingPrefs.meaning ? 'active' : ''}" onclick="toggleReadingMeaning()" title="Ẩn/Hiện Nghĩa tiếng Việt">
              Dịch nghĩa
            </button>
            <button type="button" class="reading-toggle-btn ${readingPrefs.highlight ? 'active' : ''}" onclick="toggleReadingHighlight()" title="Ẩn/Hiện Tô màu ngữ pháp">
              Highlight
            </button>
          </div>
        </div>

        <!-- HIGHLIGHT COLOR LEGEND -->
        ${readingPrefs.highlight ? `
          <div class="reading-legend">
            <div class="legend-item"><span class="legend-dot dot-grammar"></span> <span>Ngữ pháp & Điểm bẫy (把, 被, 连...都)</span></div>
            <div class="legend-item"><span class="legend-dot dot-core"></span> <span>Từ vựng cốt lõi HSK 4</span></div>
            <div class="legend-item"><span class="legend-dot dot-advanced"></span> <span>Từ mới / Mở rộng</span></div>
          </div>
        ` : ''}

        <!-- CHINESE PASSAGE WITH TOKENS -->
        <div class="reading-passage-box">
          <div class="reading-zh-line" id="readingZhLine">
            ${readingPrefs.dictationMode ? `
              <span style="font-size:1.1rem; color:var(--text-secondary); font-style:italic;">
                🎧 Chế độ chép chính tả đang bật. Hãy nghe phát âm và gõ vào ô bên dưới!
              </span>
            ` : renderTokensHtml(currentEntry)}
          </div>
        </div>

        <!-- TRANSLATIONS BOX -->
        ${!readingPrefs.dictationMode && (readingPrefs.pinyin || readingPrefs.hanviet || readingPrefs.meaning) ? `
          <div class="reading-translations-box">
            ${readingPrefs.pinyin ? `<div class="reading-full-py"><strong>Pinyin:</strong> ${currentEntry.pinyin || ''}</div>` : ''}
            ${readingPrefs.hanviet ? `<div class="reading-full-hv"><strong>Hán - Việt:</strong> ［${currentEntry.hanviet || ''}］</div>` : ''}
            ${readingPrefs.meaning ? `<div class="reading-full-vi"><strong>Dịch nghĩa:</strong> ${currentEntry.vietnamese || ''}</div>` : ''}
          </div>
        ` : ''}

        <!-- AUDIO & DICTATION TOOLBAR -->
        <div class="reading-audio-bar">
          <div class="reading-audio-main">
            <button type="button" class="reading-audio-btn" id="readingPlayAudioBtn" onclick="playReadingSentenceAudio(readingFilteredList[readingCurrentIndex])" aria-label="Nghe đọc câu">
              🔊 Phát âm câu
            </button>
            <button type="button" class="reading-speed-btn" id="readingSpeedBtn" onclick="toggleReadingSpeed()">
              Tốc độ: ${readingPrefs.speechSpeed}x
            </button>
          </div>

          <button type="button" class="reading-dictation-btn ${readingPrefs.dictationMode ? 'active' : ''}" onclick="toggleReadingDictation()">
            ✍️ Chép chính tả (Dictation)
          </button>
        </div>

        <!-- DICTATION INPUT BOX -->
        ${readingPrefs.dictationMode ? `
          <div class="reading-dictation-box">
            <div class="dictation-input-row">
              <input type="text" id="dictationInput" class="dictation-input" placeholder="Gõ chữ Hán hoặc Pinyin nghe được..." autocomplete="off">
              <button type="button" class="dictation-check-btn" onclick="checkDictationAnswer()">Kiểm tra</button>
            </div>
            <div class="dictation-feedback" id="dictationFeedback"></div>
          </div>
        ` : ''}

        <!-- TOKEN INSPECTOR DRAWER -->
        <div id="readingTokenInspector" style="display:none;"></div>
      </section>

      <!-- CONTENT PANELS BASED ON ACTIVE MODE -->
      ${readingActiveMode === 'breakdown' ? renderBreakdownPanelsHtml(currentEntry) : renderPracticePanelsHtml(currentEntry)}

      <!-- BOTTOM NAVIGATION -->
      <footer class="reading-navigation-footer">
        <button type="button" class="reading-nav-btn" onclick="prevReadingQuestion()" ${readingCurrentIndex === 0 ? 'disabled' : ''}>
          ← Câu trước
        </button>

        <select class="reading-jump-select" aria-label="Chọn nhanh câu hỏi" onchange="jumpToReadingIndex(this.value)">
          ${readingFilteredList.map((item, idx) => `
            <option value="${idx}" ${idx === readingCurrentIndex ? 'selected' : ''}>
              ${idx + 1}. [${getCategoryLabel(item.category)}] ${item.title || item.zh.substring(0, 16) + '...'}
            </option>
          `).join('')}
        </select>

        <button type="button" class="reading-nav-btn" onclick="nextReadingQuestion()" ${readingCurrentIndex === readingFilteredList.length - 1 ? 'disabled' : ''}>
          Câu tiếp theo →
        </button>
      </footer>
    </div>
  `;
}

function getCategoryLabel(cat) {
  switch (cat) {
    case 'sentence_building': return 'Xếp câu';
    case 'sentence_logic': return 'Logic A-B-C';
    case 'cloze': return 'Điền từ';
    case 'paragraph': return 'Đoạn văn';
    default: return 'Đọc hiểu';
  }
}

/**
 * Render Tokens into Interactive Highlighted Chips
 */
function renderTokensHtml(entry) {
  if (!entry || !entry.tokens) return entry.zh || '';

  return entry.tokens.map((tok, i) => {
    let highlightClass = '';
    if (readingPrefs.highlight) {
      if (tok.type === 'grammar') highlightClass = 'token-grammar';
      else if (tok.type === 'core') highlightClass = 'token-core';
      else if (tok.type === 'advanced') highlightClass = 'token-advanced';
    }

    return `
      <span class="reading-token ${highlightClass}" data-token-idx="${i}" onclick="inspectToken(${i})" title="Nhấn để xem chi tiết từ này">
        ${readingPrefs.pinyin ? `<span class="reading-token-py">${tok.pinyin || ''}</span>` : ''}
        <span class="reading-token-zh">${tok.text}</span>
        ${readingPrefs.hanviet ? `<span class="reading-token-hv">${tok.hanviet || ''}</span>` : ''}
      </span>
    `;
  }).join('');
}

/**
 * Inspect a Specific Token
 */
function inspectToken(tokenIdx) {
  const entry = readingFilteredList[readingCurrentIndex];
  if (!entry || !entry.tokens || !entry.tokens[tokenIdx]) return;
  const tok = entry.tokens[tokenIdx];

  // Highlight active token
  document.querySelectorAll('.reading-token').forEach((el, i) => {
    el.classList.toggle('active-inspect', i === tokenIdx);
  });

  const inspector = document.getElementById('readingTokenInspector');
  if (!inspector) return;

  let tagLabel = 'Từ cơ bản';
  let tagColor = 'var(--surface-subtle)';
  if (tok.type === 'grammar') {
    tagLabel = '⚡ Điểm ngữ pháp / Bẫy';
    tagColor = 'rgba(139, 92, 246, 0.15)';
  } else if (tok.type === 'core') {
    tagLabel = '📗 Từ cốt lõi HSK 4';
    tagColor = 'rgba(16, 185, 129, 0.15)';
  } else if (tok.type === 'advanced') {
    tagLabel = '📙 Từ mới / Nâng cao';
    tagColor = 'rgba(245, 158, 11, 0.15)';
  }

  inspector.style.display = 'flex';
  inspector.className = 'reading-token-inspector';
  inspector.innerHTML = `
    <div class="inspector-word-group">
      <span class="inspector-zh">${tok.text}</span>
      <span class="inspector-py">${tok.pinyin || ''}</span>
      <span class="inspector-hv">［${tok.hanviet || ''}］</span>
      <span class="inspector-meaning">👉 ${tok.meaning || 'Từ vựng trong câu'}</span>
    </div>
    <div class="inspector-tags">
      <span class="inspector-tag" style="background:${tagColor}">${tagLabel}</span>
      <span class="inspector-tag" style="background:var(--surface-chip)">Vai trò: ${tok.role || 'Từ loại'}</span>
      <button type="button" class="reading-audio-btn" style="padding:4px 8px; font-size:0.78rem;" onclick="speakToken('${tok.text}')">🔊</button>
      <button type="button" class="reading-toggle-btn" onclick="closeInspector()">✕</button>
    </div>
  `;
}

function speakToken(word) {
  if (typeof speakText === 'function') {
    speakText(word, null, 0.85);
  }
}

function closeInspector() {
  const inspector = document.getElementById('readingTokenInspector');
  if (inspector) inspector.style.display = 'none';
  document.querySelectorAll('.reading-token').forEach(el => el.classList.remove('active-inspect'));
}

/**
 * Render Grammar & SVO Breakdown Panels
 */
function renderBreakdownPanelsHtml(entry) {
  const gp = entry.grammar_point || {};
  const breakdown = entry.breakdown || [];

  return `
    <div class="reading-analysis-panels">
      <!-- GRAMMAR TRAP & PATTERN CARD -->
      <div class="grammar-trap-card">
        <div class="grammar-trap-header">
          <div class="grammar-trap-title">
            <span>⚡ ${gp.name || 'Phân tích ngữ pháp trọng tâm'}</span>
          </div>
          <span class="reading-exam-pill">${gp.level || 'HSK 4'}</span>
        </div>

        ${gp.pattern ? `<div class="grammar-trap-pattern">Cấu trúc: ${gp.pattern}</div>` : ''}

        ${gp.trap_note ? `
          <div class="grammar-trap-note">
            <strong>⚠️ Mẹo phòng bẫy thi HSK 4:</strong> ${gp.trap_note}
          </div>
        ` : ''}

        ${gp.explanation ? `
          <div class="grammar-explanation-text">
            <strong>💡 Phân tích chi tiết:</strong> ${gp.explanation}
          </div>
        ` : ''}
      </div>

      <!-- SVO / COMPONENT BREAKDOWN TABLE -->
      ${breakdown.length > 0 ? `
        <div class="sentence-breakdown-card">
          <div class="breakdown-card-title">
            <span>🔬 Phân tách thành phần cấu trúc câu (Word Order Breakdown)</span>
          </div>
          <div class="breakdown-table-wrapper">
            <table class="breakdown-table">
              <thead>
                <tr>
                  <th style="width: 140px;">Thành phần ngữ pháp</th>
                  <th style="width: 180px;">Từ ngữ trong câu</th>
                  <th>Chức năng & Ý nghĩa ngữ pháp</th>
                </tr>
              </thead>
              <tbody>
                ${breakdown.map(b => `
                  <tr>
                    <td><span class="breakdown-role-badge role-${b.type || 'subject'}">${b.role}</span></td>
                    <td><span class="breakdown-text">${b.text}</span></td>
                    <td><span class="breakdown-desc">${b.desc || ''}</span></td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      ` : ''}
    </div>
  `;
}

function renderPracticeFeedbackHtml() {
  if (!practiceFeedback) return '<div id="practiceResultFeedback"></div>';
  return `
    <div id="practiceResultFeedback">
      <div class="practice-result-banner ${practiceFeedback.type}">
        ${practiceFeedback.html}
      </div>
    </div>
  `;
}

/**
 * Render Practice Interactive Modes (Dạng 1: Xếp câu, Dạng 2: Điền khuyết, Dạng 3: Sắp xếp logic)
 */
function renderPracticePanelsHtml(entry) {
  const p = entry.practice || {};

  // Self-heal practice state if empty or mismatched
  if (p.type === 'sentence_building') {
    if ((practiceBuilderBank.length === 0 && practiceBuilderSlots.length === 0 && p.scrambled_chunks) ||
        practiceBuilderBank.some(x => typeof x !== 'string') ||
        practiceBuilderSlots.some(x => typeof x !== 'string')) {
      resetPracticeState();
    }
  } else if (p.type === 'sentence_logic') {
    if ((practiceBuilderBank.length === 0 && practiceBuilderSlots.length === 0 && p.scrambled_items) ||
        practiceBuilderBank.some(x => !x || typeof x !== 'object') ||
        practiceBuilderSlots.some(x => !x || typeof x !== 'object')) {
      resetPracticeState();
    }
  }

  // Case 1: Sentence Building (Xếp câu)
  if (p.type === 'sentence_building') {
    return `
      <div class="reading-practice-card">
        <div class="practice-header">
          <div class="practice-title">🧩 Dạng 1: Sắp xếp các khối từ thành câu hoàn chỉnh</div>
          <div class="practice-hint-text">Bấm vào khối từ để chuyển lên / xuống</div>
        </div>

        <!-- Target Slots -->
        <div class="practice-slots-area ${practiceSolved ? 'is-correct' : ''}" id="practiceSlotsArea">
          ${practiceBuilderSlots.length === 0 ? `
            <span class="practice-empty-placeholder">Bấm chọn các khối từ bên dưới theo trật tự câu đúng...</span>
          ` : practiceBuilderSlots.map((chunk, i) => `
            <button type="button" class="builder-tile slot-tile" onclick="removeFromSlots(${i})">
              ${chunk}
            </button>
          `).join('')}
        </div>

        <!-- Available Bank -->
        <div class="practice-bank-area" id="practiceBankArea">
          ${practiceBuilderBank.map((chunk, i) => `
            <button type="button" class="builder-tile" onclick="moveToSlots(${i})">
              ${chunk}
            </button>
          `).join('')}
        </div>

        <!-- Practice Actions -->
        <div class="practice-actions-bar">
          <div class="practice-btn-group">
            <button type="button" class="practice-action-btn practice-btn-secondary" onclick="resetPracticeState(); renderReadingAnalysisScreen();">
              ↺ Làm lại
            </button>
            <button type="button" class="practice-action-btn practice-btn-secondary" onclick="hintPracticeBuilder()">
              💡 Gợi ý
            </button>
          </div>

          <button type="button" class="practice-action-btn practice-btn-primary" onclick="checkPracticeBuilder()">
            Kiểm tra đáp án
          </button>
        </div>

        ${renderPracticeFeedbackHtml()}
      </div>
    `;
  }

  // Case 2: Cloze Test (Điền khuyết)
  if (p.type === 'cloze') {
    return `
      <div class="reading-practice-card">
        <div class="practice-header">
          <div class="practice-title">📝 Dạng 2: Bài tập Điền khuyết (Cloze Test) theo ngữ cảnh</div>
          <div class="practice-hint-text">Chọn từ thích hợp nhất để điền vào chỗ trống</div>
        </div>

        <div class="cloze-blank-text">
          ${(p.blank_sentence || '').replace('（ ____ ）', `<span class="cloze-blank-spot">${practiceSelectedOption || '？'}</span>`)}
        </div>

        <div class="cloze-options-grid">
          ${(p.options || []).map(opt => {
            let optClass = '';
            if (practiceSelectedOption) {
              if (opt.word === p.target_word) optClass = 'selected-correct';
              else if (opt.word === practiceSelectedOption) optClass = 'selected-wrong';
            }
            return `
              <button type="button" class="cloze-option-btn ${optClass}" onclick="selectClozeOption('${opt.word}')" ${practiceSelectedOption ? 'disabled' : ''}>
                <div>
                  <div class="cloze-opt-zh">${opt.word}</div>
                  <div class="cloze-opt-sub">${opt.pinyin} · ［${opt.hanviet}］</div>
                </div>
                <div class="cloze-opt-sub">${opt.meaning}</div>
              </button>
            `;
          }).join('')}
        </div>

        ${p.clue ? `
          <div style="font-size:0.86rem; color:var(--text-secondary); margin-bottom:12px;">
            💡 <strong>Gợi ý ngữ cảnh:</strong> ${p.clue}
          </div>
        ` : ''}

        ${renderPracticeFeedbackHtml()}
      </div>
    `;
  }

  // Case 3: Sentence Logic (Sắp xếp A-B-C)
  if (p.type === 'sentence_logic') {
    return `
      <div class="reading-practice-card">
        <div class="practice-header">
          <div class="practice-title">🔀 Dạng 3: Sắp xếp thứ tự logic đoạn văn (A - B - C)</div>
          <div class="practice-hint-text">Chọn thứ tự các câu để tạo thành đoạn văn logic</div>
        </div>

        <!-- Target Slots -->
        <div class="practice-slots-area ${practiceSolved ? 'is-correct' : ''}" id="practiceSlotsArea">
          ${practiceBuilderSlots.length === 0 ? `
            <span class="practice-empty-placeholder">Bấm chọn các vế câu A, B, C theo thứ tự đúng...</span>
          ` : practiceBuilderSlots.map((item, i) => `
            <button type="button" class="builder-tile slot-tile" style="text-align:left; font-size:0.95rem; width:100%;" onclick="removeFromSlots(${i})">
              <strong>${item.key}.</strong> ${item.text}
            </button>
          `).join('')}
        </div>

        <!-- Available Bank -->
        <div class="practice-bank-area" style="flex-direction:column; align-items:stretch;" id="practiceBankArea">
          ${practiceBuilderBank.map((item, i) => `
            <button type="button" class="builder-tile" style="text-align:left; font-size:0.95rem; justify-content:flex-start;" onclick="moveToSlots(${i})">
              <strong>${item.key}.</strong> ${item.text}
            </button>
          `).join('')}
        </div>

        <!-- Practice Actions -->
        <div class="practice-actions-bar">
          <div class="practice-btn-group">
            <button type="button" class="practice-action-btn practice-btn-secondary" onclick="resetPracticeState(); renderReadingAnalysisScreen();">
              ↺ Làm lại
            </button>
          </div>

          <button type="button" class="practice-action-btn practice-btn-primary" onclick="checkPracticeLogicOrder()">
            Kiểm tra thứ tự
          </button>
        </div>

        ${renderPracticeFeedbackHtml()}
      </div>
    `;
  }

  return `
    <div class="reading-practice-card">
      <div class="practice-title">📖 Đoạn văn chuyên sâu</div>
      <p style="color:var(--text-secondary); line-height:1.6; margin-top:10px;">
        Đoạn văn này được thiết kế để luyện đọc hiểu toàn diện và phân tích ngữ pháp sống. 
        Hãy chuyển sang tab <strong>"Phân tích chuyên sâu"</strong> để xem phân rã thành phần và bẫy đề thi.
      </p>
    </div>
  `;
}

/**
 * Builder Interactions
 */
function moveToSlots(bankIndex) {
  if (bankIndex >= 0 && bankIndex < practiceBuilderBank.length) {
    const item = practiceBuilderBank.splice(bankIndex, 1)[0];
    practiceBuilderSlots.push(item);
    practiceFeedback = null;
    renderReadingAnalysisScreen();
  }
}

function removeFromSlots(slotIndex) {
  if (slotIndex >= 0 && slotIndex < practiceBuilderSlots.length) {
    const item = practiceBuilderSlots.splice(slotIndex, 1)[0];
    practiceBuilderBank.push(item);
    practiceFeedback = null;
    renderReadingAnalysisScreen();
  }
}

function hintPracticeBuilder() {
  const entry = readingFilteredList[readingCurrentIndex];
  if (!entry || !entry.practice || !entry.practice.target_chunks) return;

  const target = entry.practice.target_chunks;
  const nextTargetWord = target[practiceBuilderSlots.length];
  if (!nextTargetWord) return;

  const foundIdx = practiceBuilderBank.findIndex(c => c === nextTargetWord);
  if (foundIdx !== -1) {
    moveToSlots(foundIdx);
  }
}

function checkPracticeBuilder() {
  const entry = readingFilteredList[readingCurrentIndex];
  if (!entry || !entry.practice || !entry.practice.target_chunks) return;

  const userSentence = practiceBuilderSlots.join('');
  const targetSentence = entry.practice.target_chunks.join('');

  if (userSentence === targetSentence) {
    practiceSolved = true;
    practiceFeedback = {
      type: 'success',
      html: `<span>🎉 <strong>Chính xác xuất sắc!</strong> Trật tự câu hoàn toàn chuẩn ngữ pháp tiếng Trung.</span>`
    };
    playReadingSentenceAudio(entry);
    renderReadingAnalysisScreen();
  } else {
    practiceSolved = false;
    practiceFeedback = {
      type: 'error',
      html: `<span>❌ <strong>Chưa đúng thứ tự:</strong> Hãy chú ý vị trí của từ chỉ thời gian, trạng ngữ, hoặc cấu trúc ngữ pháp (把/被).</span>`
    };
    renderReadingAnalysisScreen();
    const slotsArea = document.getElementById('practiceSlotsArea');
    if (slotsArea) {
      slotsArea.classList.add('is-wrong');
      setTimeout(() => slotsArea.classList.remove('is-wrong'), 400);
    }
  }
}

function checkPracticeLogicOrder() {
  const entry = readingFilteredList[readingCurrentIndex];
  if (!entry || !entry.practice || !entry.practice.correct_order) return;

  const userOrder = practiceBuilderSlots.map(item => item.key).join('');
  const targetOrder = entry.practice.correct_order;

  if (userOrder === targetOrder) {
    practiceSolved = true;
    practiceFeedback = {
      type: 'success',
      html: `
        <div>
          <div>🎉 <strong>Chính xác! Thứ tự chuẩn: ${targetOrder}</strong></div>
          <div style="font-size:0.86rem; margin-top:4px;">${entry.practice.explanation || ''}</div>
        </div>
      `
    };
    playReadingSentenceAudio(entry);
    renderReadingAnalysisScreen();
  } else {
    practiceSolved = false;
    practiceFeedback = {
      type: 'error',
      html: `<span>❌ Thứ tự hiện tại chưa đúng logic phát triển của đoạn văn. Hãy kiểm tra các liên từ nối!</span>`
    };
    renderReadingAnalysisScreen();
    const slotsArea = document.getElementById('practiceSlotsArea');
    if (slotsArea) {
      slotsArea.classList.add('is-wrong');
      setTimeout(() => slotsArea.classList.remove('is-wrong'), 400);
    }
  }
}

function selectClozeOption(word) {
  const entry = readingFilteredList[readingCurrentIndex];
  if (!entry || !entry.practice) return;

  practiceSelectedOption = word;
  const isCorrect = word === entry.practice.target_word;
  const p = entry.practice;

  if (isCorrect) {
    practiceSolved = true;
    practiceFeedback = {
      type: 'success',
      html: `
        <div>
          <div>🎉 <strong>Chính xác!</strong> Từ cần điền là <strong>${word}</strong>.</div>
          <div style="font-size:0.85rem; margin-top:4px;">${entry.grammar_point ? entry.grammar_point.trap_note : ''}</div>
        </div>
      `
    };
    playReadingSentenceAudio(entry);
  } else {
    practiceSolved = false;
    practiceFeedback = {
      type: 'error',
      html: `
        <div>
          <div>❌ Chưa chính xác. Đáp án đúng là <strong>${p.target_word}</strong>.</div>
          <div style="font-size:0.85rem; margin-top:4px;">${entry.grammar_point ? entry.grammar_point.trap_note : ''}</div>
        </div>
      `
    };
  }
  renderReadingAnalysisScreen();
}

/**
 * Dictation Check
 */
function checkDictationAnswer() {
  const entry = readingFilteredList[readingCurrentIndex];
  const input = document.getElementById('dictationInput');
  const feedback = document.getElementById('dictationFeedback');
  if (!entry || !input || !feedback) return;

  const val = input.value.trim().replace(/[，。？！\s]/g, '');
  const targetZh = entry.zh.replace(/[，。？！\s]/g, '');

  if (val === targetZh) {
    feedback.style.color = '#10b981';
    feedback.innerHTML = `🎉 <strong>Tuyệt vời!</strong> Bạn đã chép chính xác 100%: <em>${entry.zh}</em>`;
  } else {
    feedback.style.color = 'var(--text-primary)';
    feedback.innerHTML = `
      <div>Đáp án câu gốc: <strong style="color:var(--accent); font-size:1.1rem;">${entry.zh}</strong></div>
      <div style="font-size:0.84rem; color:var(--text-secondary); margin-top:2px;">(Pinyin: ${entry.pinyin})</div>
    `;
  }
}

// Global Exports
window.startReadingAnalysis = startReadingAnalysis;
window.setReadingCategory = setReadingCategory;
window.setReadingTestFilter = setReadingTestFilter;
window.setReadingActiveMode = setReadingActiveMode;
window.nextReadingQuestion = nextReadingQuestion;
window.prevReadingQuestion = prevReadingQuestion;
window.jumpToReadingIndex = jumpToReadingIndex;
window.toggleReadingPinyin = toggleReadingPinyin;
window.toggleReadingHanViet = toggleReadingHanViet;
window.toggleReadingMeaning = toggleReadingMeaning;
window.toggleReadingHighlight = toggleReadingHighlight;
window.toggleReadingDictation = toggleReadingDictation;
window.toggleReadingSpeed = toggleReadingSpeed;
window.playReadingSentenceAudio = playReadingSentenceAudio;
window.inspectToken = inspectToken;
window.closeInspector = closeInspector;
window.speakToken = speakToken;
window.moveToSlots = moveToSlots;
window.removeFromSlots = removeFromSlots;
window.hintPracticeBuilder = hintPracticeBuilder;
window.checkPracticeBuilder = checkPracticeBuilder;
window.checkPracticeLogicOrder = checkPracticeLogicOrder;
window.selectClozeOption = selectClozeOption;
window.checkDictationAnswer = checkDictationAnswer;
window.resetPracticeState = resetPracticeState;
