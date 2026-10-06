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

function buildSpeedQuizRound(sentence) {
  const blankIdx = 1 + Math.floor(Math.random() * (sentence.zh_tokens.length - 1));
  const answer = sentence.zh_tokens[blankIdx];
  const displayTokens = sentence.zh_tokens.slice();
  // Match the visible gap to the answer length so a one-character particle such as 了
  // does not look like a missing two-character word.
  displayTokens[blankIdx] = '＿'.repeat(Math.max(1, Array.from(String(answer)).length));
  return { sentence, answer, sentenceText: displayTokens.join('') };
}

function loadNextSpeedQuizRound() {
  clearInterval(speedQuizTimerId);
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
  feedbackEl.textContent = `⏱ Hết giờ! Đáp án: ${round.answer}`;
  feedbackEl.className = 'speed-quiz-feedback incorrect';
  document.getElementById('speedQuizNextBtn').hidden = false;
  document.querySelectorAll('.speed-quiz-option').forEach(btn => {
    btn.disabled = true;
    if (btn.textContent === round.answer) btn.classList.add('correct');
  });
  updateSpeedQuizScoreboard();
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
    feedbackEl.textContent = `✓ ${round.sentence.zh_tokens.join('')} — ${round.sentence.meaning}`;
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
  } else {
    speedQuizStreak = 0;
    feedbackEl.textContent = '✗ Sai rồi, chọn lại nhé.';
    feedbackEl.className = 'speed-quiz-feedback incorrect';
    document.querySelectorAll('.speed-quiz-option').forEach(btn => {
      if (btn.textContent === word) btn.classList.add('incorrect');
    });
    updateSpeedQuizScoreboard();
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
