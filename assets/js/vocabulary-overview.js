// Vocabulary overview mode, search, status filtering, and card deep links.
function setViewMode(mode) {
  if (!currentLevel || !['cards', 'overview'].includes(mode)) return;

  stopSpeech();
  currentView = mode;
  const showOverview = mode === 'overview';
  const studyView = document.getElementById('studyView');
  const overviewView = document.getElementById('overviewView');
  const flashcardTab = document.getElementById('flashcardTab');
  const overviewTab = document.getElementById('overviewTab');

  studyView.hidden = showOverview;
  overviewView.hidden = !showOverview;
  flashcardTab.classList.toggle('active', mode === 'cards');
  overviewTab.classList.toggle('active', showOverview);
  flashcardTab.setAttribute('aria-selected', String(mode === 'cards'));
  overviewTab.setAttribute('aria-selected', String(showOverview));
  document.getElementById('appTitle').textContent = showOverview
    ? LEVELS[currentLevel].label + ' · Tổng quan'
    : LEVELS[currentLevel].label + ' Flashcards';

  if (showOverview) {
    const searchInput = document.getElementById('overviewSearch');
    const statusSelect = document.getElementById('overviewStatus');
    searchInput.value = overviewQuery;
    statusSelect.value = overviewStatus;
    renderOverview();
  }

  if (mode === 'cards') {
    setFilter(currentFilter);
  }
}

function normalizeSearchText(value) {
  return String(value || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim();
}

function updateOverviewSearch(value) {
  overviewQuery = value;
  renderOverview();
}

function updateOverviewStatus(value) {
  overviewStatus = value;
  renderOverview();
}

function wordLearningStatus(word) {
  const status = progress[word.id];
  return status === 'known' || status === 'unknown' ? status : 'unseen';
}

function formatWordCount(count) {
  return new Intl.NumberFormat('vi-VN').format(count);
}

function renderOverview() {
  if (!currentLevel || currentView !== 'overview') return;

  const normalizedQuery = normalizeSearchText(overviewQuery);
  const matches = WORDS
    .map((word, wordIndex) => ({ word, wordIndex }))
    .filter(({ word }) => {
      const matchesStatus = overviewStatus === 'all' || wordLearningStatus(word) === overviewStatus;
      if (!matchesStatus) return false;
      if (!normalizedQuery) return true;
      return normalizeSearchText(`${word.hanzi} ${word.pinyin} ${word.meaning}`).includes(normalizedQuery);
    });

  document.getElementById('overviewTitle').textContent = `Trọn bộ từ vựng ${LEVELS[currentLevel].label}`;
  document.getElementById('overviewDescription').textContent =
    `Xem tổng thể ${formatWordCount(WORDS.length)} từ trước và trong khi học.`;
  document.getElementById('overviewTotal').textContent = `${formatWordCount(WORDS.length)} từ`;
  document.getElementById('overviewResultSummary').textContent =
    normalizedQuery || overviewStatus !== 'all'
      ? `Tìm thấy ${matches.length} / ${WORDS.length} từ`
      : `Hiển thị toàn bộ ${WORDS.length} từ`;

  const list = document.getElementById('vocabularyList');
  list.innerHTML = '';

  if (matches.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'overview-empty';
    empty.textContent = 'Không tìm thấy từ phù hợp. Hãy thử từ khóa hoặc trạng thái khác.';
    list.appendChild(empty);
    return;
  }

  const statusLabels = {
    unseen: 'Chưa học',
    unknown: 'Chưa nhớ',
    known: 'Đã nhớ',
  };
  const fragment = document.createDocumentFragment();

  matches.forEach(({ word, wordIndex }) => {
    const status = wordLearningStatus(word);
    const item = document.createElement('button');
    item.type = 'button';
    item.className = 'vocabulary-item';
    item.setAttribute('aria-label', `${word.hanzi}, ${word.pinyin}, ${word.meaning}. Mở flashcard`);
    item.onclick = () => openWordInCards(wordIndex);

    const number = document.createElement('span');
    number.className = 'vocabulary-number';
    number.textContent = String(wordIndex + 1).padStart(String(WORDS.length).length, '0');

    const content = document.createElement('span');
    content.className = 'vocabulary-content';

    const wordLine = document.createElement('span');
    wordLine.className = 'vocabulary-word-line';

    const hanzi = document.createElement('span');
    hanzi.className = 'vocabulary-hanzi';
    hanzi.textContent = word.hanzi;

    const pinyin = document.createElement('span');
    pinyin.className = 'vocabulary-pinyin';
    pinyin.textContent = word.pinyin;

    const meaning = document.createElement('span');
    meaning.className = 'vocabulary-meaning';
    meaning.textContent = word.meaning;

    const badge = document.createElement('span');
    badge.className = `vocabulary-status vocabulary-status--${status}`;
    badge.textContent = statusLabels[status];

    wordLine.append(hanzi, pinyin);
    content.append(wordLine, meaning);
    item.append(number, content, badge);
    fragment.appendChild(item);
  });

  list.appendChild(fragment);
}

function openWordInCards(wordIndex) {
  currentFilter = 'all';
  filteredOrder = order.slice();
  const position = filteredOrder.indexOf(wordIndex);
  idx = position >= 0 ? position : 0;
  renderFilters();
  setViewMode('cards');
  render('fade');
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.getElementById('cardArea').scrollIntoView({
    behavior: prefersReducedMotion ? 'auto' : 'smooth',
    block: 'start',
  });
}
