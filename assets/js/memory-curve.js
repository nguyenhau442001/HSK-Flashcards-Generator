// Lazy, per-card memory curve rendering using ts-fsrs retrievability.
const CURVE_RATING_COLORS = { again: '#d94d4d', hard: '#e58b32', good: '#3b9b68', easy: '#4385d1' };

function openCurrentMemoryCurve() {
  if (!currentLevel || !filteredOrder.length) return;
  const word = WORDS[filteredOrder[idx % filteredOrder.length]];
  openMemoryCurve(currentLevel, word.id);
}

function formatCurveDate(date) {
  return new Intl.DateTimeFormat('vi-VN', { day: 'numeric', month: 'short', year: 'numeric' }).format(date);
}

function formatCurvePercent(value) {
  return Number.isFinite(value) ? Math.round(value * 100) + '%' : '—';
}

function curveCardAt(stability, difficulty, reviewedAt) {
  const card = SRS.createNewCard(reviewedAt);
  card.state = SRS.State.Review;
  card.stability = stability;
  card.difficulty = difficulty;
  card.last_review = new Date(reviewedAt).toISOString();
  card.reps = 1;
  card.lapses = 0;
  return card;
}

function buildCurveSvg(card, logs, retention) {
  const width = 760, height = 340;
  const left = 54, right = 22, top = 22, bottom = 48;
  const plotWidth = width - left - right;
  const plotHeight = height - top - bottom;
  const now = new Date();
  const due = new Date(card.due);
  const history = logs.map(entry => ({ ...entry, date: new Date(entry.timestamp) }))
    .filter(entry => Number.isFinite(entry.date.getTime()) && Number.isFinite(entry.stabilityAfter))
    .sort((a, b) => a.date - b.date);
  const firstMemoryDate = history.length ? history[0].date : card.last_review ? new Date(card.last_review) : now;
  const duePadding = Number.isFinite(due.getTime()) ? Math.max(86400000, (due.getTime() - firstMemoryDate.getTime()) * 0.2) : 86400000;
  const end = new Date(Math.max(now.getTime() + 86400000, due.getTime() + duePadding));
  const start = firstMemoryDate.getTime() < now.getTime() ? firstMemoryDate : now;
  const span = Math.max(86400000, end.getTime() - start.getTime());
  const x = date => left + ((date.getTime() - start.getTime()) / span) * plotWidth;
  const y = value => top + (1 - Math.min(1, Math.max(0, value))) * plotHeight;
  const sampleCount = 160;
  const sampleDates = (from, to) => Array.from({ length: sampleCount + 1 }, (_, index) =>
    new Date(from.getTime() + ((to.getTime() - from.getTime()) * index / sampleCount)));

  let historyPath = '';
  if (history.length) {
    const points = sampleDates(start, now);
    let lastEntryIndex = -1;
    points.forEach((date, index) => {
      while (lastEntryIndex + 1 < history.length && history[lastEntryIndex + 1].date <= date) lastEntryIndex++;
      if (lastEntryIndex < 0) return;
      const entry = history[lastEntryIndex];
      const curveCard = curveCardAt(entry.stabilityAfter, entry.difficultyAfter || card.difficulty, entry.date);
      const value = SRS.retrievability(curveCard, date, retention);
      historyPath += (index === 0 || historyPath === '' ? 'M' : 'L') + x(date).toFixed(2) + ',' + y(value).toFixed(2) + ' ';
    });
  }

  const futureStart = now;
  const futureDates = sampleDates(futureStart, end);
  const futurePath = futureDates.map((date, index) => {
    const value = SRS.retrievability(card, date, retention);
    return (index === 0 ? 'M' : 'L') + x(date).toFixed(2) + ',' + y(value).toFixed(2);
  }).join(' ');

  const retentionY = y(retention);
  const todayX = x(now);
  const dueX = x(due);
  const grid = [0, 0.25, 0.5, 0.75, 1].map(value => `
    <g class="curve-gridline"><line x1="${left}" y1="${y(value)}" x2="${width - right}" y2="${y(value)}" />
      <text x="${left - 9}" y="${y(value) + 4}" text-anchor="end">${Math.round(value * 100)}%</text></g>`).join('');
  const markers = history.map(entry => {
    const color = CURVE_RATING_COLORS[entry.rating] || '#888';
    const retrievability = Number(entry.retrievabilityBefore) || 0;
    const tooltip = `${formatCurveDate(entry.date)} · ${entry.rating} · R ${formatCurvePercent(retrievability)} · S ${Number(entry.stabilityAfter).toFixed(1)} ngày`;
    return `<circle class="curve-review-point" cx="${x(entry.date)}" cy="${y(retrievability)}" r="5" fill="${color}"
      tabindex="0" role="button" aria-label="${escapeHtml(tooltip)}" data-tooltip="${escapeHtml(tooltip)}"><title>${escapeHtml(tooltip)}</title></circle>`;
  }).join('');
  const dateLabels = `<text x="${left}" y="${height - 12}">${escapeHtml(formatCurveDate(start))}</text>
    <text x="${width - right}" y="${height - 12}" text-anchor="end">${escapeHtml(formatCurveDate(end))}</text>`;

  return `<svg class="memory-curve-svg" viewBox="0 0 ${width} ${height}" role="img" aria-label="Đường cong retrievability của từ vựng">
    ${grid}
    <line class="curve-retention-line" x1="${left}" y1="${retentionY}" x2="${width - right}" y2="${retentionY}" />
    <text class="curve-retention-label" x="${width - right - 2}" y="${retentionY - 5}" text-anchor="end">Mục tiêu ${Math.round(retention * 100)}%</text>
    ${historyPath ? `<path class="curve-history-path" d="${historyPath}" />` : ''}
    <path class="curve-future-path" d="${futurePath}" />
    ${markers}
    ${todayX >= left && todayX <= width - right ? `<line class="curve-today-line" x1="${todayX}" y1="${top}" x2="${todayX}" y2="${height - bottom}" /><text x="${todayX + 4}" y="${top + 12}">Hôm nay</text>` : ''}
    ${dueX >= left && dueX <= width - right ? `<line class="curve-due-line" x1="${dueX}" y1="${top}" x2="${dueX}" y2="${height - bottom}" /><text x="${dueX - 4}" y="${top + 26}" text-anchor="end">Đến hạn</text>` : ''}
    ${dateLabels}
  </svg>`;
}

function showCurvePointTooltip(event) {
  const tooltip = document.getElementById('memoryCurveTooltip');
  const point = event.target.closest('.curve-review-point');
  if (!tooltip || !point) return;
  tooltip.textContent = point.dataset.tooltip;
  tooltip.hidden = false;
  const rect = tooltip.parentElement.getBoundingClientRect();
  const pointerX = Number.isFinite(event.clientX) ? event.clientX - rect.left : rect.width / 2;
  const pointerY = Number.isFinite(event.clientY) ? event.clientY - rect.top : rect.height / 2;
  tooltip.style.left = Math.max(8, Math.min(rect.width - 230, pointerX)) + 'px';
  tooltip.style.top = Math.max(8, pointerY - 42) + 'px';
}

function closeMemoryCurve() {
  const modal = document.getElementById('memoryCurveModal');
  if (modal) modal.remove();
  document.removeEventListener('keydown', memoryCurveKeydown);
}

function memoryCurveKeydown(event) {
  if (event.key === 'Escape') closeMemoryCurve();
}

function openMemoryCurve(level, wordId) {
  const word = (level === currentLevel ? WORDS : []).find(item => String(item.id) === String(wordId));
  const cardMap = level === currentLevel ? srsCards : readSrsRecord(level)?.cards || {};
  const card = cardMap[wordId] || SRS.createNewCard();
  const logs = readSrsReviewLog(level).filter(entry => String(entry.wordId) === String(wordId)
    && (!card.historyStartAt || new Date(entry.timestamp) >= new Date(card.historyStartAt)));
  const targetWord = word || { hanzi: String(wordId), pinyin: '', meaning: '' };
  const retrievability = SRS.retrievability(card, new Date(), srsRetention);
  const due = new Date(card.due);
  const noHistory = logs.length === 0;
  const modal = document.createElement('div');
  modal.id = 'memoryCurveModal';
  modal.className = 'memory-curve-overlay';
  modal.innerHTML = `
    <section class="memory-curve-dialog" role="dialog" aria-modal="true" aria-labelledby="memoryCurveTitle">
      <button type="button" class="memory-curve-close" onclick="closeMemoryCurve()" aria-label="Đóng">✕</button>
      <h2 id="memoryCurveTitle">📈 Đường cong ghi nhớ · ${escapeHtml(targetWord.hanzi)}</h2>
      <p class="memory-curve-subtitle">${escapeHtml(targetWord.pinyin)} · ${escapeHtml(targetWord.meaning)}</p>
      ${noHistory ? '<p class="memory-curve-note">Chưa có lịch sử ôn; biểu đồ chỉ hiển thị đường dự kiến từ hôm nay.</p>' : ''}
      <div class="memory-curve-chart-wrap">${buildCurveSvg(card, logs, srsRetention)}<div id="memoryCurveTooltip" class="memory-curve-tooltip" hidden></div></div>
      <div class="memory-curve-legend">
        <span><i class="curve-line-swatch"></i> Quá khứ</span><span><i class="curve-line-swatch future"></i> Dự kiến</span>
        <span><i class="curve-dot" style="--dot:${CURVE_RATING_COLORS.again}"></i> Again</span>
        <span><i class="curve-dot" style="--dot:${CURVE_RATING_COLORS.hard}"></i> Hard</span>
        <span><i class="curve-dot" style="--dot:${CURVE_RATING_COLORS.good}"></i> Good</span>
        <span><i class="curve-dot" style="--dot:${CURVE_RATING_COLORS.easy}"></i> Easy</span>
      </div>
      <dl class="memory-curve-stats">
        <div><dt>Stability</dt><dd>${Number(card.stability).toFixed(1)} ngày</dd></div>
        <div><dt>Difficulty</dt><dd>${Number(card.difficulty).toFixed(1)} / 10</dd></div>
        <div><dt>Lượt ôn</dt><dd>${Number(card.reps) || 0}</dd></div>
        <div><dt>Số lần quên</dt><dd>${Number(card.lapses) || 0}</dd></div>
        <div><dt>R hiện tại</dt><dd>${formatCurvePercent(retrievability)}</dd></div>
        <div><dt>Đến hạn</dt><dd>${escapeHtml(Number.isFinite(due.getTime()) ? formatCurveDate(due) : '—')}</dd></div>
      </dl>
    </section>`;
  modal.addEventListener('click', event => { if (event.target === modal) closeMemoryCurve(); });
  modal.querySelectorAll('.curve-review-point').forEach(point => {
    point.addEventListener('pointerenter', showCurvePointTooltip);
    point.addEventListener('click', showCurvePointTooltip);
    point.addEventListener('focus', showCurvePointTooltip);
  });
  document.body.appendChild(modal);
  document.addEventListener('keydown', memoryCurveKeydown);
}
