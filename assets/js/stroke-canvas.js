// Right sidebar: Hanzi Writer stroke-order canvas with animate + quiz mode.
let strokeCanvasWriter = null;
let currentStrokeChar = '';

function destroyStrokeCanvasWriter() {
  const el = document.getElementById('strokeCanvasTarget');
  if (el) {
    el.innerHTML = '';
    el.classList.remove('is-quiz-mode');
  }
  strokeCanvasWriter = null;
  currentStrokeChar = '';
  const hint = document.getElementById('strokeQuizHint');
  if (hint) { hint.hidden = true; hint.textContent = ''; }
  const animateBtn = document.getElementById('strokeAnimateBtn');
  const quizBtn = document.getElementById('strokeQuizBtn');
  if (animateBtn) animateBtn.classList.remove('active');
  if (quizBtn) quizBtn.classList.remove('active');
}

function loadStrokeCanvasWord(word) {
  const target = document.getElementById('strokeCanvasTarget');
  const fallback = document.getElementById('strokeCanvasFallback');
  const badge = document.getElementById('strokeCharBadge');
  if (!target || !fallback) return;
  destroyStrokeCanvasWriter();
  fallback.hidden = true;

  if (!word || !word.hanzi || typeof HanziWriter === 'undefined') {
    fallback.hidden = false;
    fallback.textContent = !word ? 'Chọn một từ để xem thứ tự nét.' : 'Không thể tải thư viện viết chữ.';
    if (badge) badge.textContent = '';
    syncStrokeCanvasControls();
    return;
  }

  const thisChar = word.hanzi[0]; // canvas shows first character of multi-char words
  currentStrokeChar = thisChar;
  if (badge) badge.textContent = word.hanzi.length > 1 ? `${thisChar} (từ ${word.hanzi})` : thisChar;

  try {
    strokeCanvasWriter = HanziWriter.create('strokeCanvasTarget', thisChar, {
      width: 180,
      height: 180,
      padding: 10,
      showOutline: true,
      strokeColor: '#2b2926',
      radicalColor: '#c2654a',
      showHintAfterMisses: 2,
      highlightOnComplete: true,
    });
    // Auto-animate stroke order smoothly so user immediately sees how to write
    strokeCanvasWriter.animateCharacter({
      onComplete: () => {
        const hint = document.getElementById('strokeQuizHint');
        if (hint) {
          hint.hidden = false;
          hint.textContent = '💡 Bấm trực tiếp vào ô chữ để tự luyện viết!';
        }
      }
    });
  } catch (e) {
    fallback.hidden = false;
    fallback.textContent = 'Không thể tải nét chữ cho ký tự này.';
  }
  syncStrokeCanvasControls();
}

// Buttons do nothing without a writer (no word chosen, or the character failed to load).
function syncStrokeCanvasControls() {
  ['strokeAnimateBtn', 'strokeQuizBtn'].forEach(id => {
    const button = document.getElementById(id);
    if (button) button.disabled = !strokeCanvasWriter;
  });
}

function animateStrokeCanvas() {
  if (!strokeCanvasWriter) return;
  const target = document.getElementById('strokeCanvasTarget');
  if (target) target.classList.remove('is-quiz-mode');
  const animateBtn = document.getElementById('strokeAnimateBtn');
  const quizBtn = document.getElementById('strokeQuizBtn');
  const hint = document.getElementById('strokeQuizHint');
  if (animateBtn) animateBtn.classList.add('active');
  if (quizBtn) quizBtn.classList.remove('active');
  if (hint) {
    hint.hidden = false;
    hint.textContent = `Đang diễn họa thứ tự nét chữ "${currentStrokeChar}"…`;
  }
  strokeCanvasWriter.animateCharacter({
    onComplete: () => {
      if (animateBtn) animateBtn.classList.remove('active');
      if (hint) {
        hint.textContent = 'Bấm trực tiếp vào ô hoặc nhấn "Luyện viết" để thử viết!';
      }
    }
  });
}

function quizStrokeCanvas() {
  if (!strokeCanvasWriter) return;
  const target = document.getElementById('strokeCanvasTarget');
  if (target) target.classList.add('is-quiz-mode');
  const animateBtn = document.getElementById('strokeAnimateBtn');
  const quizBtn = document.getElementById('strokeQuizBtn');
  const hint = document.getElementById('strokeQuizHint');
  if (quizBtn) quizBtn.classList.add('active');
  if (animateBtn) animateBtn.classList.remove('active');
  if (hint) {
    hint.hidden = false;
    hint.textContent = `✍️ Hãy vẽ nét chữ "${currentStrokeChar}" vào ô bên trên!`;
  }
  strokeCanvasWriter.quiz({
    onMistake: () => {
      if (hint) hint.textContent = 'Nét chưa chuẩn. Hãy thử lại theo đường mờ!';
    },
    onCorrectStroke: (strokeData) => {
      if (hint) hint.textContent = `Đúng nét ${strokeData.strokeNum + 1}! Tiếp tục nào…`;
    },
    onComplete: (summary) => {
      if (quizBtn) quizBtn.classList.remove('active');
      if (target) target.classList.remove('is-quiz-mode');
      if (hint) {
        hint.textContent = `🎉 Tuyệt vời! Bạn đã viết hoàn chỉnh chữ "${currentStrokeChar}" với ${summary.totalMistakes} lỗi sai!`;
      }
    }
  });
}

function initStrokeCanvas() {
  const isDesktop = document.body.classList.contains('is-desktop-dock');
  const mount = isDesktop
    ? document.getElementById('workstationRight')
    : document.getElementById('screenCards');
  if (!mount) return;
  const wrap = document.createElement(isDesktop ? 'div' : 'details');
  wrap.className = 'stroke-canvas-panel';
  wrap.id = 'strokeCanvasWrap';
  if (!isDesktop) {
    const summary = document.createElement('summary');
    summary.textContent = 'Thứ tự nét & Luyện viết';
    wrap.appendChild(summary);
  } else {
    const title = document.createElement('div');
    title.className = 'sidebar-panel-header';
    title.innerHTML = `
      <div class="sidebar-panel-title">Thứ tự nét & Luyện viết</div>
      <span class="stroke-char-badge" id="strokeCharBadge"></span>
    `;
    wrap.appendChild(title);
  }
  const body = document.createElement('div');
  body.className = 'stroke-canvas-body';
  body.innerHTML = `
    <div class="stroke-canvas-grid" id="strokeCanvasTarget" title="Bấm vào ô để tự viết nét chữ"></div>
    <div class="stroke-canvas-fallback" id="strokeCanvasFallback" hidden></div>
    <div class="stroke-canvas-controls">
      <button type="button" class="stroke-ctrl-btn" id="strokeAnimateBtn">▶ Xem nét</button>
      <button type="button" class="stroke-ctrl-btn" id="strokeQuizBtn">✍️ Luyện viết</button>
    </div>
    <div class="stroke-quiz-hint" id="strokeQuizHint" hidden></div>
  `;
  wrap.appendChild(body);
  mount.appendChild(wrap);

  const target = wrap.querySelector('#strokeCanvasTarget');
  target.addEventListener('click', () => {
    if (strokeCanvasWriter) {
      quizStrokeCanvas();
    }
  });

  wrap.querySelector('#strokeAnimateBtn').addEventListener('click', (e) => {
    e.stopPropagation();
    animateStrokeCanvas();
  });
  wrap.querySelector('#strokeQuizBtn').addEventListener('click', (e) => {
    e.stopPropagation();
    quizStrokeCanvas();
  });

  onActiveWordChange(loadStrokeCanvasWord);
  loadStrokeCanvasWord(typeof activeStudyWord !== 'undefined' ? activeStudyWord : null);
}

document.addEventListener('DOMContentLoaded', initStrokeCanvas);
