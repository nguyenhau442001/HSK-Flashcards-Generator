// Right sidebar: Hanzi Writer stroke-order canvas with multi-character support, animate + quiz mode.
let currentStrokeWord = null;
let currentStrokeChars = [];
let activeCharIndex = 0;
let strokeCanvasWriter = null;
let currentStrokeChar = '';

function extractHanziCharacters(text) {
  if (!text || typeof text !== 'string') return [];
  // Match CJK Unified Ideographs and extension blocks
  const chars = Array.from(text).filter(ch => /\p{Script=Han}/u.test(ch));
  if (chars.length > 0) return chars;
  // Fallback if no script=Han matched (e.g. edge cases)
  return Array.from(text).filter(ch => ch.trim().length > 0 && !/[\s\p{P}]/u.test(ch));
}

function getStrokeColors() {
  const isDark = document.documentElement.dataset.theme === 'dark' ||
    (!document.documentElement.dataset.theme && window.matchMedia('(prefers-color-scheme: dark)').matches);
  return {
    strokeColor: isDark ? '#f1f0f2' : '#2b2926',
    radicalColor: isDark ? '#e07860' : '#c2654a',
    outlineColor: isDark ? '#3d3c45' : '#e4e4e7',
  };
}

function destroyStrokeCanvasWriter() {
  const el = document.getElementById('strokeCanvasTarget');
  if (el) {
    el.innerHTML = '';
    el.classList.remove('is-quiz-mode');
  }
  if (strokeCanvasWriter) {
    try {
      if (typeof strokeCanvasWriter.cancelQuiz === 'function') {
        strokeCanvasWriter.cancelQuiz();
      }
    } catch (e) {}
    strokeCanvasWriter = null;
  }
  currentStrokeChar = '';
  const hint = document.getElementById('strokeQuizHint');
  if (hint) { hint.hidden = true; hint.innerHTML = ''; }
  const animateBtn = document.getElementById('strokeAnimateBtn');
  const quizBtn = document.getElementById('strokeQuizBtn');
  if (animateBtn) animateBtn.classList.remove('active');
  if (quizBtn) quizBtn.classList.remove('active');
}

function updateStrokeCharSelector() {
  const wrap = document.getElementById('strokeCharSelectorWrap');
  const tabsContainer = document.getElementById('strokeCharTabs');
  const prevBtn = document.getElementById('strokePrevCharBtn');
  const nextBtn = document.getElementById('strokeNextCharBtn');
  const badge = document.getElementById('strokeCharBadge');
  const mobileBadge = document.getElementById('strokeMobileCharBadge');

  const currentChar = currentStrokeChars[activeCharIndex] || '';
  const totalChars = currentStrokeChars.length;
  const wordHanzi = currentStrokeWord?.hanzi || currentChar;

  // Update badges
  if (totalChars > 1 && currentChar) {
    const badgeText = `${currentChar} (${activeCharIndex + 1}/${totalChars} từ ${wordHanzi})`;
    if (badge) badge.textContent = badgeText;
    if (mobileBadge) mobileBadge.textContent = `${currentChar} (${activeCharIndex + 1}/${totalChars})`;
  } else {
    if (badge) badge.textContent = currentChar;
    if (mobileBadge) mobileBadge.textContent = currentChar;
  }

  if (!wrap || !tabsContainer) return;

  // Single-character word or no characters: hide selector
  if (totalChars <= 1) {
    wrap.hidden = true;
    tabsContainer.innerHTML = '';
    return;
  }

  // Multi-character word: render selector tabs
  wrap.hidden = false;
  tabsContainer.innerHTML = '';

  currentStrokeChars.forEach((ch, idx) => {
    const tab = document.createElement('button');
    tab.type = 'button';
    tab.className = 'stroke-char-pill' + (idx === activeCharIndex ? ' active' : '');
    tab.setAttribute('role', 'tab');
    tab.setAttribute('aria-selected', idx === activeCharIndex ? 'true' : 'false');
    tab.setAttribute('title', `Xem & luyện viết chữ ${idx + 1}/${totalChars}: "${ch}"`);
    tab.innerHTML = `<span class="stroke-pill-index">${idx + 1}</span><span class="stroke-pill-char">${ch}</span>`;
    tab.addEventListener('click', (e) => {
      e.stopPropagation();
      if (idx !== activeCharIndex) {
        selectStrokeChar(idx, true);
      }
    });
    tabsContainer.appendChild(tab);
  });

  if (prevBtn) {
    prevBtn.disabled = activeCharIndex <= 0;
  }
  if (nextBtn) {
    nextBtn.disabled = activeCharIndex >= totalChars - 1;
  }
}

function selectStrokeChar(index, autoAnimate = true) {
  if (!currentStrokeChars || currentStrokeChars.length === 0) return;
  if (index < 0 || index >= currentStrokeChars.length) return;
  activeCharIndex = index;
  renderStrokeCharacter(currentStrokeChars[index], autoAnimate);
  updateStrokeCharSelector();
}

function renderStrokeCharacter(char, autoAnimate = true) {
  const target = document.getElementById('strokeCanvasTarget');
  const fallback = document.getElementById('strokeCanvasFallback');
  if (!target || !fallback) return;

  destroyStrokeCanvasWriter();
  fallback.hidden = true;

  if (!char || typeof HanziWriter === 'undefined') {
    fallback.hidden = false;
    fallback.textContent = typeof HanziWriter === 'undefined'
      ? 'Không thể tải thư viện viết chữ.'
      : 'Không có ký tự để hiển thị.';
    syncStrokeCanvasControls();
    return;
  }

  currentStrokeChar = char;
  const colors = getStrokeColors();
  const thisChar = char;

  try {
    strokeCanvasWriter = HanziWriter.create('strokeCanvasTarget', char, {
      width: 180,
      height: 180,
      padding: 10,
      showOutline: true,
      strokeColor: colors.strokeColor,
      radicalColor: colors.radicalColor,
      outlineColor: colors.outlineColor,
      showHintAfterMisses: 2,
      highlightOnComplete: true,
      onLoadCharDataError: function() {
        if (currentStrokeChar === thisChar && fallback) {
          fallback.hidden = false;
          fallback.textContent = `Chưa có dữ liệu nét chữ cho "${thisChar}".`;
        }
      }
    });

    if (autoAnimate) {
      const thisWriter = strokeCanvasWriter;
      strokeCanvasWriter.animateCharacter({
        onComplete: () => {
          if (strokeCanvasWriter !== thisWriter || currentStrokeChar !== thisChar) return;
          const hint = document.getElementById('strokeQuizHint');
          if (hint) {
            hint.hidden = false;
            const nextChar = activeCharIndex < currentStrokeChars.length - 1 ? currentStrokeChars[activeCharIndex + 1] : null;
            hint.innerHTML = `
              <span>💡 Bấm trực tiếp vào ô để tự luyện viết!</span>
              ${nextChar ? `<div class="stroke-hint-sub">Chữ tiếp theo: <strong>"${nextChar}"</strong> (${activeCharIndex + 2}/${currentStrokeChars.length})</div>` : ''}
            `;
          }
        }
      });
    }
  } catch (e) {
    fallback.hidden = false;
    fallback.textContent = `Không thể tải nét chữ cho "${char}".`;
  }
  syncStrokeCanvasControls();
}

function loadStrokeCanvasWord(word) {
  currentStrokeWord = word;
  const fallback = document.getElementById('strokeCanvasFallback');
  const badge = document.getElementById('strokeCharBadge');
  const mobileBadge = document.getElementById('strokeMobileCharBadge');

  if (!word || !word.hanzi) {
    destroyStrokeCanvasWriter();
    currentStrokeChars = [];
    activeCharIndex = 0;
    if (fallback) {
      fallback.hidden = false;
      fallback.textContent = 'Chọn một từ để xem thứ tự nét & luyện viết.';
    }
    if (badge) badge.textContent = '';
    if (mobileBadge) mobileBadge.textContent = '';
    updateStrokeCharSelector();
    syncStrokeCanvasControls();
    return;
  }

  currentStrokeChars = extractHanziCharacters(word.hanzi);
  activeCharIndex = 0;

  if (currentStrokeChars.length === 0) {
    destroyStrokeCanvasWriter();
    if (fallback) {
      fallback.hidden = false;
      fallback.textContent = 'Từ này không có chữ Hán để luyện viết.';
    }
    updateStrokeCharSelector();
    syncStrokeCanvasControls();
    return;
  }

  updateStrokeCharSelector();
  selectStrokeChar(0, true);
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
  try {
    if (typeof strokeCanvasWriter.cancelQuiz === 'function') {
      strokeCanvasWriter.cancelQuiz();
    }
  } catch (e) {}

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
  const thisWriter = strokeCanvasWriter;
  const thisChar = currentStrokeChar;
  strokeCanvasWriter.animateCharacter({
    onComplete: () => {
      if (strokeCanvasWriter !== thisWriter || currentStrokeChar !== thisChar) return;
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
    const progress = currentStrokeChars.length > 1 ? ` (${activeCharIndex + 1}/${currentStrokeChars.length})` : '';
    hint.textContent = `✍️ Hãy vẽ nét chữ "${currentStrokeChar}"${progress} vào ô bên trên!`;
  }
  const thisWriter = strokeCanvasWriter;
  const thisChar = currentStrokeChar;
  const thisIndex = activeCharIndex;

  strokeCanvasWriter.quiz({
    onMistake: () => {
      if (strokeCanvasWriter !== thisWriter || currentStrokeChar !== thisChar) return;
      if (hint) hint.textContent = 'Nét chưa chuẩn. Hãy thử lại theo đường mờ!';
    },
    onCorrectStroke: (strokeData) => {
      if (strokeCanvasWriter !== thisWriter || currentStrokeChar !== thisChar) return;
      if (hint) hint.textContent = `Đúng nét ${strokeData.strokeNum + 1}! Tiếp tục nào…`;
    },
    onComplete: (summary) => {
      if (strokeCanvasWriter !== thisWriter || currentStrokeChar !== thisChar) return;
      if (quizBtn) quizBtn.classList.remove('active');
      if (target) target.classList.remove('is-quiz-mode');
      if (!hint) return;
      hint.hidden = false;

      const mistakes = summary ? (summary.totalMistakes || 0) : 0;
      const mistakesText = mistakes === 0 ? 'hoàn hảo không lỗi nào' : `${mistakes} lỗi sai`;

      if (thisIndex < currentStrokeChars.length - 1) {
        const nextIdx = thisIndex + 1;
        const nextChar = currentStrokeChars[nextIdx];
        hint.innerHTML = `
          <div class="stroke-quiz-feedback">
            <div class="stroke-feedback-title">🎉 Tuyệt vời! Viết xong chữ <strong>"${thisChar}"</strong> (${mistakesText})!</div>
            <button type="button" class="stroke-advance-btn" id="strokeQuizAdvanceBtn">
              Viết tiếp chữ "${nextChar}" (${nextIdx + 1}/${currentStrokeChars.length}) ➔
            </button>
          </div>
        `;
        const advanceBtn = document.getElementById('strokeQuizAdvanceBtn');
        if (advanceBtn) {
          advanceBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            selectStrokeChar(nextIdx, false);
            quizStrokeCanvas();
          });
        }
      } else {
        const total = currentStrokeChars.length;
        hint.innerHTML = `
          <div class="stroke-quiz-feedback is-done">
            <div class="stroke-feedback-title">🎉 Xuất sắc! Bạn đã viết xong ${total > 1 ? `toàn bộ ${total} chữ của từ <strong>"${currentStrokeWord?.hanzi || thisChar}"</strong>` : `chữ <strong>"${thisChar}"</strong>`} (${mistakesText})!</div>
            ${total > 1 ? `
              <button type="button" class="stroke-advance-btn secondary" id="strokeQuizRestartBtn">
                ↺ Luyện viết lại từ đầu
              </button>
            ` : ''}
          </div>
        `;
        const restartBtn = document.getElementById('strokeQuizRestartBtn');
        if (restartBtn) {
          restartBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            selectStrokeChar(0, false);
            quizStrokeCanvas();
          });
        }
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
    summary.innerHTML = 'Thứ tự nét & Luyện viết <span class="stroke-char-badge" id="strokeMobileCharBadge"></span>';
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
    <div class="stroke-char-selector-wrap" id="strokeCharSelectorWrap" hidden>
      <div class="stroke-char-nav">
        <button type="button" class="stroke-char-arrow-btn" id="strokePrevCharBtn" title="Chữ trước đó" aria-label="Chữ trước đó">‹</button>
        <div class="stroke-char-tabs" id="strokeCharTabs" role="tablist" aria-label="Chọn chữ cần viết"></div>
        <button type="button" class="stroke-char-arrow-btn" id="strokeNextCharBtn" title="Chữ tiếp theo" aria-label="Chữ tiếp theo">›</button>
      </div>
    </div>
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

  const prevBtn = wrap.querySelector('#strokePrevCharBtn');
  if (prevBtn) {
    prevBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (activeCharIndex > 0) {
        selectStrokeChar(activeCharIndex - 1, true);
      }
    });
  }
  const nextBtn = wrap.querySelector('#strokeNextCharBtn');
  if (nextBtn) {
    nextBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (activeCharIndex < currentStrokeChars.length - 1) {
        selectStrokeChar(activeCharIndex + 1, true);
      }
    });
  }

  // Keyboard navigation when user is on or within stroke canvas panel
  wrap.addEventListener('keydown', (e) => {
    if (currentStrokeChars.length <= 1) return;
    if (e.key === 'ArrowRight' || e.key === 'PageDown') {
      if (activeCharIndex < currentStrokeChars.length - 1) {
        e.preventDefault();
        selectStrokeChar(activeCharIndex + 1, true);
      }
    } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
      if (activeCharIndex > 0) {
        e.preventDefault();
        selectStrokeChar(activeCharIndex - 1, true);
      }
    }
  });

  // Re-render when theme changes dynamically (dark/light)
  try {
    const themeObserver = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
          if (currentStrokeChar && strokeCanvasWriter) {
            renderStrokeCharacter(currentStrokeChar, false);
          }
          break;
        }
      }
    });
    themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  } catch (e) {}

  onActiveWordChange(loadStrokeCanvasWord);
  loadStrokeCanvasWord(typeof activeStudyWord !== 'undefined' ? activeStudyWord : null);
}

window.loadStrokeCanvasWord = loadStrokeCanvasWord;
window.selectStrokeChar = selectStrokeChar;
window.animateStrokeCanvas = animateStrokeCanvas;
window.quizStrokeCanvas = quizStrokeCanvas;

document.addEventListener('DOMContentLoaded', initStrokeCanvas);

