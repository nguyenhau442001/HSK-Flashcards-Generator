// Fast-review (speed quiz) mode: pool building, timer, grading, screen transitions.
const REVIEW_TONE_MARKS = {
  'ā':'a','á':'a','ǎ':'a','à':'a',
  'ē':'e','é':'e','ě':'e','è':'e',
  'ī':'i','í':'i','ǐ':'i','ì':'i',
  'ō':'o','ó':'o','ǒ':'o','ò':'o',
  'ū':'u','ú':'u','ǔ':'u','ù':'u',
  'ǖ':'v','ǘ':'v','ǚ':'v','ǜ':'v','ü':'v',
};

function stripTonePinyin(text) {
  return String(text || '')
    .toLowerCase()
    .split('')
    .map(ch => REVIEW_TONE_MARKS[ch] || ch)
    .join('')
    .replace(/\s+/g, ' ')
    .trim();
}

function pinyinLooseMatch(input, target) {
  return stripTonePinyin(input) === stripTonePinyin(target);
}

const REVIEW_RANGE_LEVELS = ['hsk1', 'hsk2', 'hsk3', 'hsk4', 'hsk5', 'hsk6'];

function updateReviewRangeLabel(sliderValue) {
  const n = Number(sliderValue);
  const levels = REVIEW_RANGE_LEVELS.slice(0, n);
  const totalWords = levels.reduce((sum, lvl) => sum + LEVELS[lvl].total, 0);
  document.getElementById('reviewRangeLabel').textContent =
    n === 1 ? 'HSK1' : `HSK1 – HSK${n}`;
  document.getElementById('reviewRangeCount').textContent = `${totalWords} từ`;
}

function buildReviewPool() {
  const pool = [];
  for (let i = 0; i < WORDS.length; i++) {
    if (progress[WORDS[i].id] !== 'known') pool.push(i);
  }
  for (let i = pool.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [pool[i], pool[j]] = [pool[j], pool[i]];
  }
  return pool;
}

function renderReviewStart() {
  document.getElementById('reviewSession').hidden = true;
  document.getElementById('reviewResult').hidden = true;
  const start = document.getElementById('reviewStart');
  start.hidden = false;

  const pool = buildReviewPool();
  reviewPool = pool;

  if (pool.length === 0) {
    start.innerHTML = `
      <div class="review-empty">
        <div class="review-empty-icon">🎉</div>
        <div class="review-empty-title">Bạn đã thuộc hết từ ở cấp độ này!</div>
        <div class="review-empty-msg">Không còn từ nào để ôn nhanh. Hãy học thêm từ mới hoặc chuyển cấp độ khác.</div>
      </div>`;
    return;
  }

  start.innerHTML = `
    <div class="review-intro">
      <div class="review-intro-icon">⚡</div>
      <div class="review-intro-title">Ôn nhanh</div>
      <ul class="review-rules">
        <li>Mỗi câu có <strong>20 giây</strong> để trả lời</li>
        <li>Bạn có <strong>3 mạng</strong> — trả lời sai hoặc hết giờ sẽ mất 1 mạng</li>
        <li>Gõ pinyin hoặc chọn đáp án đúng, xen kẽ ngẫu nhiên</li>
        <li><strong>${pool.length}</strong> từ chưa nhớ đang chờ ôn</li>
      </ul>
      <button class="review-start-btn" onclick="startReviewSession()">Bắt đầu</button>
    </div>`;
}

function startReviewSession() {
  reviewIndex = 0;
  reviewLives = 3;
  reviewScore = 0;
  reviewStreak = 0;
  reviewBestStreak = 0;
  document.getElementById('reviewStart').hidden = true;
  document.getElementById('reviewResult').hidden = true;
  document.getElementById('reviewSession').hidden = false;
  renderReviewQuestion();
}

function pickReviewQuestionType() {
  return Math.random() < 0.5 ? 'type' : 'choice';
}

function buildReviewChoices(correctWordIdx) {
  const correctPinyin = stripTonePinyin(WORDS[correctWordIdx].pinyin);
  const others = [];
  for (let i = 0; i < WORDS.length; i++) {
    if (i !== correctWordIdx && stripTonePinyin(WORDS[i].pinyin) !== correctPinyin) others.push(i);
  }
  for (let i = others.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [others[i], others[j]] = [others[j], others[i]];
  }
  const distractors = others.slice(0, 3);
  const choices = [correctWordIdx, ...distractors];
  for (let i = choices.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [choices[i], choices[j]] = [choices[j], choices[i]];
  }
  return choices;
}

function abandonReviewSession() {
  if (reviewTimer) { clearInterval(reviewTimer); reviewTimer = null; }
  reviewAnswered = true;
  reviewSessionLive = false;
}

function renderReviewQuestion() {
  if (reviewAnswered && !reviewSessionLive) return;
  reviewSessionLive = true;
  if (reviewTimer) { clearInterval(reviewTimer); reviewTimer = null; }
  if (reviewLives <= 0 || reviewIndex >= reviewPool.length) { endReviewSession(); return; }

  const wordIdx = reviewPool[reviewIndex];
  const word = WORDS[wordIdx];
  const type = pickReviewQuestionType();
  reviewCurrentQuestion = { wordIdx, type };
  reviewAnswered = false;
  reviewTimeLeft = 20;

  const livesHtml = '♥'.repeat(reviewLives) + '♡'.repeat(3 - reviewLives);
  const header = `
    <div class="review-header">
      <div class="review-lives" aria-label="${reviewLives} mạng còn lại">${livesHtml}</div>
      <div class="review-progress-text">${reviewIndex + 1} / ${reviewPool.length}</div>
    </div>
    <div class="review-timer-track"><div class="review-timer-fill" id="reviewTimerFill"></div></div>
    <div class="review-question-word">
      <div class="review-hanzi">${word.hanzi}</div>
      <div class="review-meaning">${word.meaning}</div>
    </div>`;

  let bodyHtml;
  if (type === 'type') {
    bodyHtml = `
      <div class="review-answer-area">
        <input type="text" id="reviewTypeInput" class="review-type-input"
          autocomplete="off" autocapitalize="off" spellcheck="false"
          placeholder="Gõ pinyin (không dấu)..."
          onkeydown="if(event.key==='Enter') submitReviewTypeAnswer()">
        <button class="review-submit-btn" onclick="submitReviewTypeAnswer()">Trả lời</button>
      </div>
      <div class="review-feedback" id="reviewFeedback"></div>`;
  } else {
    const choiceIdxs = buildReviewChoices(wordIdx);
    bodyHtml = `
      <div class="review-choices">
        ${choiceIdxs.map(i => `
          <button class="review-choice-btn" data-word-idx="${i}" onclick="submitReviewChoice(${i})">
            ${WORDS[i].pinyin}
          </button>`).join('')}
      </div>
      <div class="review-feedback" id="reviewFeedback"></div>`;
  }

  document.getElementById('reviewSession').innerHTML = header + bodyHtml;

  const input = document.getElementById('reviewTypeInput');
  if (input) input.focus();

  reviewTimer = setInterval(reviewTick, 1000);
  updateReviewTimerBar();
}

function updateReviewTimerBar() {
  const fill = document.getElementById('reviewTimerFill');
  if (!fill) return;
  const pct = Math.max(0, (reviewTimeLeft / 20) * 100);
  fill.style.width = pct + '%';
  fill.classList.toggle('review-timer-low', reviewTimeLeft <= 5);
}

function reviewTick() {
  reviewTimeLeft -= 1;
  updateReviewTimerBar();
  if (reviewTimeLeft <= 0) {
    clearInterval(reviewTimer);
    reviewTimer = null;
    gradeReviewAnswer(false);
  }
}

function submitReviewTypeAnswer() {
  if (reviewAnswered) return;
  const input = document.getElementById('reviewTypeInput');
  const word = WORDS[reviewCurrentQuestion.wordIdx];
  const isCorrect = pinyinLooseMatch(input.value, word.pinyin);
  gradeReviewAnswer(isCorrect);
}

function submitReviewChoice(chosenIdx) {
  if (reviewAnswered) return;
  const isCorrect = chosenIdx === reviewCurrentQuestion.wordIdx;
  gradeReviewAnswer(isCorrect);
}

function gradeReviewAnswer(isCorrect) {
  if (reviewAnswered) return;
  reviewAnswered = true;
  if (reviewTimer) { clearInterval(reviewTimer); reviewTimer = null; }

  const wordIdx = reviewCurrentQuestion.wordIdx;
  const word = WORDS[wordIdx];
  progress[word.id] = isCorrect ? 'known' : 'unknown';
  saveProgress();
  recordDailyStudy(word.id);
  checkCelebration();

  if (isCorrect) {
    reviewScore += 1;
    reviewStreak += 1;
    if (reviewStreak > reviewBestStreak) reviewBestStreak = reviewStreak;
  } else {
    reviewLives -= 1;
    reviewStreak = 0;
  }

  const feedback = document.getElementById('reviewFeedback');
  if (feedback) {
    feedback.textContent = isCorrect ? 'Chính xác!' : `Sai rồi. Đáp án: ${word.pinyin}`;
    feedback.className = 'review-feedback show ' + (isCorrect ? 'review-feedback--correct' : 'review-feedback--wrong');
  }
  document.querySelectorAll('.review-choice-btn').forEach(btn => {
    btn.disabled = true;
    if (Number(btn.dataset.wordIdx) === wordIdx) btn.classList.add('review-choice-btn--correct');
  });

  setTimeout(() => {
    reviewIndex += 1;
    renderReviewQuestion();
  }, 900);
}

function endReviewSession() {
  if (reviewTimer) { clearInterval(reviewTimer); reviewTimer = null; }
  document.getElementById('reviewSession').hidden = true;
  renderReviewResult();
}

function renderReviewResult() {
  const result = document.getElementById('reviewResult');
  result.hidden = false;
  const total = Math.min(reviewIndex, reviewPool.length);
  const survived = reviewLives > 0;

  result.innerHTML = `
    <div class="review-result">
      <div class="review-result-icon">${survived ? '🏁' : '💔'}</div>
      <div class="review-result-title">${survived ? 'Hoàn thành!' : 'Hết mạng!'}</div>
      <div class="review-result-stats">
        <div class="review-result-stat">
          <div class="review-result-num">${reviewScore}</div>
          <div class="review-result-lbl">câu đúng</div>
        </div>
        <div class="review-result-stat">
          <div class="review-result-num">${total}</div>
          <div class="review-result-lbl">tổng số câu</div>
        </div>
        <div class="review-result-stat">
          <div class="review-result-num">${reviewBestStreak}</div>
          <div class="review-result-lbl">chuỗi đúng dài nhất</div>
        </div>
      </div>
      <div class="review-result-actions">
        <button class="review-again-btn" onclick="renderReviewStart()">Chơi lại</button>
        <button class="review-back-btn" onclick="setViewMode('cards')">Về flashcard</button>
      </div>
    </div>`;
}
