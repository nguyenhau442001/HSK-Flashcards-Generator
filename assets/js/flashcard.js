// Flashcard markup, filtering, statistics, and rendering.
function buildCardArea() {
  document.getElementById('cardArea').innerHTML = `
    <div class="progress-bar-track">
      <div class="progress-bar-fill" id="progressBar"></div>
    </div>
    <div class="card" id="card">
      <div class="swipe-badge swipe-badge--known" id="swipeBadgeKnown">✓ Đã nhớ</div>
      <div class="swipe-badge swipe-badge--unknown" id="swipeBadgeUnknown">✗ Chưa nhớ</div>
      <div class="card-toolbar card-interactive" id="cardToolbar" onclick="event.stopPropagation()">
        <button type="button" class="card-tool-btn" id="randomWordBtn" onclick="jumpToRandomWord()" aria-label="Hiện từ ngẫu nhiên (R)" title="Hiện từ ngẫu nhiên (R)">
          <span aria-hidden="true">🎲</span>
        </button>
        <button type="button" class="card-tool-btn" id="shuffleBtn" onclick="shuffleDeck()" aria-label="Xáo trộn bộ từ" title="Xáo trộn bộ từ">
          <span aria-hidden="true">🔀</span>
        </button>
        <button type="button" class="card-tool-btn" id="pinyinToggle" onclick="togglePinyin()" aria-label="Ẩn hoặc hiện pinyin" title="Ẩn hoặc hiện pinyin">
          <span id="pinyinToggleIcon" aria-hidden="true">👁</span>
        </button>
        <button type="button" class="card-tool-btn" id="weakWordToggleBtn" onclick="toggleWeakWord(activeStudyWord && activeStudyWord.hanzi, currentLevel)" aria-label="Đánh dấu từ khó" title="Đánh dấu từ khó">
          <span id="weakWordToggleIcon" aria-hidden="true">☆</span>
        </button>
        <button type="button" class="card-tool-btn" id="transferToggle" onclick="toggleTransferPanel()" aria-label="Sao lưu tiến trình" title="Sao lưu tiến trình" aria-controls="transferPanel" aria-expanded="false">
          <span aria-hidden="true">💾</span>
        </button>
      </div>
      <div id="cardContent" class="card-content">
        <div class="hanzi" id="hanzi"></div>
        <div class="pinyin-row">
          <div class="pinyin" id="pinyin"></div>
          <button class="sound-btn speech-btn" id="soundBtn" type="button"
            onclick="event.stopPropagation(); speakWord()"
            aria-label="Nghe phát âm" aria-live="polite">
            <span class="sound-btn-icon" aria-hidden="true">🔊</span>
          </button>
        </div>
        <div class="meaning" id="meaning"></div>
        <div class="example-box" id="exampleBox">
          <div class="ex-label">Ví dụ</div>
          <div class="ex-zh-row">
            <div class="ex-line ex-zh" id="exZh"></div>
            <div class="example-audio-controls card-interactive">
              <button class="example-sound-btn speech-btn" id="exampleSoundBtn" type="button"
                onclick="event.stopPropagation(); speakExample()"
                aria-label="Nghe câu ví dụ" aria-live="polite">
                <span class="sound-btn-icon" aria-hidden="true">🔊</span>
              </button>
              <details class="example-speed-picker" id="exampleSpeedPicker"
                onclick="event.stopPropagation()">
                <summary aria-label="Tốc độ đọc câu ví dụ: ${formatExampleSpeechSpeed(exampleSpeechSpeed)}">
                  <span class="example-speed-label">Tốc độ đọc</span>
                  <span class="example-current-speed" id="exampleCurrentSpeed">${formatExampleSpeechSpeed(exampleSpeechSpeed)}</span>
                </summary>
                <div class="example-speed-options" role="group" aria-label="Chọn tốc độ đọc câu ví dụ">
                  ${EXAMPLE_SPEECH_SPEEDS.map(speed => `
                    <button class="example-speed-option${speed === exampleSpeechSpeed ? ' selected' : ''}"
                      type="button" data-speed="${speed}"
                      aria-pressed="${speed === exampleSpeechSpeed}"
                      onclick="event.preventDefault(); setExampleSpeechSpeed(this.dataset.speed)">
                      ${formatExampleSpeechSpeed(speed)}
                    </button>
                  `).join('')}
                </div>
              </details>
            </div>
          </div>
          <div class="ex-line ex-py" id="exPy"></div>
          <div class="ex-line ex-vi" id="exVi"></div>
        </div>
        <div class="hint" id="hint">Nhấn vào thẻ để xem nghĩa và ví dụ</div>
      </div>
    </div>

    <div class="nav-row nav-row--progress-only">
      <span class="progress-text" id="progress">1 / ${WORDS.length}</span>
    </div>

    <div class="rating-area">
      ${revealButtonHtml('flip()', 'revealBtn')}
      <div class="rating-row" id="ratingRow" hidden>
        ${ratingButtonsHtml('rateCurrentCard', 'preview-')}
      </div>
    </div>

    <div class="action-row secondary-actions">
      <button class="show-unknown-btn" id="unknownWordsToggle" onclick="toggleUnknownWords()"
        aria-controls="unknownWordsList" aria-expanded="false">
        Hiển thị từ chưa nhớ
      </button>
      <button class="reset-progress-btn" type="button" onclick="resetProgress()">↻ Học lại từ đầu</button>
    </div>
    <div id="dailyNewLimitMessage" class="daily-new-limit-message" role="status"></div>
    <div class="unknown-words-list" id="unknownWordsList"></div>
  `;
  const pinyinBtn = document.getElementById('pinyinToggle');
  const pinyinIcon = document.getElementById('pinyinToggleIcon');
  if (pinyinIcon) {
    pinyinIcon.textContent = showPinyin ? '👁' : '🙈';
    pinyinBtn.title = showPinyin ? 'Ẩn pinyin' : 'Hiện pinyin';
    pinyinBtn.setAttribute('aria-label', showPinyin ? 'Ẩn pinyin' : 'Hiện pinyin');
  } else if (pinyinBtn) {
    pinyinBtn.textContent = showPinyin ? '👁 Đang hiện pinyin' : '🙈 Chế độ thử thách: ẩn pinyin';
  }
  if (pinyinBtn) pinyinBtn.classList.toggle('on', !showPinyin);
  if (typeof updateWeakWordToggleButton === 'function') updateWeakWordToggleButton();
  initSwipe();
}

function renderFilters() {
  const row = document.getElementById('filterRow');
  if (!row) return;
  row.innerHTML = '';
  const known = Object.values(progress).filter(value => value === 'known').length;
  const unknown = Object.values(progress).filter(value => value === 'unknown').length;
  const counts = {
    all: WORDS.length,
    unknown,
    known,
    unseen: Math.max(0, WORDS.length - known - unknown),
  };
  const filters = [
    { key: 'all', label: 'Tất cả', count: counts.all },
    { key: 'unknown', label: 'Chưa nhớ', count: counts.unknown, modifier: 'unknown' },
    { key: 'known', label: 'Đã nhớ', count: counts.known, modifier: 'known' },
    { key: 'unseen', label: 'Chưa học', count: counts.unseen, modifier: 'unseen' },
  ];
  filters.forEach(f => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'filter-btn' + (f.modifier ? ' filter-btn--' + f.modifier : '') + (currentFilter === f.key ? ' active' : '');
    b.innerHTML = `<span class="filter-label">${f.label}</span> <span class="filter-count">(${f.count})</span>`;
    b.onclick = () => setFilter(f.key);
    row.appendChild(b);
  });
}
function setFilter(key) {
  currentFilter = key;
  if (key === 'all') filteredOrder = order.slice();
  else if (key === 'unseen') filteredOrder = order.filter(i => !progress[WORDS[i].id]);
  else filteredOrder = order.filter(i => progress[WORDS[i].id] === key);
  idx = 0;
  renderFilters();
  renderStudyWordList();
  render('fade');
}
function updateStats() {
  let known = 0, unknown = 0;
  Object.values(progress).forEach(v => { if (v === 'known') known++; else if (v === 'unknown') unknown++; });
  const sTotal = document.getElementById('s-total');
  if (sTotal) sTotal.textContent = WORDS.length;
  const sKnown = document.getElementById('s-known');
  if (sKnown) sKnown.textContent = known;
  const sUnknown = document.getElementById('s-unknown');
  if (sUnknown) sUnknown.textContent = unknown;
  const sUnseen = document.getElementById('s-unseen');
  if (sUnseen) sUnseen.textContent = Math.max(0, WORDS.length - known - unknown);
  renderFilters();
}
const RATING_BUTTONS = [
  { rating: 'again', emoji: '❌', label: 'Chưa nhớ', key: '1', interval: 'Hôm nay' },
  { rating: 'good', emoji: '✅', label: 'Đã nhớ', key: '2', interval: 'Ôn ngắt quãng' },
];
const RATING_KEYS = {
  '1': 'again',
  '2': 'good',
  'ArrowLeft': 'again',
  'ArrowRight': 'good',
};

// Shared by the level deck and "Ôn hôm nay": label on top, repeat() interval below.
function ratingButtonsHtml(handlerName, previewIdPrefix, previews) {
  return RATING_BUTTONS.map(button => {
    const preview = previews ? previews[button.rating] : null;
    const intervalText = preview ? formatSrsInterval(preview, button.interval) : button.interval;
    return `
    <button type="button" class="rating-btn rating-btn--${button.rating}"
      onclick="${handlerName}('${button.rating}')" aria-keyshortcuts="${button.key}">
      <span class="rating-emoji" aria-hidden="true">${button.emoji}</span>
      <span class="rating-label">${button.label}</span>
      <span class="rating-interval"${previewIdPrefix ? ` id="${previewIdPrefix}${button.rating}"` : ''}>${intervalText}</span>
    </button>`;
  }).join('');
}
function revealButtonHtml(onclick, id) {
  return `<button type="button" class="reveal-btn" id="${id}" onclick="${onclick}" aria-keyshortcuts="Space">
      <span>Lật thẻ</span><kbd class="key-badge" aria-hidden="true">Space</kbd>
    </button>`;
}
function formatSrsInterval(preview, fallback) {
  if (preview && preview.intervalText) return preview.intervalText;
  if (!preview) return fallback || '';
  if (preview.rating === 'again') return 'Hôm nay';
  const ms = preview.intervalMs;
  if (!Number.isFinite(ms)) return fallback || '';
  const days = Math.round(ms / 86400000);
  if (days <= 0) return 'Hôm nay';
  if (days === 1) return '1 ngày';
  return days + ' ngày';
}
function updateSrsPreviews(word) {
  const card = word && srsCards[word.id];
  const previews = card ? SRS.preview(card, new Date(), srsRetention) : {};
  RATING_BUTTONS.forEach(({ rating, interval }) => {
    const node = document.getElementById('preview-' + rating);
    if (node) node.textContent = formatSrsInterval(previews[rating], interval);
  });
}
function ratingsVisible() {
  const ratingRow = document.getElementById('ratingRow');
  return Boolean(ratingRow && !ratingRow.hidden);
}
function isCardRevealed() {
  const meaning = document.getElementById('meaning');
  return Boolean(meaning && meaning.classList.contains('show'));
}
// Rating buttons appear only once the answer is visible; before that, one "Lật thẻ" button.
function syncRevealControls() {
  const revealBtn = document.getElementById('revealBtn');
  const ratingRow = document.getElementById('ratingRow');
  if (!revealBtn || !ratingRow) return;
  const hasCard = filteredOrder.length > 0;
  const revealed = hasCard && isCardRevealed();
  revealBtn.hidden = !hasCard || revealed;
  ratingRow.hidden = !revealed;
}
function updateProgress(current, total) {
  document.getElementById('progress').textContent = total === 0 ? '0 / 0' : current + ' / ' + total;
  const bar = document.getElementById('progressBar');
  if (bar) bar.style.width = (total === 0 ? 0 : (current / total * 100)) + '%';
}
function ensureStudyWordList() {
  if (!document.body.classList.contains('is-desktop-dock')) return null;
  let panel = document.getElementById('studyWordListPanel');
  if (panel) return panel;
  const mount = document.getElementById('workstationLeft');
  if (!mount) return null;
  panel = document.createElement('section');
  panel.id = 'studyWordListPanel';
  panel.className = 'study-word-list-panel';
  panel.setAttribute('aria-label', 'Danh sách từ trong bài học hiện tại');
  panel.innerHTML = `
    <div class="study-word-list-heading">
      <div class="study-word-list-header-row">
        <strong id="studyWordListTitle">Danh sách từ</strong>
        <span id="studyWordListCount" class="study-word-count-badge"></span>
      </div>
      <div id="studyWordListActiveWord" class="study-word-active-banner"></div>
      <label class="study-word-list-search">
        <span class="sr-only">Tìm trong bài học</span>
        <input type="search" id="studyWordListSearch" placeholder="Tìm kiếm từ trong bài..." autocomplete="off">
      </label>
    </div>
    <div class="study-word-list-items" id="studyWordListItems" role="listbox" aria-label="Chọn từ trong bài học"></div>`;
  mount.appendChild(panel);
  panel.querySelector('#studyWordListSearch').addEventListener('input', renderStudyWordList);
  return panel;
}

function renderStudyWordList() {
  const panel = ensureStudyWordList();
  if (!panel) return;
  const items = panel.querySelector('#studyWordListItems');
  const query = panel.querySelector('#studyWordListSearch').value.trim().toLowerCase();
  const currentIndex = filteredOrder.length ? filteredOrder[idx % filteredOrder.length] : -1;
  const activeWord = currentIndex >= 0 ? WORDS[currentIndex] : null;

  const countBadge = panel.querySelector('#studyWordListCount');
  if (countBadge) {
    const levelLabel = currentLevel && LEVELS[currentLevel] ? LEVELS[currentLevel].label : '';
    countBadge.textContent = WORDS.length ? `${levelLabel} · ${WORDS.length} từ` : '';
  }

  const activeBanner = panel.querySelector('#studyWordListActiveWord');
  if (activeBanner) {
    if (activeWord) {
      const status = progress[activeWord.id];
      const statusText = status === 'known' ? 'Đã nhớ' : status === 'unknown' ? 'Chưa nhớ' : 'Chưa học';
      const statusClass = status === 'known' ? 'badge-known' : status === 'unknown' ? 'badge-unknown' : 'badge-unseen';
      activeBanner.innerHTML = `
        <div class="active-word-info">
          <span class="active-kicker">Từ số ${currentIndex + 1}:</span>
          <strong class="active-hanzi">${activeWord.hanzi}</strong>
          <span class="active-py">${activeWord.pinyin || ''}</span>
        </div>
        <span class="active-status ${statusClass}">${statusText}</span>
      `;
    } else {
      activeBanner.innerHTML = '<span class="active-kicker">Chọn một từ để học</span>';
    }
  }

  items.innerHTML = WORDS.map((word, wordIndex) => ({ word, wordIndex }))
    .filter(({ word }) => !query || `${word.hanzi} ${word.pinyin} ${word.meaning}`.toLowerCase().includes(query))
    .map(({ word, wordIndex }) => {
      const isCurrent = wordIndex === currentIndex;
      const status = progress[word.id];
      const statusIcon = status === 'known' ? '✓' : status === 'unknown' ? '✗' : '·';
      const statusClass = status === 'known' ? 'status-known' : status === 'unknown' ? 'status-unknown' : 'status-unseen';
      return `
        <button type="button" class="study-word-list-item${isCurrent ? ' active' : ''}"
          role="option" aria-selected="${isCurrent}" data-word-index="${wordIndex}"
          title="${word.hanzi} ${word.pinyin || ''} - ${word.meaning || ''}">
          <span class="study-word-status ${statusClass}" aria-hidden="true">${statusIcon}</span>
          <span class="study-word-list-content">
            <span class="study-word-list-main">
              <span class="study-word-list-hanzi">${word.hanzi}</span>
              <span class="word-py">${word.pinyin || ''}</span>
            </span>
            <small class="word-vi">${word.meaning || ''}</small>
          </span>
          <span class="study-word-list-number">#${wordIndex + 1}</span>
        </button>
      `;
    }).join('');

  items.querySelectorAll('[data-word-index]').forEach(button => {
    button.addEventListener('click', () => {
      const wordIndex = Number(button.dataset.wordIndex);
      let filteredIndex = filteredOrder.indexOf(wordIndex);
      if (filteredIndex < 0) {
        currentFilter = 'all';
        filteredOrder = order.slice();
        renderFilters();
        filteredIndex = filteredOrder.indexOf(wordIndex);
      }
      if (filteredIndex >= 0) {
        idx = filteredIndex;
        render('fade');
      }
    });
  });

  if (currentIndex >= 0) {
    const activeButton = items.querySelector('.active');
    if (activeButton && !query) activeButton.scrollIntoView({ block: 'nearest' });
  }
}
function render(animate) {
  stopSpeech();
  if (transitionTimer) { clearTimeout(transitionTimer); transitionTimer = null; }
  // Hide ratings right away so a double press cannot rate the next card during the exit animation.
  const ratingRow = document.getElementById('ratingRow');
  if (ratingRow) ratingRow.hidden = true;

  const content = document.getElementById('cardContent');
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function applyContent() {
    if (content) content.className = 'card-content';
    const exBox = document.getElementById('exampleBox');
    if (exBox) exBox.classList.remove('show');
    const soundBtn = document.getElementById('soundBtn');
    if (soundBtn) soundBtn.classList.remove('show');
    if (filteredOrder.length === 0) {
      document.getElementById('hanzi').textContent = '';
      document.getElementById('pinyin').textContent = '';
      document.getElementById('meaning').textContent = 'Không có từ trong bộ lọc này';
      document.getElementById('meaning').classList.add('show');
      document.getElementById('hint').textContent = '';
      if (content) content.classList.add('is-empty');
      updateProgress(0, 0);
      updateStats();
      setActiveStudyWord(null);
      renderStudyWordList();
      syncRevealControls();
      return;
    }
    if (content) content.classList.remove('is-empty');
    const wIdx = filteredOrder[idx % filteredOrder.length];
    const w = WORDS[wIdx];
    if (!w) return; // deck was swapped out (level change) while this render was pending
    setActiveStudyWord(w);
    renderStudyWordList();
    updateSrsPreviews(w);
    document.getElementById('hanzi').textContent = w.hanzi;
    document.getElementById('pinyin').textContent = showPinyin ? w.pinyin : '';
    const m = document.getElementById('meaning');
    m.textContent = w.meaning;
    m.classList.remove('show');
    const hasExample = Boolean(w.example_zh || w.example_py || w.example_vi);
    const exampleBox = document.getElementById('exampleBox');
    if (exampleBox) exampleBox.hidden = !hasExample;
    document.getElementById('exZh').innerHTML = w.example_zh;
    document.getElementById('exPy').innerHTML = w.example_py;
    document.getElementById('exVi').innerHTML = w.example_vi;
    document.getElementById('hint').textContent = hasExample
      ? 'Nhấn vào thẻ để xem nghĩa và ví dụ'
      : 'Nhấn vào thẻ để xem nghĩa';
    updateProgress(idx % filteredOrder.length + 1, filteredOrder.length);
    updateStats();
    syncRevealControls();
    if (animate && content && !prefersReduced) {
      if (animate === 'next') content.classList.add('enter-right');
      else if (animate === 'prev') content.classList.add('enter-left');
      else content.classList.add('enter-fade');
    }
  }

  if (!animate || !content || prefersReduced) {
    applyContent();
    return;
  }

  content.className = 'card-content';
  if (animate === 'next') content.classList.add('exit-left');
  else if (animate === 'prev') content.classList.add('exit-right');
  else content.classList.add('exit-fade');

  transitionTimer = setTimeout(() => {
    transitionTimer = null;
    applyContent();
  }, 150);
}
