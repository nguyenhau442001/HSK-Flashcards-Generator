// Sentence-ordering game: drag/tap words from database/vocabs/sentence_bank.json into the right order.
let sentenceBankData = null;
let sentenceGameOrder = [];
let sentenceGameIdx = 0;
let sentenceGameSlots = [];
let sentenceGameBankTokens = [];
let sentenceGameSolved = false;
let sentenceGameCurrentEntry = null;

async function ensureSentenceBankLoaded() {
  if (sentenceBankData) return;
  const res = await fetch('database/vocabs/sentence_bank.json');
  sentenceBankData = await res.json();
}

function shuffleSentenceGameArray(arr) {
  const copy = arr.slice();
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

async function startSentenceGame() {
  document.getElementById('sentenceGameBank').innerHTML = '<div class="loading-text">Đang tải dữ liệu...</div>';

  await ensureSentenceBankLoaded();
  sentenceGameOrder = shuffleSentenceGameArray(Array.from({ length: sentenceBankData.length }, (_, i) => i));
  sentenceGameIdx = 0;
  loadNextSentenceGameRound();
}

function loadNextSentenceGameRound() {
  if (sentenceGameIdx >= sentenceGameOrder.length) {
    sentenceGameOrder = shuffleSentenceGameArray(sentenceGameOrder);
    sentenceGameIdx = 0;
  }
  const entry = sentenceBankData[sentenceGameOrder[sentenceGameIdx]];
  sentenceGameCurrentEntry = entry;
  sentenceGameIdx++;
  sentenceGameSolved = false;
  sentenceGameSlots = [];
  sentenceGameBankTokens = shuffleSentenceGameArray(entry.zh_tokens.map((tok, i) => ({ tok, i })));

  document.getElementById('sentenceGameMeaning').textContent = entry.meaning;
  document.getElementById('sentenceGameFeedback').textContent = '';
  document.getElementById('sentenceGameFeedback').className = 'sentence-game-feedback';
  document.getElementById('sentenceGameNextBtn').hidden = true;
  document.getElementById('sentenceGameCheckBtn').hidden = false;
  renderSentenceGameBoard();
}

function renderSentenceGameBoard() {
  const entry = sentenceGameCurrentEntry;
  const slotsEl = document.getElementById('sentenceGameSlots');
  const bankEl = document.getElementById('sentenceGameBank');

  slotsEl.innerHTML = entry.zh_tokens.map((_, slotIdx) => {
    const filled = sentenceGameSlots[slotIdx];
    if (filled === undefined) return '<button class="sentence-slot empty" type="button" disabled></button>';
    const tok = entry.zh_tokens[filled];
    return `<button class="sentence-slot filled" type="button" onclick="removeSentenceGameSlot(${slotIdx})">${tok}</button>`;
  }).join('');

  const usedIndices = new Set(sentenceGameSlots);
  bankEl.innerHTML = sentenceGameBankTokens
    .filter(item => !usedIndices.has(item.i))
    .map(item => `<button class="sentence-chip" type="button" onclick="pickSentenceGameToken(${item.i})">${item.tok}</button>`)
    .join('');
}

function pickSentenceGameToken(tokenIdx) {
  if (sentenceGameSolved) return;
  const entry = sentenceGameCurrentEntry;
  const nextEmptySlot = sentenceGameSlots.length;
  if (nextEmptySlot >= entry.zh_tokens.length) return;
  sentenceGameSlots.push(tokenIdx);
  renderSentenceGameBoard();
}

function removeSentenceGameSlot(slotIdx) {
  if (sentenceGameSolved) return;
  if (slotIdx >= sentenceGameSlots.length) return;
  sentenceGameSlots = sentenceGameSlots.slice(0, slotIdx);
  renderSentenceGameBoard();
}

function checkSentenceGameAnswer() {
  const entry = sentenceGameCurrentEntry;
  const feedbackEl = document.getElementById('sentenceGameFeedback');
  if (sentenceGameSlots.length !== entry.zh_tokens.length) {
    feedbackEl.textContent = 'Hãy xếp đủ các từ trước khi kiểm tra.';
    feedbackEl.className = 'sentence-game-feedback';
    return;
  }
  const isCorrect = sentenceGameSlots.every((tokenIdx, slotIdx) => tokenIdx === slotIdx);
  if (isCorrect) {
    sentenceGameSolved = true;
    feedbackEl.textContent = `✓ Đúng rồi! ${entry.pinyin_tokens.join(' ')}`;
    feedbackEl.className = 'sentence-game-feedback correct';
    document.getElementById('sentenceGameCheckBtn').hidden = true;
    document.getElementById('sentenceGameNextBtn').hidden = false;
  } else {
    feedbackEl.textContent = '✗ Chưa đúng, thử lại nhé.';
    feedbackEl.className = 'sentence-game-feedback incorrect';
  }
}
