// Right sidebar: Multi-character Hanzi Writer stroke-order canvas with side-by-side grids,
// sequential auto-advancing quiz mode, and instructional text.
let currentStrokeWord = null;
let currentStrokeChars = [];
let strokeWriters = [];
let activeCharIndex = 0;
let isAnimatingSequential = false;

function extractHanziCharacters(text) {
  if (!text || typeof text !== 'string') return [];
  // Match CJK Unified Ideographs and extension blocks
  const chars = Array.from(text).filter(ch => /\p{Script=Han}/u.test(ch));
  if (chars.length > 0) return chars;
  // Fallback if no script=Han matched
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

function getGridBoxSize(totalChars) {
  const container = document.getElementById('strokeGridsContainer');
  const availableWidth = (container && container.clientWidth > 100) ? container.clientWidth : 300;
  if (totalChars <= 1) {
    return Math.min(176, Math.max(120, Math.floor(availableWidth * 0.72)));
  }
  if (totalChars === 2) {
    return Math.min(142, Math.max(100, Math.floor((availableWidth - 12) / 2)));
  }
  if (totalChars === 3) {
    return Math.min(94, Math.max(76, Math.floor((availableWidth - 16) / 3)));
  }
  return Math.min(136, Math.max(90, Math.floor((availableWidth - 12) / 2)));
}

function destroyStrokeCanvasWriters() {
  strokeWriters.forEach(writer => {
    if (writer) {
      try {
        if (typeof writer.cancelQuiz === 'function') writer.cancelQuiz();
      } catch (e) {}
    }
  });
  strokeWriters = [];
  isAnimatingSequential = false;

  const container = document.getElementById('strokeGridsContainer');
  if (container) container.innerHTML = '';

  const statusWrap = document.getElementById('strokeQuizStatusWrap');
  if (statusWrap) {
    statusWrap.hidden = true;
    statusWrap.innerHTML = '';
  }

  const animateBtn = document.getElementById('strokeAnimateBtn');
  const quizBtn = document.getElementById('strokeQuizBtn');
  if (animateBtn) animateBtn.classList.remove('active');
  if (quizBtn) quizBtn.classList.remove('active');
}

function renderInstructionText(highlightIndex = null) {
  const box = document.getElementById('strokeInstructionBox');
  if (!box) return;

  const total = currentStrokeChars.length;
  if (total === 0) {
    box.hidden = true;
    return;
  }
  box.hidden = false;

  if (total <= 1) {
    box.innerHTML = `
      <div class="stroke-instruction-prompt">
        <span class="stroke-instruction-icon">💡</span>
        <span>Bấm trực tiếp vào ô chữ để tự luyện viết!</span>
      </div>
    `;
    return;
  }

  // Multi-character sequence e.g. 作 -> 者
  const seqHtml = currentStrokeChars.map((ch, idx) => {
    const isCompleted = document.getElementById(`strokeGridCheck_${idx}`) && !document.getElementById(`strokeGridCheck_${idx}`).hidden;
    const isCurrent = highlightIndex === idx;
    let cls = 'stroke-seq-chip';
    if (isCompleted) cls += ' is-done';
    if (isCurrent) cls += ' is-current';
    return `<span class="${cls}">${isCompleted ? '✓ ' : ''}${ch}</span>`;
  }).join('<span class="stroke-seq-arrow">→</span>');

  box.innerHTML = `
    <div class="stroke-instruction-prompt">
      <span class="stroke-instruction-icon">💡</span>
      <span>Bấm trực tiếp vào các ô chữ để tự luyện viết!</span>
    </div>
    <div class="stroke-instruction-order">
      <span class="stroke-order-label">Luyện viết theo thứ tự:</span>
      <div class="stroke-order-seq">${seqHtml}</div>
    </div>
  `;
}

function renderStrokeGrids(autoAnimate = true) {
  const container = document.getElementById('strokeGridsContainer');
  const fallback = document.getElementById('strokeCanvasFallback');
  if (!container || !fallback) return;

  destroyStrokeCanvasWriters();
  fallback.hidden = true;

  const totalChars = currentStrokeChars.length;
  if (totalChars === 0) {
    fallback.hidden = false;
    fallback.textContent = 'Từ này không có chữ Hán để luyện viết.';
    renderInstructionText();
    syncStrokeCanvasControls();
    return;
  }

  if (typeof HanziWriter === 'undefined') {
    fallback.hidden = false;
    fallback.textContent = 'Không thể tải thư viện viết chữ (HanziWriter).';
    renderInstructionText();
    syncStrokeCanvasControls();
    return;
  }

  const boxSize = getGridBoxSize(totalChars);
  container.className = `stroke-grids-container chars-${Math.min(totalChars, 4)}`;
  container.style.setProperty('--grid-box-size', `${boxSize}px`);

  // Build grid containers for each character
  currentStrokeChars.forEach((ch, idx) => {
    const wrapper = document.createElement('div');
    wrapper.className = 'stroke-grid-wrapper' + (idx === 0 ? ' is-active' : '');
    wrapper.id = `strokeGridWrapper_${idx}`;
    wrapper.innerHTML = `
      <div class="stroke-canvas-grid" id="strokeCanvasTarget_${idx}" data-char-index="${idx}" title="Bấm vào ô để tự luyện viết chữ '${ch}'"></div>
      <div class="stroke-grid-footer">
        <span class="stroke-grid-num">${idx + 1}.</span>
        <span class="stroke-grid-char">${ch}</span>
        <span class="stroke-grid-check" id="strokeGridCheck_${idx}" hidden>✓</span>
      </div>
    `;
    container.appendChild(wrapper);

    // Clicking directly on any grid triggers quiz mode for that character
    const target = wrapper.querySelector('.stroke-canvas-grid');
    target.addEventListener('click', (e) => {
      e.stopPropagation();
      startQuizOnChar(idx, true);
    });
  });

  const colors = getStrokeColors();
  const padding = Math.max(6, Math.round(boxSize * 0.06));

  // Initialize HanziWriter for every character grid
  currentStrokeChars.forEach((ch, idx) => {
    try {
      const writer = HanziWriter.create(`strokeCanvasTarget_${idx}`, ch, {
        width: boxSize,
        height: boxSize,
        padding,
        showOutline: true,
        strokeColor: colors.strokeColor,
        radicalColor: colors.radicalColor,
        outlineColor: colors.outlineColor,
        showHintAfterMisses: 2,
        highlightOnComplete: true,
        onLoadCharDataError: function() {
          const wrap = document.getElementById(`strokeGridWrapper_${idx}`);
          if (wrap) {
            wrap.classList.add('has-error');
            const target = wrap.querySelector('.stroke-canvas-grid');
            if (target && !target.querySelector('svg')) {
              target.innerHTML = `<span style="font-size:${Math.round(boxSize * 0.45)}px; font-weight:700; color:var(--text-primary);">${ch}</span>`;
            }
          }
        }
      });
      strokeWriters[idx] = writer;
    } catch (err) {
      console.warn('HanziWriter init error for character', ch, err);
    }
  });

  renderInstructionText();
  syncStrokeCanvasControls();

  if (autoAnimate) {
    animateStrokeCanvas();
  }
}

function startQuizOnChar(charIndex, isManual = false) {
  if (!currentStrokeChars || charIndex < 0 || charIndex >= currentStrokeChars.length) return;
  const writer = strokeWriters[charIndex];
  if (!writer) return;

  // Cancel any running quiz or animation on other characters
  strokeWriters.forEach((w, idx) => {
    if (idx !== charIndex && w && typeof w.cancelQuiz === 'function') {
      try { w.cancelQuiz(); } catch (e) {}
    }
  });
  isAnimatingSequential = false;

  activeCharIndex = charIndex;

  // Update visual state of all grids
  currentStrokeChars.forEach((ch, idx) => {
    const wrap = document.getElementById(`strokeGridWrapper_${idx}`);
    const target = document.getElementById(`strokeCanvasTarget_${idx}`);
    if (wrap) wrap.classList.toggle('is-active', idx === charIndex);
    if (target) target.classList.toggle('is-quiz-mode', idx === charIndex);
  });

  const quizBtn = document.getElementById('strokeQuizBtn');
  const animateBtn = document.getElementById('strokeAnimateBtn');
  if (quizBtn) quizBtn.classList.add('active');
  if (animateBtn) animateBtn.classList.remove('active');

  const currentChar = currentStrokeChars[charIndex];
  const total = currentStrokeChars.length;

  renderInstructionText(charIndex);

  const statusWrap = document.getElementById('strokeQuizStatusWrap');
  if (statusWrap) {
    statusWrap.hidden = false;
    statusWrap.innerHTML = `
      <div class="stroke-status-live">
        ✍️ Hãy vẽ nét chữ <strong>"${currentChar}"</strong> (${charIndex + 1}/${total}) vào ô bên trên!
      </div>
    `;
  }

  writer.quiz({
    onMistake: () => {
      const statusEl = document.querySelector('.stroke-status-live');
      if (statusEl) {
        statusEl.innerHTML = `<span style="color:var(--danger-text)">Nét chưa chuẩn ở chữ "${currentChar}". Hãy thử lại theo đường mờ!</span>`;
      }
    },
    onCorrectStroke: (strokeData) => {
      const statusEl = document.querySelector('.stroke-status-live');
      if (statusEl) {
        statusEl.innerHTML = `<span style="color:var(--success-text)">Đúng nét ${strokeData.strokeNum + 1} của chữ "${currentChar}"! Tiếp tục nào…</span>`;
      }
    },
    onComplete: (summary) => {
      const mistakes = summary ? (summary.totalMistakes || 0) : 0;
      const mistakesText = mistakes === 0 ? 'hoàn hảo' : `${mistakes} lỗi sai`;

      // Mark this character completed
      const checkEl = document.getElementById(`strokeGridCheck_${charIndex}`);
      if (checkEl) checkEl.hidden = false;
      const wrap = document.getElementById(`strokeGridWrapper_${charIndex}`);
      if (wrap) wrap.classList.add('is-completed');
      const target = document.getElementById(`strokeCanvasTarget_${charIndex}`);
      if (target) target.classList.remove('is-quiz-mode');

      renderInstructionText(charIndex);

      if (charIndex < total - 1) {
        // AUTOMATICALLY ADVANCE TO NEXT CHARACTER GRID!
        const nextChar = currentStrokeChars[charIndex + 1];
        if (statusWrap) {
          statusWrap.innerHTML = `
            <div class="stroke-status-next">
              🎉 Xong chữ <strong>"${currentChar}"</strong> (${mistakesText})! Đang chuyển sang chữ <strong>"${nextChar}"</strong> (${charIndex + 2}/${total})…
            </div>
          `;
        }
        setTimeout(() => {
          startQuizOnChar(charIndex + 1, false);
        }, 600);
      } else {
        // ALL CHARACTERS COMPLETED!
        if (quizBtn) quizBtn.classList.remove('active');
        if (statusWrap) {
          const wordText = currentStrokeWord?.hanzi || currentStrokeChars.join('');
          statusWrap.innerHTML = `
            <div class="stroke-status-success">
              <div class="stroke-status-success-title">
                🎉 Xuất sắc! Bạn đã viết xong toàn bộ từ <strong>"${wordText}"</strong> (${total} chữ Hán)!
              </div>
              <button type="button" class="stroke-restart-btn" id="strokeRestartQuizBtn">
                ↺ Luyện viết lại từ đầu
              </button>
            </div>
          `;
          const restartBtn = document.getElementById('strokeRestartQuizBtn');
          if (restartBtn) {
            restartBtn.addEventListener('click', (e) => {
              e.stopPropagation();
              // Reset checkmarks and restart from char 0
              currentStrokeChars.forEach((ch, idx) => {
                const c = document.getElementById(`strokeGridCheck_${idx}`);
                if (c) c.hidden = true;
                const w = document.getElementById(`strokeGridWrapper_${idx}`);
                if (w) w.classList.remove('is-completed');
              });
              startQuizOnChar(0, true);
            });
          }
        }
      }
    }
  });
}

function animateStrokeCanvas() {
  if (!strokeWriters || strokeWriters.length === 0) return;

  // Cancel any running quiz
  strokeWriters.forEach(w => {
    if (w && typeof w.cancelQuiz === 'function') {
      try { w.cancelQuiz(); } catch (e) {}
    }
  });

  isAnimatingSequential = true;
  const animateBtn = document.getElementById('strokeAnimateBtn');
  const quizBtn = document.getElementById('strokeQuizBtn');
  if (animateBtn) animateBtn.classList.add('active');
  if (quizBtn) quizBtn.classList.remove('active');

  const statusWrap = document.getElementById('strokeQuizStatusWrap');
  if (statusWrap) {
    statusWrap.hidden = false;
    statusWrap.innerHTML = `
      <div class="stroke-status-live">
        ▶ Đang diễn họa thứ tự nét chữ…
      </div>
    `;
  }

  function playChar(idx) {
    if (!isAnimatingSequential) return;
    if (idx >= strokeWriters.length) {
      isAnimatingSequential = false;
      if (animateBtn) animateBtn.classList.remove('active');
      if (statusWrap) {
        statusWrap.innerHTML = `
          <div class="stroke-status-live">
            ✨ Đã diễn họa xong! Bấm trực tiếp vào các ô hoặc nhấn "Luyện viết" để thử viết.
          </div>
        `;
      }
      renderInstructionText();
      return;
    }

    const writer = strokeWriters[idx];
    const ch = currentStrokeChars[idx];
    currentStrokeChars.forEach((c, i) => {
      const wrap = document.getElementById(`strokeGridWrapper_${i}`);
      if (wrap) wrap.classList.toggle('is-active', i === idx);
    });

    renderInstructionText(idx);

    if (statusWrap) {
      statusWrap.innerHTML = `
        <div class="stroke-status-live">
          ▶ Đang diễn họa nét chữ <strong>"${ch}"</strong> (${idx + 1}/${strokeWriters.length})…
        </div>
      `;
    }

    if (writer && typeof writer.animateCharacter === 'function') {
      writer.animateCharacter({
        onComplete: () => {
          if (isAnimatingSequential) {
            playChar(idx + 1);
          }
        }
      });
    } else {
      playChar(idx + 1);
    }
  }

  playChar(0);
}

function loadStrokeCanvasWord(word) {
  currentStrokeWord = word;
  const badge = document.getElementById('strokeCharBadge');
  const mobileBadge = document.getElementById('strokeMobileCharBadge');
  const fallback = document.getElementById('strokeCanvasFallback');

  if (!word || !word.hanzi) {
    destroyStrokeCanvasWriters();
    currentStrokeChars = [];
    activeCharIndex = 0;
    if (fallback) {
      fallback.hidden = false;
      fallback.textContent = 'Chọn một từ để xem thứ tự nét & luyện viết.';
    }
    if (badge) badge.textContent = '';
    if (mobileBadge) mobileBadge.textContent = '';
    renderInstructionText();
    syncStrokeCanvasControls();
    return;
  }

  currentStrokeChars = extractHanziCharacters(word.hanzi);
  activeCharIndex = 0;

  // Update header badges
  const total = currentStrokeChars.length;
  const badgeText = total > 1 ? `${word.hanzi} (${total} chữ Hán)` : word.hanzi;
  if (badge) badge.textContent = badgeText;
  if (mobileBadge) mobileBadge.textContent = badgeText;

  renderStrokeGrids(true);
}

function syncStrokeCanvasControls() {
  const hasWriters = strokeWriters.length > 0;
  ['strokeAnimateBtn', 'strokeQuizBtn'].forEach(id => {
    const button = document.getElementById(id);
    if (button) button.disabled = !hasWriters;
  });
}

function initStrokeCanvas() {
  const isDesktop = document.body.classList.contains('is-desktop-dock');
  const mount = isDesktop
    ? document.getElementById('workstationRight')
    : document.getElementById('screenCards');
  if (!mount) return;

  if (document.getElementById('strokeCanvasWrap')) return;

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
    <div class="stroke-grids-container" id="strokeGridsContainer"></div>
    <div class="stroke-canvas-fallback" id="strokeCanvasFallback" hidden></div>
    <div class="stroke-canvas-controls">
      <button type="button" class="stroke-ctrl-btn" id="strokeAnimateBtn">▶ Xem nét</button>
      <button type="button" class="stroke-ctrl-btn" id="strokeQuizBtn">✍️ Luyện viết</button>
    </div>
    <div class="stroke-instruction-box" id="strokeInstructionBox" hidden></div>
    <div class="stroke-quiz-status-wrap" id="strokeQuizStatusWrap" hidden></div>
  `;
  wrap.appendChild(body);
  mount.appendChild(wrap);

  wrap.querySelector('#strokeAnimateBtn').addEventListener('click', (e) => {
    e.stopPropagation();
    animateStrokeCanvas();
  });

  wrap.querySelector('#strokeQuizBtn').addEventListener('click', (e) => {
    e.stopPropagation();
    startQuizOnChar(0, true);
  });

  // Re-render when theme changes dynamically (dark/light)
  try {
    const themeObserver = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
          if (currentStrokeChars.length > 0) {
            renderStrokeGrids(false);
          }
          break;
        }
      }
    });
    themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  } catch (e) {}

  // Debounced resize handler to adjust grid sizes if panel width changes
  let resizeTimer = null;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      if (currentStrokeChars.length > 0) {
        const newSize = getGridBoxSize(currentStrokeChars.length);
        const container = document.getElementById('strokeGridsContainer');
        const oldSize = container ? parseInt(container.style.getPropertyValue('--grid-box-size') || '0', 10) : 0;
        if (Math.abs(newSize - oldSize) > 4) {
          renderStrokeGrids(false);
        }
      }
    }, 150);
  });

  onActiveWordChange(loadStrokeCanvasWord);
  loadStrokeCanvasWord(typeof activeStudyWord !== 'undefined' ? activeStudyWord : null);
}

// Global API exports for external callers & interactions
window.loadStrokeCanvasWord = loadStrokeCanvasWord;
window.selectStrokeChar = function(idx) { startQuizOnChar(idx, true); };
window.animateStrokeCanvas = animateStrokeCanvas;
window.quizStrokeCanvas = function() { startQuizOnChar(0, true); };

document.addEventListener('DOMContentLoaded', initStrokeCanvas);
