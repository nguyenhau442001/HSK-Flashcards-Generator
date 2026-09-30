// Study navigation, mastery actions, celebration, and progress controls.
function nextCard() { if (filteredOrder.length===0) return; idx = (idx + 1) % filteredOrder.length; render('next'); }
function prevCard() { if (filteredOrder.length===0) return; idx = (idx - 1 + filteredOrder.length) % filteredOrder.length; render('prev'); }
function rateCurrentCard(rating) {
  if (filteredOrder.length===0) return;
  const wIdx = filteredOrder[idx % filteredOrder.length];
  const word = WORDS[wIdx];
  const card = srsCards[word.id];
  if (card && card.state === SRS.State.New && countNewReviewsToday() >= readDailyStudyGoal()) {
    const message = document.getElementById('dailyNewLimitMessage');
    if (message) message.textContent = 'Đã đạt giới hạn thẻ mới hôm nay. Bạn vẫn có thể ôn thẻ đến hạn ở mục “Ôn hôm nay”.';
    return;
  }
  reviewSrsCard(currentLevel, word.id, rating, srsCards);
  const limitMessage = document.getElementById('dailyNewLimitMessage');
  if (limitMessage) limitMessage.textContent = '';
  saveProgress();
  recordDailyStudy(word.id, currentLevel);
  updateStats();
  if (currentView === 'overview') renderOverview();
  checkCelebration();
  if (currentFilter !== 'all') advanceAfterMark(wIdx); else nextCard();
}
function markKnown() { rateCurrentCard('good'); }
function markUnknown() { rateCurrentCard('again'); }
function checkCelebration() {
  if (celebrationShown || WORDS.length === 0) return;
  const known = Object.values(srsCards).filter(card => card.state === SRS.State.Review).length;
  if (known === WORDS.length) {
    celebrationShown = true;
    showCelebration();
  }
}
function showCelebration() {
  const overlay = document.createElement('div');
  overlay.id = 'celebrationOverlay';
  overlay.className = 'celebration-overlay';
  overlay.innerHTML = `
    <div class="celebration-box">
      <div class="celebration-trophy">🏆</div>
      <div class="celebration-title">Xuất sắc!</div>
      <div class="celebration-msg">Bạn đã nhớ tất cả <strong>${WORDS.length}</strong> từ vựng <strong>${LEVELS[currentLevel].label}</strong>!</div>
      <button class="celebration-btn" onclick="document.getElementById('celebrationOverlay').remove()">Tiếp tục ôn luyện</button>
    </div>`;
  overlay.addEventListener('click', e => { if (e.target === overlay) overlay.remove(); });
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const colors = ['var(--accent)', 'var(--success-text)', 'var(--info-text)', 'var(--danger-text)'];
    for (let i = 0; i < 28; i++) {
      const p = document.createElement('div');
      p.className = 'confetti-piece';
      const size = 5 + Math.random() * 6;
      p.style.cssText = `left:${3 + Math.random() * 94}%;width:${size}px;height:${size + Math.random() * 7}px;background:${colors[i % colors.length]};animation-delay:${(Math.random() * 0.5).toFixed(2)}s;animation-duration:${(1 + Math.random() * 0.7).toFixed(2)}s;border-radius:${Math.random() > 0.4 ? '50%' : '2px'};`;
      overlay.appendChild(p);
    }
  }
  document.body.appendChild(overlay);
}
function advanceAfterMark(prevWIdx) {
  const prevIdx = idx;
  if (currentFilter === 'unseen') filteredOrder = order.filter(i => !progress[WORDS[i].id]);
  else filteredOrder = order.filter(i => progress[WORDS[i].id] === currentFilter);
  renderFilters();
  if (filteredOrder.length === 0) { idx = 0; render('fade'); return; }
  if (filteredOrder.includes(prevWIdx)) {
    idx = (prevIdx + 1) % filteredOrder.length;
  } else {
    idx = Math.min(prevIdx, filteredOrder.length - 1);
  }
  render('fade');
}
function togglePinyin() {
  showPinyin = !showPinyin;
  const btn = document.getElementById('pinyinToggle');
  if (btn) {
    const icon = document.getElementById('pinyinToggleIcon');
    if (icon) {
      icon.textContent = showPinyin ? '👁' : '🙈';
      btn.title = showPinyin ? 'Ẩn pinyin' : 'Hiện pinyin';
      btn.setAttribute('aria-label', showPinyin ? 'Ẩn pinyin' : 'Hiện pinyin');
    } else {
      btn.textContent = showPinyin ? '👁 Đang hiện pinyin' : '🙈 Chế độ thử thách: ẩn pinyin';
    }
    btn.classList.toggle('on', !showPinyin);
  }
  savePrefs();
  render();
}
function shuffleDeck() {
  for (let i = order.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [order[i], order[j]] = [order[j], order[i]];
  }
  savePrefs();
  setFilter(currentFilter);
}
function resetProgress() {
  const cards = Object.values(srsCards);
  const started = cards.filter(card => card.state !== SRS.State.New).length;
  const known = cards.filter(card => card.state === SRS.State.Review).length;
  const message = [
    'Học lại ' + LEVELS[currentLevel].label + ' từ đầu?',
    '',
    'Sẽ bị reset:',
    '• Lịch ôn FSRS của cả ' + WORDS.length + ' từ (' + started + ' từ đã học, ' + known + ' từ đã nhớ) — mọi thẻ quay về "chưa học".',
    '• Trạng thái Đã nhớ / Chưa nhớ và số thẻ đến hạn của cấp độ này.',
    '',
    'Giữ nguyên: nhật ký ôn tập, chuỗi ngày học, từ khó đã đánh dấu và các cấp độ khác.',
    '',
    'Không thể hoàn tác. Nên bấm "Sao lưu" trước nếu muốn giữ lại.',
  ].join('\n');
  if (!confirm(message)) return;
  srsCards = {};
  WORDS.forEach(word => { srsCards[word.id] = SRS.createNewCard(); });
  progress = {};
  saveProgress();
  setFilter(currentFilter);
}
function toggleTransferPanel() {
  const panel = document.getElementById('transferPanel');
  const button = document.getElementById('transferToggle');
  const willOpen = panel.hidden;
  panel.hidden = !willOpen;
  button.setAttribute('aria-expanded', String(willOpen));
  button.classList.toggle('on', willOpen);
}
function toggleUnknownWords() {
  const box = document.getElementById('unknownWordsList');
  const button = document.getElementById('unknownWordsToggle');
  const isOpen = box.classList.contains('show');

  if (isOpen) {
    box.classList.remove('show');
    button.textContent = 'Hiển thị từ chưa nhớ';
    button.setAttribute('aria-expanded', 'false');
    return;
  }

  const unknownWords = WORDS.filter(w => progress[w.id] === 'unknown');
  if (unknownWords.length === 0) {
    box.textContent = 'Chưa có từ nào được đánh dấu "Chưa nhớ".';
  } else {
    box.textContent = unknownWords
      .map((w, index) => (index + 1) + '. ' + w.hanzi + ' (' + w.pinyin + ') - ' + w.meaning)
      .join('\n');
  }
  box.classList.add('show');
  button.textContent = 'Ẩn từ chưa nhớ';
  button.setAttribute('aria-expanded', 'true');
}

document.addEventListener('keydown', event => {
  if (!currentLevel || currentView !== 'cards' || event.altKey || event.ctrlKey || event.metaKey) return;
  if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement && document.activeElement.tagName)) return;
  if (event.key === ' ') {
    if (document.activeElement && document.activeElement.closest('button, summary, a')) return;
    event.preventDefault();
    if (!isCardRevealed()) flip();
    return;
  }
  const rating = RATING_KEYS[event.key];
  if (rating && ratingsVisible()) { event.preventDefault(); rateCurrentCard(rating); }
});
