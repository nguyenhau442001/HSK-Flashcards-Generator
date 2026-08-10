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
  document.getElementById('reviewSession').hidden = false;
  document.getElementById('reviewSession').textContent = 'Phiên ôn tập sẽ được xây dựng ở bước tiếp theo.';
}
