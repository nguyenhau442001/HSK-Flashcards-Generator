// Level picker, welcome message, and level data loading.
function localDateKey(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function calendarDayDifference(fromKey, toKey) {
  const from = String(fromKey).split('-').map(Number);
  const to = String(toKey).split('-').map(Number);
  if (from.length !== 3 || to.length !== 3 || from.some(Number.isNaN) || to.some(Number.isNaN)) return null;
  const fromDate = new Date(from[0], from[1] - 1, from[2], 12);
  const toDate = new Date(to[0], to[1] - 1, to[2], 12);
  return Math.round((toDate - fromDate) / 86400000);
}

function hasSavedProgress() {
  return Object.keys(LEVELS).some(level => {
    try {
      const raw = localStorage.getItem('hsk_' + level + '_progress_v2');
      return raw && Object.keys(JSON.parse(raw)).length > 0;
    } catch (e) {
      return false;
    }
  });
}

function timeGreeting(hour) {
  if (hour < 5) return 'Học giờ này là chăm chỉ hay chưa chịu ngủ vậy bạn? 👀';
  if (hour < 8) return 'Chim sẻ dậy sớm, từ vựng tự chui vào đầu 🐦';
  if (hour < 11) return 'Buổi sáng học vài từ, cả ngày thấy mình tri thức ☀️';
  if (hour < 14) return 'Ăn trưa nhớ ăn, học từ cũng nhớ học nha 🍜';
  if (hour < 18) return 'Buổi chiều hơi buồn ngủ, làm vài flashcard cho tỉnh ☕';
  if (hour < 22) return 'Tối nay không lướt vô tri, mình lướt flashcard nhé 😌';
  return 'Cú đêm học bài — mai dậy nhớ được bao nhiêu tính sau 🦉';
}

function pickGreeting(candidates, previousGreeting) {
  const freshCandidates = candidates.filter(message => message !== previousGreeting);
  const pool = freshCandidates.length ? freshCandidates : candidates;
  return pool[Math.floor(Math.random() * pool.length)];
}

function showWelcomeToast() {
  const toast = document.getElementById('welcomeToast');
  const messageNode = document.getElementById('welcomeToastMessage');
  if (!toast || !messageNode) return;

  try {
    if (sessionStorage.getItem('hsk_welcome_shown_v1')) return;
    sessionStorage.setItem('hsk_welcome_shown_v1', '1');
  } catch (e) {}

  const now = new Date();
  const today = localDateKey(now);
  let history = null;
  let previousGreeting = '';

  try {
    history = JSON.parse(localStorage.getItem('hsk_visit_history_v1'));
    previousGreeting = localStorage.getItem('hsk_last_greeting_v1') || '';
  } catch (e) {}

  let greeting;
  let streak = 1;
  const firstVisit = !history || !history.lastVisit;

  if (firstVisit) {
    greeting = 'Chào mừng bạn! Chọn một cấp độ rồi mình chiến thôi 👋';
  } else {
    const dayDifference = calendarDayDifference(history.lastVisit, today);
    const continuedStreak = dayDifference === 1;
    const sameDay = dayDifference === 0;
    streak = sameDay ? Math.max(1, Number(history.streak) || 1)
      : continuedStreak ? Math.max(1, Number(history.streak) || 1) + 1
        : 1;

    const contextualGreetings = [];

    if (hasSavedProgress()) {
      contextualGreetings.push('Lại gặp nhau rồi! Hôm nay mình xử tiếp mấy từ hôm qua nhé.');
    }
    if (continuedStreak && streak >= 2) {
      contextualGreetings.push('Chuỗi học vẫn còn nóng, đừng để nó nguội nha 🔥');
    }
    contextualGreetings.push(
      timeGreeting(now.getHours()),
      'Mừng bạn quay trở lại! Não bộ đã sẵn sàng nạp tiếng Trung chưa? 🧠',
    );

    const playfulGreetings = [
      'Không học hôm nay thì ngày mai… vẫn phải học thôi 😌',
      'Một từ cũng là học, 50 từ là hơi tham.',
      'HSK không khó, chỉ là từ vựng hơi đông.',
      'Bạn học đi, chiếc app này tin bạn.',
      'Não đang loading… flashcard đang hỗ trợ.',
      'Học nhẹ vài từ, flex mạnh một đời.',
      'Vuốt phải vì đã nhớ, không phải vì định mệnh.',
      'Từ này quen lắm, nhưng nghĩa là gì thì chưa chắc.',
      'Thêm một từ vào não, bớt một chút hoang mang.',
      'Đừng để chữ Hán nhìn bạn như người xa lạ.',
    ];

    const playfulGreeting = pickGreeting(playfulGreetings, previousGreeting);
    greeting = pickGreeting([...contextualGreetings, playfulGreeting], previousGreeting);
  }

  try {
    localStorage.setItem('hsk_visit_history_v1', JSON.stringify({ lastVisit: today, streak }));
    localStorage.setItem('hsk_last_greeting_v1', greeting);
  } catch (e) {}

  messageNode.textContent = greeting;
  toast.hidden = false;
  requestAnimationFrame(() => toast.classList.add('show'));

  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => { toast.hidden = true; }, 220);
  }, 4200);
}

function renderLevelProgress() {
  Object.keys(LEVELS).forEach(level => {
    const total = LEVELS[level].total;
    let known = 0;
    try {
      const raw = localStorage.getItem('hsk_' + level + '_progress_v2');
      if (raw) {
        const data = JSON.parse(raw);
        Object.values(data).forEach(v => { if (v === 'known') known++; });
      }
    } catch (e) {}
    const pct = total > 0 ? (known / total * 100) : 0;
    const bar = document.getElementById('bar-' + level);
    const text = document.getElementById('text-' + level);
    if (bar) bar.style.width = pct + '%';
    if (text) text.textContent = known + ' / ' + total + ' đã nhớ';
  });
}

function goBackToPicker() {
  stopSpeech();
  document.body.classList.remove('study-mode');
  document.getElementById('screenPicker').style.display = '';
  document.getElementById('screenCards').style.display = 'none';
  document.getElementById('appTitle').textContent = 'HSK Flashcards';
  currentLevel = null;
  currentView = 'cards';
  overviewQuery = '';
  overviewStatus = 'all';
  const overlay = document.getElementById('celebrationOverlay');
  if (overlay) overlay.remove();
  renderLevelProgress();
}

async function selectLevel(level) {
  celebrationShown = false;
  currentLevel = level;
  document.body.classList.add('study-mode');
  WORDS = [];
  currentView = 'cards';
  overviewQuery = '';
  overviewStatus = 'all';
  document.getElementById('appTitle').textContent = LEVELS[level].label + ' Flashcards';
  document.getElementById('transferPanel').hidden = true;
  document.getElementById('screenPicker').style.display = 'none';
  document.getElementById('screenCards').style.display = '';
  document.getElementById('overviewTab').disabled = true;
  setViewMode('cards');
  document.getElementById('cardArea').innerHTML = `
    <div class="skel-bar"></div>
    <div class="skel-card">
      <div class="skel-line skel-hanzi"></div>
      <div class="skel-line skel-pinyin"></div>
      <div class="skel-line skel-hint"></div>
    </div>
    <div class="skel-nav">
      <div class="skel-line skel-nav-btn"></div>
      <div class="skel-line skel-nav-mid"></div>
      <div class="skel-line skel-nav-btn"></div>
    </div>
    <div class="skel-actions">
      <div class="skel-line skel-action-btn"></div>
      <div class="skel-line skel-action-btn"></div>
    </div>`;

  // Yield to the browser's paint pipeline so the skeleton renders at least one frame
  // before the fetch begins — necessary for local file:// loads where fetch is instant.
  await new Promise(r => requestAnimationFrame(r));
  await new Promise(r => requestAnimationFrame(r));

  try {
    const res = await fetch(LEVELS[level].dataUrl);
    if (!res.ok) throw new Error('fetch failed');
    WORDS = await res.json();
  } catch (e) {
    document.getElementById('cardArea').innerHTML = '<div class="error-text">Không thể tải dữ liệu. Vui lòng thử lại.</div>';
    return;
  }

  document.getElementById('overviewTab').disabled = false;
  order = Array.from({length: WORDS.length}, (_, i) => i);
  progress = {};
  showPinyin = true;
  currentFilter = 'all';
  idx = 0;

  loadState();
  buildCardArea();
  renderFilters();
  render();
  setViewMode('cards');
}
