// Fill-in-the-blank quiz: a Chinese sentence is missing one word, pick the correct word before time runs out.
const SPEED_QUIZ_TIME_LIMIT = 8;
const SPEED_QUIZ_BASE_SCORE = 100;
const SPEED_QUIZ_STORAGE_KEY = 'hsk_speed_quiz_best';

let speedQuizBankData = null;
let speedQuizOrder = [];
let speedQuizIdx = 0;
let speedQuizCurrentRound = null;
let speedQuizSolved = false;
let speedQuizScore = 0;
let speedQuizStreak = 0;
let speedQuizBest = 0;
let speedQuizTimeLeft = SPEED_QUIZ_TIME_LIMIT;
let speedQuizTimerId = null;
let speedQuizRoundLimit = 0;

async function ensureSpeedQuizBankLoaded() {
  if (speedQuizBankData) return;
  const res = await fetch('database/vocabs/sentence_bank.json');
  speedQuizBankData = (await res.json()).filter(s => s.zh_tokens && s.zh_tokens.length >= 2);
}

function shuffleSpeedQuizArray(arr) {
  const copy = arr.slice();
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

async function startSpeedQuizGame(options = {}) {
  speedQuizRoundLimit = Number(options.roundLimit) > 0 ? Number(options.roundLimit) : 0;
  document.getElementById('speedQuizOptions').innerHTML = '<div class="loading-text">Đang tải dữ liệu...</div>';
  await ensureSpeedQuizBankLoaded();

  speedQuizOrder = shuffleSpeedQuizArray(Array.from({ length: speedQuizBankData.length }, (_, i) => i));
  speedQuizIdx = 0;
  speedQuizScore = 0;
  speedQuizStreak = 0;
  speedQuizBest = Number(localStorage.getItem(SPEED_QUIZ_STORAGE_KEY) || 0);
  updateSpeedQuizScoreboard();
  loadNextSpeedQuizRound();
}

function updateSpeedQuizScoreboard() {
  document.getElementById('speedQuizScore').textContent = `Điểm: ${speedQuizScore}`;
  document.getElementById('speedQuizStreak').textContent = speedQuizStreak > 1 ? `🔥 x${speedQuizStreak}` : '';
  document.getElementById('speedQuizBest').textContent = `Kỷ lục: ${speedQuizBest}`;
}

let speedQuizVocabMap = null;

async function ensureVocabMapLoaded() {
  if (speedQuizVocabMap && speedQuizVocabMap.size > 0) return speedQuizVocabMap;
  speedQuizVocabMap = new Map();

  if (window.sidebarSearchIndex && window.sidebarSearchIndex.length > 0) {
    for (const w of window.sidebarSearchIndex) {
      if (w.hanzi && !speedQuizVocabMap.has(w.hanzi)) {
        speedQuizVocabMap.set(w.hanzi, { pinyin: w.pinyin, meaning: w.meaning, level: w.level });
      }
    }
  }

  if (typeof buildSidebarSearchIndex === 'function') {
    try {
      const list = await buildSidebarSearchIndex();
      if (Array.isArray(list)) {
        for (const w of list) {
          if (w.hanzi && !speedQuizVocabMap.has(w.hanzi)) {
            speedQuizVocabMap.set(w.hanzi, { pinyin: w.pinyin, meaning: w.meaning, level: w.level });
          }
        }
      }
    } catch (_) {}
  }
  return speedQuizVocabMap;
}

function getWordInfoSync(hanzi) {
  if (!hanzi) return null;
  if (speedQuizVocabMap && speedQuizVocabMap.has(hanzi)) {
    return speedQuizVocabMap.get(hanzi);
  }
  if (window.sidebarSearchIndex) {
    const item = window.sidebarSearchIndex.find(w => w.hanzi === hanzi);
    if (item) return { pinyin: item.pinyin, meaning: item.meaning, level: item.level };
  }
  return null;
}

function escapeHtml(value) {
  return String(value == null ? '' : value).replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  }[c]));
}

function highlightInSentence(sentenceZh, answer) {
  if (!sentenceZh || !answer) return escapeHtml(sentenceZh || '');
  const escaped = escapeHtml(sentenceZh);
  const escAns = escapeHtml(answer);
  return escaped.replace(new RegExp(escAns, 'g'), `<mark class="sqe-highlight">${escAns}</mark>`);
}

function highlightInPinyin(sentencePy, answerPy) {
  if (!sentencePy) return '';
  const escaped = escapeHtml(sentencePy);
  if (!answerPy) return escaped;
  const escPy = escapeHtml(answerPy).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp(`\\b${escPy}\\b|${escPy}`, 'i');
  return escaped.replace(regex, match => `<mark class="sqe-highlight">${match}</mark>`);
}

async function renderSpeedQuizExplanation(round, userChoice, isCorrect, isTimeout) {
  const explanationEl = document.getElementById('speedQuizExplanation');
  if (!explanationEl) return;

  await ensureVocabMapLoaded();

  const sentence = round.sentence;
  const answer = round.answer;
  const answerInfo = getWordInfoSync(answer) || {};
  const answerPinyin = answerInfo.pinyin || (sentence.pinyin_tokens && sentence.pinyin_tokens[round.blankIdx]) || '';
  const answerMeaning = answerInfo.meaning || 'khớp nghĩa trong câu';

  const fullZh = sentence.sentence_zh || sentence.zh_tokens.join('');
  const fullPy = sentence.sentence_py || (sentence.pinyin_tokens ? sentence.pinyin_tokens.join(' ') : '');
  const grammarPoint = sentence.grammar_point || '';
  const options = round.options || [];

  const html = `
    <div class="sqe-card">
      <div class="sqe-top-bar">
        <div class="sqe-status-tag ${isCorrect ? 'sqe-tag-correct' : 'sqe-tag-incorrect'}">
          ${isCorrect ? '✓ Trả lời chính xác!' : isTimeout ? '⏱ Hết thời gian làm bài!' : '✗ Chưa chính xác!'}
        </div>
        <button type="button" class="sqe-audio-btn" onclick="speakSpeedQuizSentence()" title="Nghe câu hoàn chỉnh" aria-label="Nghe đọc câu hoàn chỉnh">
          <span class="sqe-speaker-icon" aria-hidden="true">🔊</span>
          <span>Nghe phát âm</span>
        </button>
      </div>

      <div class="sqe-sentence-box">
        <div class="sqe-sentence-zh">${highlightInSentence(fullZh, answer)}</div>
        ${fullPy ? `<div class="sqe-sentence-py">${highlightInPinyin(fullPy, answerPinyin)}</div>` : ''}
        <div class="sqe-sentence-vi">Dịch nghĩa: “${escapeHtml(sentence.meaning || '')}”</div>
      </div>

      <div class="sqe-reason-box">
        <span class="sqe-reason-badge">💡 Tại sao chọn "${escapeHtml(answer)}"?</span>
        <div class="sqe-reason-body">
          <p class="sqe-reason-point">
            • Vị trí chỗ trống cần từ <strong>${escapeHtml(answer)}</strong> ${answerPinyin ? `(<em>${escapeHtml(answerPinyin)}</em>)` : ''} mang nghĩa: <strong>${escapeHtml(answerMeaning)}</strong> để tạo thành câu hoàn chỉnh và chuẩn ngữ nghĩa.
          </p>
          ${grammarPoint ? `
            <p class="sqe-reason-grammar">
              • <strong>Cấu trúc ngữ pháp:</strong> ${escapeHtml(grammarPoint)}.
            </p>
          ` : ''}
        </div>
      </div>

      <div class="sqe-options-summary">
        <div class="sqe-options-summary-title">Tra cứu nghĩa 4 phương án:</div>
        <div class="sqe-options-list">
          ${options.map(opt => {
            const isAns = opt === answer;
            const isUserPick = opt === userChoice && !isAns;
            const optInfo = getWordInfoSync(opt) || {};
            const optPy = optInfo.pinyin || '';
            const optMean = optInfo.meaning || '—';
            return `
              <div class="sqe-opt-row ${isAns ? 'is-correct' : isUserPick ? 'is-wrong-pick' : ''}">
                <div class="sqe-opt-badge">${isAns ? '✓ Đúng' : isUserPick ? '✗ Bạn chọn' : '•'}</div>
                <div class="sqe-opt-word">
                  <strong class="sqe-opt-hanzi">${escapeHtml(opt)}</strong>
                  ${optPy ? `<span class="sqe-opt-pinyin">${escapeHtml(optPy)}</span>` : ''}
                </div>
                <div class="sqe-opt-meaning" title="${escapeHtml(optMean)}">${escapeHtml(optMean)}</div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    </div>
  `;

  explanationEl.innerHTML = html;
  explanationEl.hidden = false;
}

function speakSpeedQuizSentence() {
  if (!speedQuizCurrentRound || !speedQuizCurrentRound.sentence) return;
  const sentence = speedQuizCurrentRound.sentence;
  const text = sentence.sentence_zh || sentence.zh_tokens.join('');
  const btn = document.querySelector('.sqe-audio-btn');
  if (typeof speakText === 'function') {
    speakText(text, btn, typeof SPEECH_RATE !== 'undefined' ? SPEECH_RATE : 0.85);
  }
}
window.speakSpeedQuizSentence = speakSpeedQuizSentence;

function buildSpeedQuizRound(sentence) {
  const blankIdx = 1 + Math.floor(Math.random() * (sentence.zh_tokens.length - 1));
  const answer = sentence.zh_tokens[blankIdx];
  const displayTokens = sentence.zh_tokens.slice();
  // Match the visible gap to the answer length so a one-character particle such as 了
  // does not look like a missing two-character word.
  displayTokens[blankIdx] = '＿'.repeat(Math.max(1, Array.from(String(answer)).length));
  return { sentence, answer, blankIdx, sentenceText: displayTokens.join('') };
}

function loadNextSpeedQuizRound() {
  clearInterval(speedQuizTimerId);
  const explanationEl = document.getElementById('speedQuizExplanation');
  if (explanationEl) {
    explanationEl.hidden = true;
    explanationEl.innerHTML = '';
  }

  if (speedQuizRoundLimit && speedQuizIdx >= speedQuizRoundLimit) {
    document.getElementById('speedQuizWord').textContent = 'Hoàn thành thử thách!';
    document.getElementById('speedQuizMeaning').textContent = `Bạn đã trả lời ${speedQuizRoundLimit} câu trắc nghiệm.`;
    document.getElementById('speedQuizOptions').replaceChildren();
    document.getElementById('speedQuizFeedback').textContent = `Tổng điểm: ${speedQuizScore}`;
    document.getElementById('speedQuizFeedback').className = 'speed-quiz-feedback correct';
    document.getElementById('speedQuizNextBtn').hidden = true;
    speedQuizRoundLimit = 0;
    return;
  }
  if (speedQuizIdx >= speedQuizOrder.length) {
    speedQuizOrder = shuffleSpeedQuizArray(speedQuizOrder);
    speedQuizIdx = 0;
  }
  const sentence = speedQuizBankData[speedQuizOrder[speedQuizIdx]];
  speedQuizIdx++;
  const round = buildSpeedQuizRound(sentence);
  speedQuizCurrentRound = round;
  speedQuizSolved = false;
  speedQuizTimeLeft = SPEED_QUIZ_TIME_LIMIT;

  const distractorPool = shuffleSpeedQuizArray(
    speedQuizBankData.filter(s => s !== sentence).flatMap(s => s.zh_tokens)
  );
  const distractors = [];
  for (const tok of distractorPool) {
    if (tok === round.answer || distractors.includes(tok)) continue;
    distractors.push(tok);
    if (distractors.length === 3) break;
  }
  const options = shuffleSpeedQuizArray([round.answer, ...distractors]);
  round.options = options;

  document.getElementById('speedQuizWord').textContent = round.sentenceText;
  document.getElementById('speedQuizMeaning').textContent = sentence.meaning || '';
  document.getElementById('speedQuizFeedback').textContent = '';
  document.getElementById('speedQuizFeedback').className = 'speed-quiz-feedback';
  document.getElementById('speedQuizNextBtn').hidden = true;
  document.getElementById('speedQuizOptions').innerHTML = options.map(opt => `
    <button class="speed-quiz-option" type="button" onclick="pickSpeedQuizOption('${opt.replace(/'/g, "\\'")}')">${opt}</button>
  `).join('');

  updateSpeedQuizTimerBar();
  speedQuizTimerId = setInterval(() => {
    speedQuizTimeLeft -= 0.1;
    if (speedQuizTimeLeft <= 0) {
      speedQuizTimeLeft = 0;
      updateSpeedQuizTimerBar();
      handleSpeedQuizTimeout();
      return;
    }
    updateSpeedQuizTimerBar();
  }, 100);
}

function updateSpeedQuizTimerBar() {
  const pct = Math.max(0, (speedQuizTimeLeft / SPEED_QUIZ_TIME_LIMIT) * 100);
  const barEl = document.getElementById('speedQuizTimerBar');
  barEl.style.width = `${pct}%`;
  barEl.classList.toggle('low', pct <= 30);
}

function handleSpeedQuizTimeout() {
  if (speedQuizSolved) return;
  speedQuizSolved = true;
  clearInterval(speedQuizTimerId);
  speedQuizStreak = 0;
  const round = speedQuizCurrentRound;
  const feedbackEl = document.getElementById('speedQuizFeedback');
  feedbackEl.textContent = `⏱ Hết giờ! Đáp án đúng: ${round.answer}`;
  feedbackEl.className = 'speed-quiz-feedback incorrect';
  const nextBtn = document.getElementById('speedQuizNextBtn');
  if (nextBtn) {
    nextBtn.hidden = false;
    setTimeout(() => {
      try { nextBtn.focus(); } catch (_) {}
    }, 60);
  }
  document.querySelectorAll('.speed-quiz-option').forEach(btn => {
    btn.disabled = true;
    if (btn.textContent === round.answer) btn.classList.add('correct');
  });
  updateSpeedQuizScoreboard();
  renderSpeedQuizExplanation(round, null, false, true);
}

function pickSpeedQuizOption(word) {
  if (speedQuizSolved) return;
  const round = speedQuizCurrentRound;
  const feedbackEl = document.getElementById('speedQuizFeedback');
  const isCorrect = word === round.answer;

  if (isCorrect) {
    speedQuizSolved = true;
    clearInterval(speedQuizTimerId);
    speedQuizStreak++;
    const speedBonus = Math.round((speedQuizTimeLeft / SPEED_QUIZ_TIME_LIMIT) * SPEED_QUIZ_BASE_SCORE);
    const streakBonus = Math.min(speedQuizStreak - 1, 5) * 10;
    speedQuizScore += SPEED_QUIZ_BASE_SCORE / 2 + speedBonus + streakBonus;
    if (speedQuizScore > speedQuizBest) {
      speedQuizBest = speedQuizScore;
      localStorage.setItem(SPEED_QUIZ_STORAGE_KEY, String(speedQuizBest));
    }
    feedbackEl.textContent = `✓ Chính xác! Đáp án: ${round.answer}`;
    feedbackEl.className = 'speed-quiz-feedback correct';
    const nextBtn = document.getElementById('speedQuizNextBtn');
    if (nextBtn) {
      nextBtn.hidden = false;
      setTimeout(() => {
        try { nextBtn.focus(); } catch (_) {}
      }, 60);
    }
    document.querySelectorAll('.speed-quiz-option').forEach(btn => {
      btn.disabled = true;
      if (btn.textContent === round.answer) btn.classList.add('correct');
    });
    updateSpeedQuizScoreboard();
    renderSpeedQuizExplanation(round, word, true, false);
  } else {
    speedQuizSolved = true;
    clearInterval(speedQuizTimerId);
    speedQuizStreak = 0;
    feedbackEl.textContent = `✗ Chưa chính xác! Đáp án đúng: ${round.answer}`;
    feedbackEl.className = 'speed-quiz-feedback incorrect';
    const nextBtn = document.getElementById('speedQuizNextBtn');
    if (nextBtn) {
      nextBtn.hidden = false;
      setTimeout(() => {
        try { nextBtn.focus(); } catch (_) {}
      }, 60);
    }
    document.querySelectorAll('.speed-quiz-option').forEach(btn => {
      btn.disabled = true;
      if (btn.textContent === round.answer) btn.classList.add('correct');
      if (btn.textContent === word) btn.classList.add('incorrect');
    });
    updateSpeedQuizScoreboard();
    renderSpeedQuizExplanation(round, word, false, false);
  }
}

// Keyboard navigation for speed quiz game
document.addEventListener('keydown', (e) => {
  const screen = document.getElementById('screenSpeedQuiz');
  if (!screen || screen.style.display === 'none') return;

  const nextBtn = document.getElementById('speedQuizNextBtn');
  if (nextBtn && !nextBtn.hidden) {
    if (e.key === 'Enter' || e.key === ' ' || e.key === 'ArrowRight') {
      e.preventDefault();
      loadNextSpeedQuizRound();
      return;
    }
  }

  if (!speedQuizSolved && ['1', '2', '3', '4'].includes(e.key)) {
    const idx = parseInt(e.key, 10) - 1;
    const btns = document.querySelectorAll('.speed-quiz-option');
    if (btns[idx] && !btns[idx].disabled) {
      e.preventDefault();
      btns[idx].click();
    }
  }
});
