// Flashcard markup, filtering, statistics, and rendering.
function buildCardArea() {
  document.getElementById('cardArea').innerHTML = `
    <div class="card" id="card">
      <div class="card-header-bar card-interactive" id="cardHeaderBar" onclick="event.stopPropagation()">
        <span class="card-position-badge" id="cardPositionBadge">0 / 0</span>
        <div class="card-toolbar" id="cardToolbar">
          <button type="button" class="card-tool-btn" id="randomWordBtn" onclick="jumpToRandomWord()" aria-label="Hiện từ ngẫu nhiên (R)" title="Hiện từ ngẫu nhiên (R)">
            <span aria-hidden="true">🎲</span>
          </button>
          <button type="button" class="card-tool-btn" id="shuffleBtn" onclick="shuffleDeck()" aria-label="Xáo trộn bộ từ" title="Xáo trộn bộ từ">
            <span aria-hidden="true">🔀</span>
          </button>
          <button type="button" class="card-tool-btn" id="pinyinToggle" onclick="togglePinyin()" aria-label="Ẩn hoặc hiện pinyin" title="Ẩn hoặc hiện pinyin">
            <span id="pinyinToggleIcon" aria-hidden="true">👁</span>
          </button>
          <button type="button" class="card-tool-btn" id="hanvietToggle" onclick="toggleHanViet()" aria-label="Bật hoặc tắt âm Hán - Việt (H)" title="Bật hoặc tắt âm Hán - Việt (H)">
            <span id="hanvietToggleIcon" aria-hidden="true">漢</span>
          </button>
          <button type="button" class="card-tool-btn" id="cardWritingBtn" onclick="toggleStudyWritingPanel()" aria-label="Luyện viết chữ Hán (W)" title="Luyện viết chữ Hán (W)">
            <span aria-hidden="true">✍️</span>
          </button>
          <button type="button" class="card-tool-btn" id="weakWordToggleBtn" onclick="toggleWeakWord(activeStudyWord && activeStudyWord.hanzi, currentLevel)" aria-label="Đánh dấu từ khó" title="Đánh dấu từ khó">
            <span id="weakWordToggleIcon" aria-hidden="true">☆</span>
          </button>
          <button type="button" class="card-tool-btn" id="transferToggle" onclick="toggleTransferPanel()" aria-label="Sao lưu tiến trình" title="Sao lưu tiến trình" aria-controls="transferPanel" aria-expanded="false">
            <span aria-hidden="true">💾</span>
          </button>
          <button type="button" class="card-tool-btn" id="aiSettingsToggleBtn" onclick="openAiSettingsModal()" aria-label="Google AI Studio Key" title="Cài đặt Google AI Studio Key">
            <span aria-hidden="true">✨</span>
          </button>
        </div>
      </div>
      <div class="swipe-badge swipe-badge--known" id="swipeBadgeKnown">✓ Đã nhớ</div>
      <div class="swipe-badge swipe-badge--unknown" id="swipeBadgeUnknown">✗ Chưa nhớ</div>
      <div id="cardContent" class="card-content">
        <div class="word-main-block split-layout" id="wordMainBlock">
          <!-- Cột trái: Hình ảnh minh họa / Neo thị giác (Visual Mnemonic - Gợi hình thuần túy) -->
          <div class="card-visual-col" id="cardVisualCol">
            <div class="card-illustration-frame" id="cardIllustrationFrame" title="Minh họa gợi hình">
              <div class="ai-skeleton-loader" id="aiSkeletonLoader" hidden>
                <div class="ai-shimmer-wave"></div>
                <div class="ai-loading-indicator">
                  <span class="ai-spinner"></span>
                  <span class="ai-loading-text">Google AI Studio...</span>
                </div>
              </div>
              <img class="card-illustration-img" id="cardIllustrationImg" alt="Minh họa gợi hình" hidden>
              <div class="card-illustration-svg" id="cardIllustrationSvg"></div>
              <button type="button" class="ai-gen-trigger-btn" id="aiGenTriggerBtn"
                onclick="event.stopPropagation(); handleAiImageGenClick()"
                title="Tạo ảnh minh họa bằng Google AI Studio">
                ✨ Tạo ảnh AI
              </button>
            </div>
          </div>

          <!-- Cột phải: Chữ Hán, Pinyin, Từ loại & Nghĩa -->
          <div class="card-content-col" id="cardContentCol">
            <div class="hanzi" id="hanzi" onclick="event.stopPropagation(); toggleStudyWritingPanel(true)" title="Nhấn để luyện viết và xem thứ tự nét (W)"></div>
            <div class="pinyin-row" id="pinyinRow">
              <div class="pinyin" id="pinyin"></div>
              <span class="hanviet-badge" id="hanvietBadge" title="Âm Hán - Việt"></span>
              <span class="pos-badge" id="posBadge" title="Từ loại"></span>
              <button class="sound-btn speech-btn" id="soundBtn" type="button"
                onclick="event.stopPropagation(); speakWord()"
                aria-label="Nghe phát âm" aria-live="polite">
                <span class="sound-btn-icon" aria-hidden="true">🔊</span>
              </button>
            </div>
            <div class="meaning" id="meaning"></div>
          </div>
        </div>
        <div class="example-box" id="exampleBox">
          <div class="ex-header-row">
            <span class="ex-label">Ví dụ</span>
            <div class="example-audio-controls card-interactive">
              <button class="example-sound-btn speech-btn" id="exampleSoundBtn" type="button"
                onclick="event.stopPropagation(); speakExample()"
                aria-label="Nghe câu ví dụ" aria-live="polite">
                <span class="sound-btn-icon" aria-hidden="true">🔊</span>
              </button>
              <details class="example-speed-picker" id="exampleSpeedPicker"
                onclick="event.stopPropagation()">
                <summary aria-label="Tốc độ đọc câu ví dụ: ${formatExampleSpeechSpeed(exampleSpeechSpeed)}">
                  <span class="example-speed-label">Tốc độ</span>
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
          <div class="ex-line ex-zh" id="exZh"></div>
          <div class="ex-line ex-py" id="exPy"></div>
          <div class="ex-line ex-vi" id="exVi"></div>
        </div>
        <div class="hint" id="hint">Nhấn vào thẻ để xem nghĩa và ví dụ</div>
      </div>
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
  const hanvietBtn = document.getElementById('hanvietToggle');
  if (hanvietBtn) {
    hanvietBtn.classList.toggle('on', !showHanViet);
    hanvietBtn.title = showHanViet ? 'Ẩn âm Hán - Việt (H)' : 'Hiện âm Hán - Việt (H)';
    hanvietBtn.setAttribute('aria-label', showHanViet ? 'Ẩn âm Hán - Việt (H)' : 'Hiện âm Hán - Việt (H)');
  }
  const topbarHanvietBtn = document.getElementById('studyHanvietToggleBtn');
  if (topbarHanvietBtn) {
    topbarHanvietBtn.classList.toggle('active', showHanViet);
  }
  if (typeof updateWeakWordToggleButton === 'function') updateWeakWordToggleButton();
  updateProgress();
  updateCardPosition();
  initSwipe();
}

function toggleHanViet() {
  showHanViet = !showHanViet;
  try { localStorage.setItem('hsk_show_hanviet', String(showHanViet)); } catch (e) {}
  document.body.classList.toggle('hide-hanviet', !showHanViet);
  document.documentElement.classList.toggle('hide-hanviet', !showHanViet);
  const badge = document.getElementById('hanvietBadge');
  if (badge) {
    badge.style.display = showHanViet && badge.textContent ? 'inline-flex' : 'none';
  }
  const btn = document.getElementById('hanvietToggle');
  if (btn) {
    btn.classList.toggle('on', !showHanViet);
    btn.title = showHanViet ? 'Ẩn âm Hán - Việt (H)' : 'Hiện âm Hán - Việt (H)';
    btn.setAttribute('aria-label', showHanViet ? 'Ẩn âm Hán - Việt (H)' : 'Hiện âm Hán - Việt (H)');
  }
  const topbarBtn = document.getElementById('studyHanvietToggleBtn');
  if (topbarBtn) {
    topbarBtn.classList.toggle('active', showHanViet);
  }
  document.querySelectorAll('.hanviet-badge, .study-word-hanviet, .active-hv, .vocabulary-hanviet').forEach(el => {
    el.style.display = showHanViet ? '' : 'none';
  });
}
window.toggleHanViet = toggleHanViet;

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
  updateProgress();
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
    const shortcutArrow = button.rating === 'again' ? '←' : '→';
    return `
    <button type="button" class="rating-btn rating-btn--${button.rating}"
      onclick="${handlerName}('${button.rating}')" aria-keyshortcuts="${button.key}"
      title="Đánh giá: ${button.label} (Phím [${button.key}] hoặc [${shortcutArrow}])">
      <div class="rating-main-label">
        <span class="rating-emoji" aria-hidden="true">${button.emoji}</span>
        <span class="rating-label">${button.label}</span>
        <kbd class="rating-kbd" aria-hidden="true">${button.key}</kbd>
      </div>
      <span class="rating-interval"${previewIdPrefix ? ` id="${previewIdPrefix}${button.rating}"` : ''}>${intervalText}</span>
    </button>`;
  }).join('');
}
function revealButtonHtml(onclick, id) {
  return `<button type="button" class="reveal-btn" id="${id}" onclick="${onclick}" aria-keyshortcuts="Space" title="Lật thẻ (Phím Space)">
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
function computeDeckProgress() {
  if (!Array.isArray(WORDS) || WORDS.length === 0) {
    return { learned: 0, total: 0, pct: 0, known: 0, unknown: 0 };
  }
  let known = 0, unknown = 0;
  WORDS.forEach(w => {
    const st = progress[w.id];
    if (st === 'known') known++;
    else if (st === 'unknown') unknown++;
  });
  const learned = known + unknown;
  const total = WORDS.length;
  const pct = total === 0 ? 0 : Math.round((learned / total) * 100);
  return { learned, total, pct, known, unknown };
}

function updateProgress(current, total) {
  const deck = computeDeckProgress();
  const el = document.getElementById('progress');
  if (el) el.textContent = deck.total === 0 ? '0 / 0' : `${deck.learned} / ${deck.total}`;
  const bar = document.getElementById('progressBar');
  if (bar) bar.style.width = deck.pct + '%';
  const pctEl = document.getElementById('progressPct');
  if (pctEl) pctEl.textContent = deck.pct + '%';
  const topbar = document.getElementById('studyTopbarProgress');
  if (topbar) {
    topbar.title = `Tiến độ học: ${deck.learned}/${deck.total} (${deck.pct}%) • Đã nhớ: ${deck.known}, Chưa nhớ: ${deck.unknown}`;
  }
}

function updateCardPosition() {
  const badge = document.getElementById('cardPositionBadge');
  if (!badge) return;
  if (!filteredOrder || filteredOrder.length === 0) {
    badge.textContent = '0 / 0';
    return;
  }
  const current = (idx % filteredOrder.length) + 1;
  const total = filteredOrder.length;
  badge.textContent = `${current} / ${total}`;
  const filterLabel = currentFilter === 'all' ? 'Tất cả'
    : currentFilter === 'known' ? 'Đã nhớ'
    : currentFilter === 'unknown' ? 'Chưa nhớ'
    : currentFilter === 'unseen' ? 'Chưa học' : currentFilter;
  badge.title = `Thẻ ${current} / ${total} (${filterLabel})`;
}

function toggleStudySidebar(forceOpen) {
  const isOpen = document.body.classList.contains('study-sidebar-open');
  const isTargetTab = document.body.dataset.sidebarTab === 'words';
  const shouldOpen = typeof forceOpen === 'boolean' ? forceOpen : (!isOpen || !isTargetTab);

  if (shouldOpen) {
    document.body.classList.add('study-sidebar-open');
    if (typeof window.setSidebarStudyTab === 'function') {
      window.setSidebarStudyTab('words');
    }
    if (typeof renderStudyWordList === 'function') {
      renderStudyWordList();
    }
    if (typeof SpaRouter !== 'undefined' && !SpaRouter.isNavigatingFromPopstate()) {
      SpaRouter.pushView({ view: 'cards', level: currentLevel, drawerOpen: true });
    }
  } else {
    document.body.classList.remove('study-sidebar-open');
  }
  updateStudyDrawerButtons();
}

function toggleStudyWritingPanel(forceOpen) {
  const isOpen = document.body.classList.contains('study-sidebar-open');
  const isTargetTab = document.body.dataset.sidebarTab === 'stroke';
  const shouldOpen = typeof forceOpen === 'boolean' ? forceOpen : (!isOpen || !isTargetTab);

  if (shouldOpen) {
    document.body.classList.add('study-sidebar-open');
    if (typeof window.setSidebarStudyTab === 'function') {
      window.setSidebarStudyTab('stroke');
    }
    if (typeof renderActiveStrokeChar === 'function') {
      setTimeout(() => renderActiveStrokeChar(true), 50);
    }
    if (typeof SpaRouter !== 'undefined' && !SpaRouter.isNavigatingFromPopstate()) {
      SpaRouter.pushView({ view: 'cards', level: currentLevel, drawerOpen: true });
    }
  } else {
    document.body.classList.remove('study-sidebar-open');
  }
  updateStudyDrawerButtons();
}

function closeAllStudyDrawers() {
  const wasOpen = document.body.classList.contains('study-sidebar-open');
  document.body.classList.remove('study-sidebar-open');
  updateStudyDrawerButtons();
  if (wasOpen && typeof SpaRouter !== 'undefined' && !SpaRouter.isNavigatingFromPopstate()) {
    if (window.history.state && window.history.state.drawerOpen) {
      window.history.back();
    }
  }
}

function updateStudyDrawerButtons() {
  const isPanelOpen = document.body.classList.contains('study-sidebar-open');
  const activeTab = document.body.dataset.sidebarTab || 'stroke';

  const sidebarBtn = document.getElementById('studySidebarToggleBtn');
  if (sidebarBtn) sidebarBtn.classList.toggle('active', isPanelOpen && activeTab === 'words');
  const writingBtn = document.getElementById('studyWritingToggleBtn');
  if (writingBtn) writingBtn.classList.toggle('active', isPanelOpen && activeTab === 'stroke');
  const cardWritingBtn = document.getElementById('cardWritingBtn');
  if (cardWritingBtn) cardWritingBtn.classList.toggle('active', isPanelOpen && activeTab === 'stroke');
}

function ensureStudyWordList() {
  if (!document.body.classList.contains('is-desktop-dock') && !document.body.classList.contains('flashcard-study-mode')) return null;
  let panel = document.getElementById('studyWordListPanel');
  if (panel) return panel;
  const isStudy = document.body.classList.contains('flashcard-study-mode');
  const mount = isStudy
    ? (document.getElementById('workstationRight') || document.getElementById('workstationLeft'))
    : document.getElementById('workstationLeft');
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
        <button type="button" class="study-drawer-close-btn" onclick="closeAllStudyDrawers()" aria-label="Đóng danh sách">✕</button>
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
          ${activeWord.hanviet ? `<span class="active-hv">［${activeWord.hanviet}］</span>` : ''}
        </div>
        <span class="active-status ${statusClass}">${statusText}</span>
      `;
    } else {
      activeBanner.innerHTML = '<span class="active-kicker">Chọn một từ để học</span>';
    }
  }

  items.innerHTML = WORDS.map((word, wordIndex) => ({ word, wordIndex }))
    .filter(({ word }) => !query || `${word.hanzi} ${word.pinyin} ${word.hanviet || ''} ${word.meaning}`.toLowerCase().includes(query))
    .map(({ word, wordIndex }) => {
      const isCurrent = wordIndex === currentIndex;
      const status = progress[word.id];
      const statusIcon = status === 'known' ? '✓' : status === 'unknown' ? '✗' : '·';
      const statusClass = status === 'known' ? 'status-known' : status === 'unknown' ? 'status-unknown' : 'status-unseen';
      return `
        <button type="button" class="study-word-list-item${isCurrent ? ' active' : ''}"
          role="option" aria-selected="${isCurrent}" data-word-index="${wordIndex}"
          title="${word.hanzi} ${word.pinyin || ''}${word.hanviet ? ' ［' + word.hanviet + '］' : ''} - ${word.meaning || ''}">
          <span class="study-word-status ${statusClass}" aria-hidden="true">${statusIcon}</span>
          <span class="study-word-list-content">
            <span class="study-word-list-main">
              <span class="study-word-list-hanzi">${word.hanzi}</span>
              <span class="word-py">${word.pinyin || ''}</span>
              ${word.hanviet ? `<span class="study-word-hanviet">［${word.hanviet}］</span>` : ''}
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
        if (window.innerWidth < 768) {
          closeAllStudyDrawers();
        }
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
      const emptyHv = document.getElementById('hanvietBadge');
      if (emptyHv) { emptyHv.textContent = ''; emptyHv.style.display = 'none'; }
      const emptyPos = document.getElementById('posBadge');
      if (emptyPos) { emptyPos.textContent = ''; emptyPos.hidden = true; emptyPos.style.display = 'none'; }
      document.getElementById('meaning').textContent = 'Không có từ trong bộ lọc này';
      document.getElementById('meaning').classList.add('show');
      document.getElementById('hint').textContent = '';
      const emptySvg = document.getElementById('cardIllustrationSvg');
      const emptyImg = document.getElementById('cardIllustrationImg');
      if (emptySvg) emptySvg.innerHTML = '';
      if (emptyImg) { emptyImg.src = ''; emptyImg.hidden = true; }
      const skeletonEl = document.getElementById('aiSkeletonLoader');
      if (skeletonEl) skeletonEl.hidden = true;
      const genBtn = document.getElementById('aiGenTriggerBtn');
      if (genBtn) genBtn.hidden = true;
      if (content) content.classList.add('is-empty');
      updateProgress();
      updateCardPosition();
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
    const hvBadge = document.getElementById('hanvietBadge');
    if (hvBadge) {
      const hv = (typeof getWordHanViet === 'function' ? getWordHanViet(w) : '') || w.hanviet;
      if (hv) {
        hvBadge.textContent = `［${hv}］`;
        hvBadge.hidden = false;
        hvBadge.style.display = showHanViet ? 'inline-flex' : 'none';
      } else {
        hvBadge.textContent = '';
        hvBadge.hidden = true;
        hvBadge.style.display = 'none';
      }
    }

    // Cập nhật Part of Speech (Từ loại)
    const pos = (typeof getWordPartOfSpeech === 'function') ? getWordPartOfSpeech(w) : null;
    const posBadge = document.getElementById('posBadge');
    if (posBadge) {
      if (pos && pos.label) {
        posBadge.textContent = pos.label;
        posBadge.className = `pos-badge pos-badge--${pos.code || 'noun'}`;
        posBadge.title = `Từ loại: ${pos.full || pos.label}`;
        posBadge.hidden = false;
        posBadge.style.display = 'inline-flex';
      } else {
        posBadge.textContent = '';
        posBadge.hidden = true;
        posBadge.style.display = 'none';
      }
    }

    const m = document.getElementById('meaning');
    m.textContent = w.meaning;
    m.classList.remove('show');
    const hasExample = Boolean(w.example_zh || w.example_py || w.example_vi);
    const exampleBox = document.getElementById('exampleBox');
    if (exampleBox) exampleBox.hidden = !hasExample;
    document.getElementById('exZh').innerHTML = w.example_zh;
    document.getElementById('exPy').innerHTML = w.example_py;
    document.getElementById('exVi').innerHTML = w.example_vi;

    // Cập nhật hình ảnh minh họa trực quan (Visual Mnemonic Anchor)
    const imgEl = document.getElementById('cardIllustrationImg');
    const svgEl = document.getElementById('cardIllustrationSvg');
    const frameEl = document.getElementById('cardIllustrationFrame');
    const skeletonEl = document.getElementById('aiSkeletonLoader');
    const genBtn = document.getElementById('aiGenTriggerBtn');

    if (skeletonEl) skeletonEl.hidden = true;
    if (genBtn) {
      genBtn.hidden = false;
      genBtn.textContent = '✨ Tạo ảnh AI';
    }

    if (imgEl && svgEl) {
      // 1. Render ngay hình mẫu vector/curated motif để không bị giật lag
      if (typeof getWordIllustration === 'function') {
        const illu = getWordIllustration(w);
        if (illu) {
          if (illu.type === 'img') {
            imgEl.src = illu.src;
            imgEl.alt = 'Minh họa gợi hình';
            imgEl.hidden = false;
            svgEl.hidden = true;
            svgEl.innerHTML = '';
          } else if (illu.type === 'svg') {
            svgEl.innerHTML = illu.svg;
            svgEl.hidden = false;
            imgEl.hidden = true;
            imgEl.src = '';
          }
          if (frameEl) {
            frameEl.title = 'Minh họa gợi hình';
          }
        }
      }

      // 2. Kiểm tra cache ảnh AI từ IndexedDB
      if (typeof AiImageCache !== 'undefined') {
        const currentHanzi = w.hanzi;
        AiImageCache.get(currentHanzi).then(cached => {
          if (!cached || !activeStudyWord || activeStudyWord.hanzi !== currentHanzi) return;
          if (cached.type === 'img') {
            imgEl.src = cached.src;
            imgEl.alt = 'Minh họa gợi hình';
            imgEl.hidden = false;
            svgEl.hidden = true;
            svgEl.innerHTML = '';
          } else if (cached.type === 'svg') {
            svgEl.innerHTML = cached.svg;
            svgEl.hidden = false;
            imgEl.hidden = true;
            imgEl.src = '';
          }
          if (genBtn) genBtn.textContent = '↻ Tạo lại';
        }).catch(() => {});
      }
    }

    document.getElementById('hint').textContent = hasExample
      ? 'Nhấn vào thẻ để xem nghĩa và ví dụ'
      : 'Nhấn vào thẻ để xem nghĩa';
    updateProgress();
    updateCardPosition();
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
