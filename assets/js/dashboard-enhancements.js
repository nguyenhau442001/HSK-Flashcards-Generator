// Home dashboard additions: compact level status, continuation card and radical study shortcuts.
const COMMON_RADICALS = [
  { char: '氵', name: 'Thủy', set: 'basic50', hint: 'Nước' },
  { char: '亻', name: 'Nhân', set: 'basic50', hint: 'Người' },
  { char: '扌', name: 'Thủ', set: 'basic50', hint: 'Tay' },
  { char: '口', name: 'Khẩu', set: 'basic50', hint: 'Miệng' },
  { char: '心', name: 'Tâm', set: 'basic50', hint: 'Tim' },
  { char: '木', name: 'Mộc', set: 'basic50', hint: 'Cây' },
];

function openCommonRadical(character) {
  setPrimaryTab('radicals');
  ensureRadicalDataLoaded().then(loaded => {
    if (!loaded || primaryTab !== 'radicals') return;
    const found = Object.entries(RADICAL_GROUPS).flatMap(([set, groups]) =>
      groups.flatMap((group, groupIndex) => group
        .map((item, itemIndex) => ({ set, groupIndex, itemIndex, item }))
        .filter(entry => entry.item.radical === character || (entry.item.variants || []).includes(character)))
    )[0];
    if (!found) return;
    startRadicalStudy(found.set, found.groupIndex);
    radicalIdx = found.itemIndex;
    renderRadicalCard();
  });
}

function renderDashboardEnhancements() {
  const continuation = document.getElementById('continueLearningCard');
  const target = learningProgressSummary().target;
  if (continuation && target) {
    const cfg = LEVELS[target.level];
    const ratio = `${target.known.toLocaleString('vi-VN')} / ${cfg.total.toLocaleString('vi-VN')} từ đã nhớ`;
    document.getElementById('continueLearningTitle').textContent = `${cfg.label} · Bộ từ đang học`;
    document.getElementById('continueLearningProgress').textContent = `${ratio} · ${Math.round(target.known / cfg.total * 100)}% tiến độ`;
    continuation.dataset.level = target.level;
  }

  const activity = readStudyActivity();
  const today = localDateKey(new Date());
  const todayWords = new Set(dayWordCount(activity.days[today]) ? activity.days[today].words : []);
  ['hsk1', 'hsk2', 'hsk3', 'hsk4', 'hsk5', 'hsk6'].forEach(level => {
    const card = document.querySelector(`.level-card[data-level="${level}"]`);
    if (!card || !LEVELS[level]) return;
    const cfg = LEVELS[level];
    const statuses = Object.values(readSavedLevelProgress(level));
    const known = statuses.filter(status => status === 'known').length;
    const studied = statuses.filter(status => status === 'known' || status === 'unknown').length;
    const complete = known >= cfg.total;
    const isLearning = !complete && (studied > 0 || (target && target.level === level));
    card.classList.toggle('is-active-level', Boolean(target && target.level === level && !complete));
    card.classList.toggle('is-complete-level', complete);
    card.classList.toggle('is-learning-level', isLearning);
    let badge = card.querySelector('.level-status-badge');
    if (!badge) {
      badge = document.createElement('span');
      badge.className = 'lvl-status-pill level-status-badge';
      const bottom = card.querySelector('.level-card-bottom-row') || card;
      bottom.appendChild(badge);
    }
    badge.className = `lvl-status-pill level-status-badge${complete ? ' is-complete' : isLearning ? ' is-learning' : ' is-not-started'}`;
    badge.textContent = complete ? '✓ Hoàn thành' : isLearning ? '● Đang học' : 'Chưa học';

    let daily = card.querySelector('.lvl-today-count');
    if (!daily) {
      daily = document.createElement('div');
      daily.className = 'lvl-today-count';
      const summary = card.querySelector('.level-card-progress-heading');
      if (summary) summary.appendChild(daily);
      else {
        const track = card.querySelector('.lvl-mastery-track');
        card.insertBefore(daily, track || card.lastElementChild);
      }
    }
    const todayCount = [...todayWords].filter(key => key.startsWith(level + ':')).length;
    daily.classList.toggle('has-activity', todayCount > 0);
    daily.textContent = `+${todayCount} từ hôm nay`;
    const pct = Math.round(known / cfg.total * 100);
    const percentValue = card.querySelector('.lvl-percent-value');
    if (percentValue) percentValue.textContent = `${pct}%`;
    const legacyPercent = card.querySelector('.lvl-percent-complete');
    if (legacyPercent) legacyPercent.remove();
    const progressText = card.querySelector('.lvl-mastery-text');
    if (progressText) progressText.textContent = `${known.toLocaleString('vi-VN')} / ${cfg.total.toLocaleString('vi-VN')} đã nhớ`;
  });
}

function initDashboardSidebar() {
  if (!document.body.classList.contains('is-desktop-dock')) return;
  const mount = document.getElementById('workstationLeft');
  if (!mount) return;

  const radicals = document.createElement('section');
  radicals.className = 'dashboard-sidebar-card common-radicals-card';
  radicals.innerHTML = `<div class="sidebar-card-heading"><h2>Bộ thủ thông dụng</h2><span>6 bộ</span></div>
    <div class="common-radicals-grid">${COMMON_RADICALS.map(item => `
      <button type="button" class="common-radical" data-radical="${item.char}" aria-label="Học bộ ${item.name}: ${item.hint}">
        <span class="common-radical-char" lang="zh-CN">${item.char}</span><span class="common-radical-name">${item.name}</span>
      </button>`).join('')}</div>`;
  radicals.addEventListener('click', event => {
    const button = event.target.closest('[data-radical]');
    if (button) openCommonRadical(button.dataset.radical);
  });
  mount.appendChild(radicals);

  const tip = document.createElement('section');
  tip.className = 'dashboard-sidebar-card radical-tip-card';
  tip.innerHTML = `<div class="sidebar-card-heading"><h2>Mẹo nhớ chữ Hán</h2><span>Gợi ý</span></div>
    <div class="radical-tip-word" lang="zh-CN">休 <span>xiū · nghỉ ngơi</span></div>
    <p>Một người <b>亻</b> tựa vào gốc cây <b>木</b> để nghỉ ngơi. Nhìn chữ là nhớ ngay!</p>`;
  mount.appendChild(tip);

  const desktopQuery = window.matchMedia('(min-width: 1280px)');
  const placeReviewCard = isDesktop => {
    const card = document.getElementById('hwForgotten');
    if (!card) return;
    const parent = isDesktop ? document.getElementById('workstationLeft') : document.getElementById('homeWidgets');
    if (parent) parent.appendChild(card);
  };
  placeReviewCard(desktopQuery.matches);
  desktopQuery.addEventListener('change', event => placeReviewCard(event.matches));
  renderDashboardEnhancements();
}

document.addEventListener('DOMContentLoaded', initDashboardSidebar);
