// Flashcard markup, filtering, statistics, and rendering.
function buildCardArea() {
  document.getElementById('cardArea').innerHTML = `
    <div class="progress-bar-track">
      <div class="progress-bar-fill" id="progressBar"></div>
    </div>
    <div class="card" id="card">
      <div class="swipe-badge swipe-badge--known" id="swipeBadgeKnown">✓ Đã nhớ</div>
      <div class="swipe-badge swipe-badge--unknown" id="swipeBadgeUnknown">✗ Chưa nhớ</div>
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

    <div class="nav-row">
      <button onclick="prevCard()">← Trước</button>
      <span class="progress-text" id="progress">1 / ${WORDS.length}</span>
      <button onclick="nextCard()">Tiếp →</button>
    </div>

    <div class="action-row">
      <button class="btn-unknown" onclick="markUnknown()">Chưa nhớ</button>
      <button class="btn-known" onclick="markKnown()">Đã nhớ</button>
      <button class="show-unknown-btn" id="unknownWordsToggle" onclick="toggleUnknownWords()"
        aria-controls="unknownWordsList" aria-expanded="false">
        Hiển thị từ chưa nhớ
      </button>
      <button class="reset-progress-btn" onclick="resetProgress()">↻ Học lại từ đầu</button>
    </div>
    <div class="unknown-words-list" id="unknownWordsList"></div>
  `;
  const btn = document.getElementById('pinyinToggle');
  btn.textContent = showPinyin ? '👁 Đang hiện pinyin' : '🙈 Chế độ thử thách: ẩn pinyin';
  btn.classList.toggle('on', !showPinyin);
  initSwipe();
}

function renderFilters() {
  const row = document.getElementById('filterRow');
  row.innerHTML = '';
  const filters = [
    {key:'all', label:'Tất cả'},
    {key:'unknown', label:'Chưa nhớ'},
    {key:'known', label:'Đã nhớ'},
    {key:'unseen', label:'Chưa học'}
  ];
  filters.forEach(f => {
    const b = document.createElement('button');
    b.className = 'filter-btn' + (currentFilter === f.key ? ' active' : '');
    b.textContent = f.label;
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
  render('fade');
}
function updateStats() {
  let known = 0, unknown = 0;
  Object.values(progress).forEach(v => { if (v === 'known') known++; else if (v === 'unknown') unknown++; });
  document.getElementById('s-total').textContent = WORDS.length;
  document.getElementById('s-known').textContent = known;
  document.getElementById('s-unknown').textContent = unknown;
  document.getElementById('s-unseen').textContent = WORDS.length - known - unknown;
}
function updateProgress(current, total) {
  document.getElementById('progress').textContent = total === 0 ? '0 / 0' : current + ' / ' + total;
  const bar = document.getElementById('progressBar');
  if (bar) bar.style.width = (total === 0 ? 0 : (current / total * 100)) + '%';
}
function render(animate) {
  stopSpeech();
  if (transitionTimer) { clearTimeout(transitionTimer); transitionTimer = null; }

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
      return;
    }
    if (content) content.classList.remove('is-empty');
    const wIdx = filteredOrder[idx % filteredOrder.length];
    const w = WORDS[wIdx];
    document.getElementById('hanzi').textContent = w.hanzi;
    document.getElementById('pinyin').textContent = showPinyin ? w.pinyin : '';
    const m = document.getElementById('meaning');
    m.textContent = w.meaning;
    m.classList.remove('show');
    document.getElementById('exZh').innerHTML = w.example_zh;
    document.getElementById('exPy').innerHTML = w.example_py;
    document.getElementById('exVi').innerHTML = w.example_vi;
    document.getElementById('hint').textContent = 'Nhấn vào thẻ để xem nghĩa và ví dụ';
    updateProgress(idx % filteredOrder.length + 1, filteredOrder.length);
    updateStats();
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
