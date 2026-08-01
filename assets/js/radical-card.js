// Radical flashcard rendering, flip interaction, and progress actions.
function buildRadicalCardArea() {
  document.getElementById('radicalCardArea').innerHTML = `
    <div class="progress-bar-track">
      <div class="progress-bar-fill" id="radicalProgressBar"></div>
    </div>
    <div class="card radical-card" id="radicalCard" onclick="radicalFlip()">
      <div id="radicalCardContent" class="card-content">
        <div class="hanzi radical-char" id="radChar"></div>
        <div class="radical-name" id="radName"></div>
        <div class="pinyin" id="radPinyin"></div>
        <div class="radical-back" id="radicalBack">
          <div class="radical-meaning" id="radMeaning"></div>
          <div class="radical-description" id="radDescription" hidden></div>
          <div class="radical-variants" id="radVariants" hidden></div>
          <div class="radical-examples" id="radExamples" hidden></div>
        </div>
        <div class="hint" id="radicalHint">Nhấn vào thẻ để xem nghĩa và ví dụ</div>
      </div>
    </div>

    <div class="nav-row">
      <button onclick="event.stopPropagation(); prevRadicalCard()">← Trước</button>
      <span class="progress-text" id="radicalProgressText">1 / ${radicalWords.length}</span>
      <button onclick="event.stopPropagation(); nextRadicalCard()">Tiếp →</button>
    </div>

    <div class="action-row">
      <button class="btn-unknown" onclick="event.stopPropagation(); markRadicalUnknown()">Chưa nhớ</button>
      <button class="btn-known" onclick="event.stopPropagation(); markRadicalKnown()">Đã nhớ</button>
    </div>
  `;
  const btn = document.getElementById('radicalPinyinToggle');
  if (btn) {
    btn.textContent = showRadicalPinyin ? '👁 Đang hiện pinyin' : '🙈 Chế độ thử thách: ẩn pinyin';
    btn.classList.toggle('on', !showRadicalPinyin);
  }
}

function radicalRelationLabel(type) {
  if (type === 'semantic') return 'Gợi nghĩa';
  if (type === 'phonetic') return 'Gợi âm';
  if (type === 'historical_graphic') return 'Cấu tạo/lịch sử';
  return type || '';
}

function renderRadicalCard(animate) {
  const content = document.getElementById('radicalCardContent');
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function applyContent() {
    if (content) content.className = 'card-content';
    const back = document.getElementById('radicalBack');
    if (back) back.classList.remove('show');
    document.getElementById('radicalHint').textContent = 'Nhấn vào thẻ để xem nghĩa và ví dụ';

    if (radicalWords.length === 0) {
      document.getElementById('radChar').textContent = '';
      document.getElementById('radName').textContent = '';
      document.getElementById('radPinyin').textContent = '';
      document.getElementById('radMeaning').textContent = 'Không có bộ thủ nào';
      document.getElementById('radicalHint').textContent = '';
      updateRadicalProgress(0, 0);
      return;
    }

    const item = radicalWords[radicalOrder[radicalIdx % radicalOrder.length]];
    document.getElementById('radChar').textContent = item.radical || '';
    document.getElementById('radName').textContent = item.name || '';
    document.getElementById('radPinyin').textContent = showRadicalPinyin ? (item.pinyin || '') : '';
    document.getElementById('radMeaning').textContent = item.meaning || '';

    const descNode = document.getElementById('radDescription');
    descNode.hidden = !item.description;
    descNode.textContent = item.description || '';

    const variantsNode = document.getElementById('radVariants');
    if (Array.isArray(item.variants) && item.variants.length) {
      variantsNode.hidden = false;
      variantsNode.innerHTML = '<div class="ex-label">Dị thể</div>' +
        item.variants.map(v => `<span class="variant-chip">${v}</span>`).join('');
    } else {
      variantsNode.hidden = true;
      variantsNode.innerHTML = '';
    }

    const examplesNode = document.getElementById('radExamples');
    if (Array.isArray(item.examples) && item.examples.length) {
      examplesNode.hidden = false;
      examplesNode.innerHTML = '<div class="ex-label">Ví dụ</div>' + item.examples.map(ex => `
        <div class="radical-example">
          <div class="ex-line ex-zh">${ex.hanzi || ''}</div>
          ${showRadicalPinyin && ex.pinyin ? `<div class="ex-line ex-py">${ex.pinyin}</div>` : ''}
          <div class="ex-line ex-vi">${ex.meaning || ''}</div>
          ${ex.relation ? `<div class="radical-relation"><span class="relation-badge">${radicalRelationLabel(ex.relation_type)}</span>${ex.relation}</div>` : ''}
        </div>`).join('');
    } else {
      examplesNode.hidden = true;
      examplesNode.innerHTML = '';
    }

    updateRadicalProgress(radicalIdx % radicalOrder.length + 1, radicalOrder.length);

    if (animate && content && !prefersReduced) {
      if (animate === 'next') content.classList.add('enter-right');
      else if (animate === 'prev') content.classList.add('enter-left');
      else content.classList.add('enter-fade');
    }
  }

  if (!animate || !content || prefersReduced) { applyContent(); return; }

  content.className = 'card-content';
  if (animate === 'next') content.classList.add('exit-left');
  else if (animate === 'prev') content.classList.add('exit-right');
  else content.classList.add('exit-fade');

  setTimeout(applyContent, 150);
}

function updateRadicalProgress(current, total) {
  const text = document.getElementById('radicalProgressText');
  if (text) text.textContent = total === 0 ? '0 / 0' : current + ' / ' + total;
  const bar = document.getElementById('radicalProgressBar');
  if (bar) bar.style.width = (total === 0 ? 0 : (current / total * 100)) + '%';
}

function radicalFlip() {
  if (radicalWords.length === 0) return;
  const back = document.getElementById('radicalBack');
  const willShow = !back.classList.contains('show');
  back.classList.toggle('show', willShow);
  document.getElementById('radicalHint').textContent = willShow ? 'Nhấn lại để ẩn' : 'Nhấn vào thẻ để xem nghĩa và ví dụ';
}

function nextRadicalCard() {
  if (radicalOrder.length === 0) return;
  radicalIdx = (radicalIdx + 1) % radicalOrder.length;
  renderRadicalCard('next');
}
function prevRadicalCard() {
  if (radicalOrder.length === 0) return;
  radicalIdx = (radicalIdx - 1 + radicalOrder.length) % radicalOrder.length;
  renderRadicalCard('prev');
}
function markRadicalKnown() {
  if (radicalWords.length === 0) return;
  const item = radicalWords[radicalOrder[radicalIdx % radicalOrder.length]];
  radicalProgress[radicalProgressKey(item)] = 'known';
  saveRadicalProgress();
  nextRadicalCard();
}
function markRadicalUnknown() {
  if (radicalWords.length === 0) return;
  const item = radicalWords[radicalOrder[radicalIdx % radicalOrder.length]];
  radicalProgress[radicalProgressKey(item)] = 'unknown';
  saveRadicalProgress();
  nextRadicalCard();
}
function shuffleRadicalDeck() {
  shuffleArray(radicalOrder);
  radicalIdx = 0;
  renderRadicalCard('fade');
}
function toggleRadicalPinyin() {
  showRadicalPinyin = !showRadicalPinyin;
  const btn = document.getElementById('radicalPinyinToggle');
  if (btn) {
    btn.textContent = showRadicalPinyin ? '👁 Đang hiện pinyin' : '🙈 Chế độ thử thách: ẩn pinyin';
    btn.classList.toggle('on', !showRadicalPinyin);
  }
  saveRadicalPrefs();
  renderRadicalCard();
}
