// Guess-the-word (emoji) game: show an emoji, pick the matching Hanzi from 4 choices.
let guessWordBankData = null;
let guessWordOrder = [];
let guessWordIdx = 0;
let guessWordCurrentEntry = null;
let guessWordSolved = false;

async function ensureGuessWordBankLoaded() {
  if (guessWordBankData) return;
  const res = await fetch('database/vocabs/guess_word_bank.json');
  guessWordBankData = await res.json();
}

function shuffleGuessWordArray(arr) {
  const copy = arr.slice();
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

async function startGuessWordGame() {
  document.getElementById('guessWordOptions').innerHTML = '<div class="loading-text">Đang tải dữ liệu...</div>';

  await ensureGuessWordBankLoaded();
  guessWordOrder = shuffleGuessWordArray(Array.from({ length: guessWordBankData.length }, (_, i) => i));
  guessWordIdx = 0;
  loadNextGuessWordRound();
}

function loadNextGuessWordRound() {
  if (guessWordIdx >= guessWordOrder.length) {
    guessWordOrder = shuffleGuessWordArray(guessWordOrder);
    guessWordIdx = 0;
  }
  const entry = guessWordBankData[guessWordOrder[guessWordIdx]];
  guessWordCurrentEntry = entry;
  guessWordIdx++;
  guessWordSolved = false;

  const distractors = shuffleGuessWordArray(
    guessWordBankData.filter(w => w.hanzi !== entry.hanzi)
  ).slice(0, 3);
  const options = shuffleGuessWordArray([entry, ...distractors]);

  document.getElementById('guessWordEmoji').textContent = entry.emoji;
  document.getElementById('guessWordFeedback').textContent = '';
  document.getElementById('guessWordFeedback').className = 'guess-word-feedback';
  document.getElementById('guessWordNextBtn').hidden = true;
  document.getElementById('guessWordOptions').innerHTML = options.map(opt => `
    <button class="guess-word-option" type="button" onclick="pickGuessWordOption('${opt.hanzi}')">${opt.hanzi}</button>
  `).join('');
}

function pickGuessWordOption(hanzi) {
  if (guessWordSolved) return;
  const entry = guessWordCurrentEntry;
  const feedbackEl = document.getElementById('guessWordFeedback');
  const isCorrect = hanzi === entry.hanzi;

  if (isCorrect) {
    guessWordSolved = true;
    feedbackEl.textContent = `✓ ${entry.hanzi} (${entry.pinyin}) — ${entry.meaning}`;
    feedbackEl.className = 'guess-word-feedback correct';
    document.getElementById('guessWordNextBtn').hidden = false;
    document.querySelectorAll('.guess-word-option').forEach(btn => {
      btn.disabled = true;
      if (btn.textContent === entry.hanzi) btn.classList.add('correct');
    });
  } else {
    feedbackEl.textContent = '✗ Chưa đúng, thử lại nhé.';
    feedbackEl.className = 'guess-word-feedback incorrect';
    document.querySelectorAll('.guess-word-option').forEach(btn => {
      if (btn.textContent === hanzi) btn.classList.add('incorrect');
    });
  }
}
