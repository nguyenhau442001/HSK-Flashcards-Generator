// Right sidebar: Hanzi Writer stroke-order canvas with animate + quiz mode.
let strokeCanvasWriter = null;

function destroyStrokeCanvasWriter() {
  const el = document.getElementById('strokeCanvasTarget');
  if (el) el.innerHTML = '';
  strokeCanvasWriter = null;
}

function loadStrokeCanvasWord(word) {
  const target = document.getElementById('strokeCanvasTarget');
  const fallback = document.getElementById('strokeCanvasFallback');
  if (!target || !fallback) return;
  destroyStrokeCanvasWriter();
  fallback.hidden = true;

  if (!word || !word.hanzi || typeof HanziWriter === 'undefined') {
    fallback.hidden = false;
    fallback.textContent = !word ? 'Chọn một từ để xem thứ tự nét.' : 'Không thể tải thư viện viết chữ.';
    return;
  }

  const thisChar = word.hanzi[0]; // canvas shows first character of multi-char words
  try {
    strokeCanvasWriter = HanziWriter.create('strokeCanvasTarget', thisChar, {
      width: 200,
      height: 200,
      padding: 10,
      showOutline: true,
      strokeColor: '#2b2926',
    });
  } catch (e) {
    fallback.hidden = false;
    fallback.textContent = 'Không thể tải nét chữ cho ký tự này (mất kết nối mạng hoặc ký tự chưa được hỗ trợ).';
  }
}

function animateStrokeCanvas() {
  if (strokeCanvasWriter) strokeCanvasWriter.animateCharacter();
}

function quizStrokeCanvas() {
  if (strokeCanvasWriter) strokeCanvasWriter.quiz();
}

function initStrokeCanvas() {
  const isDesktop = document.body.classList.contains('is-desktop-dock');
  const mount = isDesktop
    ? document.getElementById('workstationRight')
    : document.getElementById('screenCards');
  if (!mount) return;
  const wrap = document.createElement(isDesktop ? 'div' : 'details');
  wrap.className = 'stroke-canvas-panel';
  if (!isDesktop) {
    const summary = document.createElement('summary');
    summary.textContent = 'Thứ tự nét';
    wrap.appendChild(summary);
  } else {
    const title = document.createElement('div');
    title.className = 'sidebar-panel-title';
    title.textContent = 'Thứ tự nét';
    wrap.appendChild(title);
  }
  const body = document.createElement('div');
  body.innerHTML = `
    <div class="stroke-canvas-grid" id="strokeCanvasTarget"></div>
    <div class="stroke-canvas-fallback" id="strokeCanvasFallback" hidden></div>
    <div class="stroke-canvas-controls">
      <button type="button" class="icon-btn" id="strokeAnimateBtn">▶ Xem thứ tự nét</button>
      <button type="button" class="icon-btn" id="strokeQuizBtn">✍️ Luyện viết</button>
    </div>
  `;
  wrap.appendChild(body);
  mount.appendChild(wrap);

  wrap.querySelector('#strokeAnimateBtn').addEventListener('click', animateStrokeCanvas);
  wrap.querySelector('#strokeQuizBtn').addEventListener('click', quizStrokeCanvas);

  onActiveWordChange(loadStrokeCanvasWord);
  loadStrokeCanvasWord(typeof activeStudyWord !== 'undefined' ? activeStudyWord : null);
}

document.addEventListener('DOMContentLoaded', initStrokeCanvas);
