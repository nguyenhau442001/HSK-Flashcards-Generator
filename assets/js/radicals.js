// Radical hub: primary/secondary tab switching, data loading, hub rendering.
async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error('fetch failed: ' + url);
  return res.json();
}

async function ensureRadicalDataLoaded() {
  if (radicalDataLoaded) { renderRadicalHub(); return; }
  const hub = document.getElementById('radicalHub');
  hub.innerHTML = '<div class="loading-text">Đang tải dữ liệu...</div>';
  try {
    const [basic50Groups, kangxi214Groups] = await Promise.all([
      Promise.all(Array.from({ length: RADICAL_STROKE_COUNTS.basic50 }, (_, i) => fetchJson(radicalStrokeUrl('basic50', i + 1)))),
      Promise.all(Array.from({ length: RADICAL_STROKE_COUNTS.kangxi214 }, (_, i) => fetchJson(radicalStrokeUrl('kangxi214', i + 1)))),
    ]);
    RADICAL_GROUPS.basic50 = basic50Groups;
    RADICAL_GROUPS.kangxi214 = kangxi214Groups;
    radicalDataLoaded = true;
  } catch (e) {
    hub.innerHTML = '<div class="error-text">Không thể tải dữ liệu. Vui lòng thử lại.</div>';
    return;
  }
  renderRadicalHub();
}

function setPrimaryTab(tab) {
  const previousTab = primaryTab;
  primaryTab = tab;
  document.getElementById('primaryTabVocab').classList.toggle('active', tab === 'vocab');
  document.getElementById('primaryTabRadicals').classList.toggle('active', tab === 'radicals');
  document.getElementById('primaryTabReview').classList.toggle('active', tab === 'review');
  document.getElementById('primaryTabVocab').setAttribute('aria-selected', String(tab === 'vocab'));
  document.getElementById('primaryTabRadicals').setAttribute('aria-selected', String(tab === 'radicals'));
  document.getElementById('primaryTabReview').setAttribute('aria-selected', String(tab === 'review'));
  document.getElementById('screenPicker').style.display = tab === 'vocab' ? '' : 'none';
  document.getElementById('screenRadicalHub').style.display = tab === 'radicals' ? '' : 'none';
  document.getElementById('screenReviewPicker').style.display = tab === 'review' ? '' : 'none';
  if (tab === 'radicals') ensureRadicalDataLoaded();
  if (tab === 'review') {
    updateReviewRangeLabel(document.getElementById('reviewRangeSlider').value);
  }
  if (previousTab === 'review' && tab !== 'review') {
    abandonReviewSession();
  }
}

function setRadicalTab(tab) {
  radicalTab = tab;
  const basicTab = document.getElementById('radicalTabBasic50');
  const kangxiTab = document.getElementById('radicalTabKangxi214');
  const basicPanel = document.getElementById('radicalBasic50Panel');
  const kangxiPanel = document.getElementById('radicalKangxi214Panel');
  if (!basicTab) return;
  basicTab.classList.toggle('active', tab === 'basic50');
  kangxiTab.classList.toggle('active', tab === 'kangxi214');
  basicTab.setAttribute('aria-selected', String(tab === 'basic50'));
  kangxiTab.setAttribute('aria-selected', String(tab === 'kangxi214'));
  basicPanel.hidden = tab !== 'basic50';
  kangxiPanel.hidden = tab !== 'kangxi214';
}

function radicalKnownCount(items) {
  return items.filter(item => radicalProgress[radicalProgressKey(item)] === 'known').length;
}

function renderRadicalHub() {
  const hub = document.getElementById('radicalHub');
  hub.innerHTML = `
    <div class="radical-tabs view-tabs" role="tablist" aria-label="Bộ Bộ thủ">
      <button id="radicalTabBasic50" class="view-tab active" role="tab" aria-selected="true" onclick="setRadicalTab('basic50')">50 bộ cơ bản</button>
      <button id="radicalTabKangxi214" class="view-tab" role="tab" aria-selected="false" onclick="setRadicalTab('kangxi214')">214 bộ Khang Hy</button>
    </div>

    <div id="radicalBasic50Panel" class="radical-panel">
      <div class="radical-panel-header">
        <div>
          <h2>50 BỘ THỦ CƠ BẢN</h2>
          <p class="radical-panel-subtitle">Dành cho người mới bắt đầu · phân loại từ 1–10 nét</p>
        </div>
        <button type="button" class="radical-overview-btn" onclick="openRadicalOverviewFromHub('basic50')">📋 Tổng quan 50 bộ</button>
      </div>
      <div class="radical-group-grid" id="radicalGroupGridBasic50"></div>
    </div>

    <div id="radicalKangxi214Panel" class="radical-panel" hidden>
      <div class="radical-panel-header">
        <div>
          <h2>214 BỘ THỦ KHANG HY</h2>
          <p class="radical-panel-subtitle">Đầy đủ 214 bộ · phân loại từ 1–17 nét</p>
        </div>
        <button type="button" class="radical-overview-btn" onclick="openRadicalOverviewFromHub('kangxi214')">📋 Tổng quan 214 bộ</button>
      </div>
      <div class="radical-group-grid" id="radicalGroupGridKangxi214"></div>
    </div>
  `;
  setRadicalTab(radicalTab);
  renderRadicalHubProgress();
}

function renderRadicalGroupGrid(set, gridId) {
  const grid = document.getElementById(gridId);
  if (!grid) return;
  grid.innerHTML = RADICAL_GROUPS[set].map((group, i) => {
    const strokeNum = i + 1;
    // Keep previews identical between both tabs for the shared 1–10 stroke groups.
    // The basic set is the canonical preview; group counts and study decks stay separate.
    const previewGroup = RADICAL_GROUPS.basic50[i]?.length
      ? RADICAL_GROUPS.basic50[i]
      : group;
    const preview = previewGroup.slice(0, 4).map(item => item.radical).join(' ');
    const known = radicalKnownCount(group);
    return `
      <button class="radical-group-card" type="button" onclick="startRadicalStudy('${set}', ${i})">
        <div class="radical-group-stroke">${strokeNum} NÉT</div>
        <div class="radical-group-preview">${preview}</div>
        <div class="radical-group-count">${group.length} bộ</div>
        <div class="radical-group-known">${known} / ${group.length} nhớ</div>
      </button>`;
  }).join('');
}

function renderRadicalHubProgress() {
  renderRadicalGroupGrid('basic50', 'radicalGroupGridBasic50');
  renderRadicalGroupGrid('kangxi214', 'radicalGroupGridKangxi214');
}

function buildRadicalOverviewItems(mode) {
  const groups = RADICAL_GROUPS[mode];
  const items = [];
  groups.forEach((group, groupIndex) => {
    group.forEach((item, itemIndexInGroup) => {
      items.push({ item, groupIndex, itemIndexInGroup, stroke: groupIndex + 1 });
    });
  });
  return items;
}

function startRadicalStudy(mode, groupIndex, options) {
  const openOverview = !!(options && options.overview);
  radicalReturnTab = mode;
  radicalGroupIndex = groupIndex;
  radicalWords = RADICAL_GROUPS[mode][groupIndex];
  radicalOrder = Array.from({ length: radicalWords.length }, (_, i) => i);
  radicalFilteredOrder = radicalOrder.slice();
  radicalIdx = 0;
  radicalCurrentFilter = 'all';
  radicalCurrentView = 'cards';
  radicalOverviewQuery = '';
  radicalOverviewStatus = 'all';
  radicalOverviewStroke = 'all';
  radicalOverviewItems = buildRadicalOverviewItems(mode);
  document.getElementById('primaryTabs').style.display = 'none';
  document.getElementById('learningDashboard').style.display = 'none';
  document.getElementById('screenRadicalHub').style.display = 'none';
  document.getElementById('screenRadicalCards').style.display = '';
  document.getElementById('radicalTransferPanel').hidden = true;
  document.body.classList.add('study-mode');
  buildRadicalCardArea();
  renderRadicalFilters();
  setRadicalViewMode(openOverview ? 'overview' : 'cards');
  renderRadicalCard();
}

function openRadicalOverviewFromHub(mode) {
  startRadicalStudy(mode, 0, { overview: true });
}

function goBackToRadicalHub() {
  document.body.classList.remove('study-mode');
  document.getElementById('screenRadicalCards').style.display = 'none';
  document.getElementById('screenRadicalHub').style.display = '';
  document.getElementById('primaryTabs').style.display = '';
  document.getElementById('learningDashboard').style.display = '';
  document.getElementById('appTitle').textContent = 'HSK Flashcards';
  radicalTab = radicalReturnTab;
  radicalCurrentView = 'cards';
  renderRadicalHub();
}
