// Cross-level review queue and the daily new-card limit.
function countNewReviewsToday() {
  const today = localDateKey(new Date());
  const reviewed = new Set();
  Object.keys(LEVELS).filter(level => LEVELS[level].available).forEach(level => {
    readSrsReviewLog(level).forEach(entry => {
      if (entry.stateBefore !== SRS.State.New || !entry.timestamp) return;
      const timestamp = new Date(entry.timestamp);
      if (!Number.isFinite(timestamp.getTime()) || localDateKey(timestamp) !== today) return;
      reviewed.add(level + ':' + entry.wordId);
    });
  });
  return reviewed.size;
}

function countDueCardsAcrossLevels(now) {
  const currentTime = (now || new Date()).getTime();
  return Object.keys(LEVELS).filter(level => LEVELS[level].available).reduce((count, level) => {
    const record = readSrsRecord(level);
    if (record) {
      return count + Object.values(record.cards).filter(card => SRS.isDue(card, currentTime)).length;
    }
    return count + Object.values(readSavedLevelProgressLegacy(level)).filter(status => status === 'unknown').length;
  }, 0);
}

async function loadTodayReviewQueue() {
  const now = new Date();
  const levels = Object.keys(LEVELS).filter(level => LEVELS[level].available);
  const datasets = await Promise.all(levels.map(async level => {
    const response = await fetch(LEVELS[level].dataUrl);
    if (!response.ok) throw new Error('Không tải được dữ liệu ' + level);
    return response.json();
  }));
  const queue = [];
  levels.forEach((level, levelIndex) => {
    const words = datasets[levelIndex];
    const cards = loadSrsForLevel(level, words, readSavedLevelProgressLegacy(level));
    words.forEach(word => {
      const card = cards[word.id];
      if (SRS.isDue(card, now)) queue.push({ level, word, card, due: new Date(card.due).getTime() });
    });
  });
  queue.sort((a, b) => a.due - b.due);
  return queue;
}

function formatDuePreview(preview) {
  const milliseconds = preview && preview.intervalMs;
  if (!Number.isFinite(milliseconds)) return '';
  if (milliseconds < 86400000) return Math.max(1, Math.round(milliseconds / 60000)) + 'p';
  return Math.max(1, Math.round(milliseconds / 86400000)) + 'n';
}

function renderTodayReviewCard() {
  const area = document.getElementById('todayReviewCardArea');
  const progressNode = document.getElementById('todayReviewProgress');
  if (todayReviewIndex >= todayReviewQueue.length) {
    progressNode.textContent = 'Đã ôn xong tất cả thẻ đến hạn.';
    area.innerHTML = '<div class="today-review-empty">🎉 Không còn thẻ đến hạn hôm nay.</div>';
    renderLearningDashboard();
    return;
  }
  const item = todayReviewQueue[todayReviewIndex];
  const previews = SRS.preview(item.card, new Date(), srsRetention);
  progressNode.textContent = (todayReviewIndex + 1) + ' / ' + todayReviewQueue.length + ' thẻ';
  area.innerHTML = `
    <article class="today-review-card">
      <div class="today-review-level">${LEVELS[item.level].label}</div>
      <div class="hanzi">${escapeHtml(item.word.hanzi)}</div>
      <div class="pinyin">${escapeHtml(item.word.pinyin)}</div>
      <div class="meaning">${escapeHtml(item.word.meaning)}</div>
      <div class="action-row today-review-actions">
        <button class="btn-unknown" onclick="rateTodayReview('again')">Quên <span>${formatDuePreview(previews.again)}</span></button>
        <button class="btn-unknown" onclick="rateTodayReview('hard')">Khó <span>${formatDuePreview(previews.hard)}</span></button>
        <button class="btn-known" onclick="rateTodayReview('good')">Được <span>${formatDuePreview(previews.good)}</span></button>
        <button class="btn-known" onclick="rateTodayReview('easy')">Dễ <span>${formatDuePreview(previews.easy)}</span></button>
      </div>
    </article>`;
}

function escapeHtml(value) {
  return String(value == null ? '' : value).replace(/[&<>"']/g, character => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  })[character]);
}

function rateTodayReview(rating) {
  const item = todayReviewQueue[todayReviewIndex];
  if (!item) return;
  const record = readSrsRecord(item.level);
  const cards = record ? record.cards : {};
  reviewSrsCard(item.level, item.word.id, rating, cards);
  recordDailyStudy(item.word.id, item.level);
  todayReviewIndex++;
  renderTodayReviewCard();
}

async function openTodayReviews() {
  const hub = document.getElementById('screenVocabHub');
  const cards = document.getElementById('screenCards');
  const reviewScreen = document.getElementById('screenTodayReviews');
  if (hub) hub.style.display = 'none';
  if (cards) cards.style.display = 'none';
  reviewScreen.style.display = '';
  document.getElementById('primaryTabs').style.display = 'none';
  document.getElementById('todayReviewCardArea').innerHTML = '<div class="loading-text">Đang tìm thẻ đến hạn...</div>';
  try {
    todayReviewQueue = await loadTodayReviewQueue();
    todayReviewIndex = 0;
    renderTodayReviewCard();
  } catch (error) {
    console.error('Today review queue failed:', error);
    document.getElementById('todayReviewCardArea').innerHTML = '<div class="error-text">Không thể tải thẻ ôn tập. Vui lòng thử lại.</div>';
  }
}

function closeTodayReviews() {
  document.getElementById('screenTodayReviews').style.display = 'none';
  document.getElementById('screenVocabHub').style.display = '';
  document.getElementById('primaryTabs').style.display = '';
  renderLearningDashboard();
}
