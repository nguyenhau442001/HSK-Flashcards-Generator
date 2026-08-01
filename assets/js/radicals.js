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
    const [basic50, ...groups] = await Promise.all([
      fetchJson(RADICAL_BASIC50_URL),
      ...Array.from({ length: RADICAL_STROKE_COUNT }, (_, i) => fetchJson(radicalStrokeUrl(i + 1))),
    ]);
    RADICAL_BASIC50 = basic50;
    RADICAL_STROKE_GROUPS = groups;
    radicalDataLoaded = true;
  } catch (e) {
    hub.innerHTML = '<div class="error-text">Không thể tải dữ liệu. Vui lòng thử lại.</div>';
    return;
  }
  renderRadicalHub();
}

function setPrimaryTab(tab) {
  primaryTab = tab;
  document.getElementById('primaryTabVocab').classList.toggle('active', tab === 'vocab');
  document.getElementById('primaryTabRadicals').classList.toggle('active', tab === 'radicals');
  document.getElementById('primaryTabVocab').setAttribute('aria-selected', String(tab === 'vocab'));
  document.getElementById('primaryTabRadicals').setAttribute('aria-selected', String(tab === 'radicals'));
  document.getElementById('screenPicker').style.display = tab === 'vocab' ? '' : 'none';
  document.getElementById('screenRadicalHub').style.display = tab === 'radicals' ? '' : 'none';
  if (tab === 'radicals') ensureRadicalDataLoaded();
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
      <div class="radical-panel-card">
        <h2>50 BỘ THỦ CƠ BẢN</h2>
        <p class="radical-panel-subtitle">Dành cho người mới bắt đầu</p>
        <div class="radical-panel-progress" id="basic50Progress"></div>
        <button class="quick-study-btn radical-start-btn" onclick="startRadicalStudy('basic50')">Bắt đầu học 50 bộ →</button>
      </div>
    </div>

    <div id="radicalKangxi214Panel" class="radical-panel" hidden>
      <h2>214 BỘ THỦ KHANG HY</h2>
      <p class="radical-panel-subtitle">Đầy đủ 214 bộ · phân loại từ 1–17 nét</p>
      <div class="radical-group-grid" id="radicalGroupGrid"></div>
    </div>
  `;
  setRadicalTab(radicalTab);
  renderRadicalHubProgress();
}

function renderRadicalHubProgress() {
  const basicProgress = document.getElementById('basic50Progress');
  if (basicProgress) {
    const known = radicalKnownCount(RADICAL_BASIC50);
    basicProgress.textContent = `${known} / ${RADICAL_BASIC50.length} đã nhớ`;
  }
  const grid = document.getElementById('radicalGroupGrid');
  if (grid) {
    grid.innerHTML = RADICAL_STROKE_GROUPS.map((group, i) => {
      const strokeNum = i + 1;
      const preview = group.slice(0, 4).map(item => item.radical).join(' ');
      const known = radicalKnownCount(group);
      return `
        <button class="radical-group-card" type="button" onclick="startRadicalStudy('kangxi214', ${i})">
          <div class="radical-group-stroke">${strokeNum} NÉT</div>
          <div class="radical-group-preview">${preview}</div>
          <div class="radical-group-count">${group.length} bộ</div>
          <div class="radical-group-known">${known} / ${group.length} nhớ</div>
        </button>`;
    }).join('');
  }
}

function startRadicalStudy(mode, groupIndex) {
  radicalReturnTab = mode;
  radicalWords = mode === 'basic50' ? RADICAL_BASIC50 : RADICAL_STROKE_GROUPS[groupIndex];
  radicalOrder = Array.from({ length: radicalWords.length }, (_, i) => i);
  radicalIdx = 0;
  document.getElementById('primaryTabs').style.display = 'none';
  document.getElementById('learningDashboard').style.display = 'none';
  document.getElementById('screenRadicalHub').style.display = 'none';
  document.getElementById('screenRadicalCards').style.display = '';
  document.body.classList.add('study-mode');
  buildRadicalCardArea();
  renderRadicalCard();
}

function goBackToRadicalHub() {
  document.body.classList.remove('study-mode');
  document.getElementById('screenRadicalCards').style.display = 'none';
  document.getElementById('screenRadicalHub').style.display = '';
  document.getElementById('primaryTabs').style.display = '';
  document.getElementById('learningDashboard').style.display = '';
  radicalTab = radicalReturnTab;
  renderRadicalHub();
}
