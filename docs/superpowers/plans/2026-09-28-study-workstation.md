# Study Workstation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor the HSK Flashcards app into a responsive 3-column "Study Workstation" desktop layout (Reference Dock / Core Learning Hub / Interactive Study Lab) with active-word sync across columns, while keeping a clean single-column mobile experience and the existing dark/light theme.

**Architecture:** A `.workstation` CSS Grid wraps the app's existing content, 3 columns only above 1025px, 1 column below with the same DOM re-flowing via `grid-template-areas` and a `matchMedia`-driven class toggle. New sidebar features are new plain-global-JS modules that follow the codebase's existing script-tag-ordered, no-build convention, syncing through one new pub/sub pair in `state.js` (`setActiveStudyWord` / `onActiveWordChange`).

**Tech Stack:** Vanilla HTML/CSS/JS, no build step, no framework. New external dependency: Hanzi Writer (loaded from `cdn.jsdelivr.net`).

**Spec:** `docs/superpowers/specs/2026-09-28-study-workstation-design.md`

## Global Constraints

- No new JS framework or state-management library — follow the existing plain-global-variable, ordered-`<script>`-tag module pattern.
- No new CSS custom properties/tokens — new UI must consume existing `--*` tokens from `assets/css/base.css` so the dark/light theme toggle (`theme.js`) applies for free.
- Desktop 3-column layout activates only above 1025px; mobile/tablet (<1025px) stays single column.
- Desktop grid: `max-width: 1440px`, centered, columns `25% / 50% / 25%`.
- Left-sidebar search index covers HSK1–6 (2.0) only — not HSK 3.0, not topic decks.
- Search popover shows Hanzi, Pinyin, Vietnamese meaning, HSK level — no Hán-Việt field (does not exist in the data).
- Radicals quick filter reuses existing `database/radicals/*` data and `radicalStrokeUrl()` loader from `assets/js/radicals-state.js` — do not duplicate radical data.
- The existing dedicated "Bộ thủ" primary tab (`radicals.js`, `radicals-state.js`, `radical-card.js`) stays untouched and fully functional.
- Grammar breakdown data is a curated starter set only (~30-50 HSK1-2 sentences) — not full-corpus coverage. Words outside the starter set must show a placeholder, never a blank/broken panel.
- Hanzi Writer stroke data comes from its CDN on demand — no local stroke data files.
- No JS test framework exists in this repo (no `package.json`, no test runner). Verification is done by opening `flashcards.html` in a real browser (Playwright MCP tools: `browser_navigate`, `browser_snapshot`, `browser_evaluate`, `browser_console_messages`, `browser_resize`) and checking behavior/DOM/console directly. Every task's "test" step is a browser-driven check, not a unit test file.
- After implementation of any task, run `git diff --check` before committing to catch stray whitespace/conflict markers (matches this project's existing verification habits).

## Review Focus

- **Empty/short filter results** — user searches a query that matches zero words (e.g. Latin letters, punctuation): the search popover must show a "not found" state, never an empty popover or a JS error from indexing an empty array.
- **Rapid word switching** — user clicks through several words quickly (search result → radical example → weak word) before the stroke canvas or grammar panel finishes rendering the previous word: the last click must win, with no leaked Hanzi Writer instances or mismatched panel content.
- **Word with no starter-set grammar data** — the overwhelming majority of vocab words are outside the ~30-50 word starter set: the grammar panel must render its placeholder message correctly for every level (HSK1 through HSK6), not just assume HSK1-2 words are always covered.
- **Mobile ↔ desktop resize mid-session** — user resizes the browser (or rotates a tablet) across the 1025px breakpoint while a word is active and a dialog/accordion is open: no duplicated content, no orphaned open dialogs, active word stays synced across the layout change.
- **Offline / CDN-blocked Hanzi Writer** — the stroke canvas depends on a third-party CDN fetch per character; if it fails (network blocked, character not covered), the canvas must show the documented fallback message, not a blank box or uncaught promise rejection in the console.

---

## File Structure

**New files:**
- `assets/js/sidebar-search.js` — search index build (HSK1-6 2.0 only), debounced input handling, popover rendering, tone-insensitive matching helper.
- `assets/js/sidebar-radicals-filter.js` — compact stroke-count filter grid in the left sidebar, reusing `RADICAL_STROKE_COUNTS`/`radicalStrokeUrl` from `radicals-state.js`.
- `assets/js/weak-words.js` — `localStorage`-backed starred/weak words list, ★ toggle wiring, sidebar list rendering.
- `assets/js/stroke-canvas.js` — Hanzi Writer integration, 田-grid container, animate/quiz controls, active-word subscription.
- `assets/js/grammar-breakdown.js` — starter-set lookup, S/V/O/M color-coded rendering, grammar-note card, placeholder state.
- `assets/css/workstation.css` — grid shell, breakpoints, left/right panel base layout, mobile dialog/accordion presentation rules.
- `assets/css/sidebar-lab.css` — stroke canvas + grammar breakdown panel styling (田-grid, control buttons, role-color spans, note card).
- `database/grammar/starter_sentences.json` — curated grammar dataset.

**Modified files:**
- `flashcards.html` — new grid wrapper markup (`.workstation`, `.workstation-left`, `.workstation-middle`, `.workstation-right`), new stylesheet `<link>`s, Hanzi Writer CDN `<script>`, new module `<script>` tags (after existing ones, respecting load order — sidebar/lab modules depend on `state.js` sync primitives and on `radicals-state.js` for the radicals filter).
- `assets/js/state.js` — add `activeStudyWord`, `activeWordListeners`, `onActiveWordChange()`, `setActiveStudyWord()`.
- `assets/js/flashcard.js` — one-line call to `setActiveStudyWord(w)` inside `render()`'s `applyContent()` (around line 146, right after `const w = WORDS[wIdx];`), plus a matching call in the empty-filter branch reset (`setActiveStudyWord(null)`).

**Untouched (verified reused, not duplicated):** `radicals.js`, `radicals-state.js`, `radical-card.js`, `database/radicals/*`.

---

## Task 1: Workstation grid shell + responsive breakpoint

**Files:**
- Create: `assets/css/workstation.css`
- Modify: `flashcards.html:15-16` (add stylesheet link), `flashcards.html:20-21` (wrap body content in grid divs), `flashcards.html:413` (close wrapper), `flashcards.html:415-434` (add script tag, see Task 6 for exact placement)

**Interfaces:**
- Produces: `.workstation`, `.workstation-left`, `.workstation-middle`, `.workstation-right` CSS classes; a `body` class toggle `is-desktop-dock` (≥1025px) vs `is-mobile-drawer` (<1025px) driven by a `matchMedia` listener defined inline in `workstation.css`'s companion script (added in this task as an inline `<script>` in `flashcards.html`, since it must run before other modules paint).
- Consumes: nothing new yet (later tasks populate `.workstation-left`/`.workstation-right`).

- [ ] **Step 1: Add the breakpoint-detection script and empty left/right panel containers, wrap existing content in the middle column**

Edit `flashcards.html`. Change line 20-21 from:
```html
<body>
<div class="app">
```
to:
```html
<body>
<script>(function(){
  var mq = window.matchMedia('(min-width: 1025px)');
  function applyLayoutMode(e){
    document.body.classList.toggle('is-desktop-dock', e.matches);
    document.body.classList.toggle('is-mobile-drawer', !e.matches);
  }
  applyLayoutMode(mq);
  mq.addEventListener('change', applyLayoutMode);
})();</script>
<div class="app">
  <div class="workstation">
    <aside class="workstation-left" id="workstationLeft" aria-label="Tra cứu nhanh"></aside>
    <div class="workstation-middle" id="workstationMiddle">
```
This script must be the first thing inside `<body>` (before `document.body` is used) so the layout-mode class is set before any module reads it on `DOMContentLoaded`.

Then at line 413 (currently `</div>` closing `.app`, right after the `</footer>`), change:
```html
  </footer>
</div>
```
to:
```html
  </footer>
    </div>
    <aside class="workstation-right" id="workstationRight" aria-label="Phòng thực hành tương tác"></aside>
  </div>
</div>
```

This nests everything from `.app-header` through `.app-footer` inside `#workstationMiddle`, and adds two empty sibling `<aside>` elements that later tasks populate.

- [ ] **Step 2: Add the grid CSS**

Create `assets/css/workstation.css`:
```css
.workstation {
  display: grid;
  grid-template-columns: 1fr;
  max-width: 1440px;
  margin: 0 auto;
}

.workstation-left,
.workstation-right {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

@media (min-width: 1025px) {
  .workstation {
    grid-template-columns: 25% 50% 25%;
    grid-template-areas: "left middle right";
    align-items: start;
    gap: 24px;
  }
  .workstation-left   { grid-area: left; position: sticky; top: 16px; }
  .workstation-middle { grid-area: middle; min-width: 0; }
  .workstation-right  { grid-area: right; position: sticky; top: 16px; }
}

/* Mobile/tablet: left panel content is relocated into a dialog by
   sidebar-search.js / sidebar-radicals-filter.js / weak-words.js;
   right panel content is relocated into <details> accordions by
   stroke-canvas.js / grammar-breakdown.js. Those modules read
   document.body.classList.contains('is-desktop-dock') to decide
   which container to render into. */
```

- [ ] **Step 3: Add the stylesheet link**

In `flashcards.html`, after line 16 (`<link rel="stylesheet" href="assets/css/fast-review-picker.css?v=20260828">`), add:
```html
<link rel="stylesheet" href="assets/css/workstation.css?v=20260928">
```

- [ ] **Step 4: Verify in browser at desktop width**

Run: `browser_navigate` to the local `flashcards.html` file (e.g. `file:///Users/haunguyen/GitHub/HSK-Flashcards-Generator/flashcards.html`), then `browser_resize` to `1440x900`, then `browser_evaluate`:
```js
() => ({
  bodyClasses: document.body.className,
  gridCols: getComputedStyle(document.querySelector('.workstation')).gridTemplateColumns,
})
```
Expected: `bodyClasses` includes `is-desktop-dock`; `gridCols` reports three column widths roughly matching 25%/50%/25% of the viewport (allow rendering rounding).

- [ ] **Step 5: Verify in browser at mobile width**

`browser_resize` to `375x800`, then `browser_evaluate` the same snippet.
Expected: `bodyClasses` includes `is-mobile-drawer`; `gridCols` reports a single column (one value).

- [ ] **Step 6: Verify existing app still works unchanged**

`browser_snapshot` and confirm the app header, primary tabs, and level grid render exactly as before (visually unchanged, just re-parented). Check `browser_console_messages` for no new errors.

- [ ] **Step 7: Commit**

```bash
git add flashcards.html assets/css/workstation.css
git commit -m "feat(workstation): add responsive 3-column grid shell"
```

---

## Task 2: Active-word sync primitives in state.js

**Files:**
- Modify: `assets/js/state.js` (append near end of file, after line 152)
- Modify: `assets/js/flashcard.js:144-156` (hook into `render()`)

**Interfaces:**
- Produces: `let activeStudyWord` (object or `null`), `function onActiveWordChange(fn)`, `function setActiveStudyWord(word)` — global functions available to all later-loaded scripts.
- Consumes: existing globals `WORDS`, `filteredOrder`, `idx` from `state.js`.

- [ ] **Step 1: Add sync primitives to state.js**

Append to `assets/js/state.js`:
```js
let activeStudyWord = null;
const activeWordListeners = [];

function onActiveWordChange(fn) {
  activeWordListeners.push(fn);
}

function setActiveStudyWord(word) {
  activeStudyWord = word;
  activeWordListeners.forEach(fn => {
    try { fn(word); } catch (e) { /* one listener's failure must not block others */ }
  });
}
```

- [ ] **Step 2: Hook the flashcard render path**

In `assets/js/flashcard.js`, inside `render()`'s `applyContent()`, the empty-filter branch (around line 132-142) currently `return`s without touching `activeStudyWord`. Add `setActiveStudyWord(null);` right before that `return`:
```js
    if (filteredOrder.length === 0) {
      document.getElementById('hanzi').textContent = '';
      document.getElementById('pinyin').textContent = '';
      document.getElementById('meaning').textContent = 'Không có từ trong bộ lọc này';
      document.getElementById('meaning').classList.add('show');
      document.getElementById('hint').textContent = '';
      if (content) content.classList.add('is-empty');
      updateProgress(0, 0);
      updateStats();
      setActiveStudyWord(null);
      return;
    }
```

Then, right after `const w = WORDS[wIdx];` (line 145), add:
```js
    const wIdx = filteredOrder[idx % filteredOrder.length];
    const w = WORDS[wIdx];
    setActiveStudyWord(w);
```

- [ ] **Step 3: Verify via browser**

`browser_navigate` to `flashcards.html`, click into HSK1 flashcards (quick-start button), then `browser_evaluate`:
```js
() => (typeof activeStudyWord === 'object' && activeStudyWord !== null) ? activeStudyWord.hanzi : activeStudyWord
```
Expected: returns the hanzi string of the first HSK1 word (爱), matching what's shown on screen.

Then click "🔀 Xáo trộn" (shuffle) or navigate to the next card (swipe/click), re-run the same evaluate.
Expected: `activeStudyWord.hanzi` changes to match the newly displayed card.

- [ ] **Step 4: Verify listener firing**

`browser_evaluate`:
```js
() => {
  window.__testCalls = [];
  onActiveWordChange(w => window.__testCalls.push(w && w.hanzi));
  setActiveStudyWord({ hanzi: '测试' });
  return window.__testCalls;
}
```
Expected: `["测试"]`.

- [ ] **Step 5: Commit**

```bash
git add assets/js/state.js assets/js/flashcard.js
git commit -m "feat(workstation): add active-word sync primitives"
```

---

## Task 3: Left sidebar — instant search

**Files:**
- Create: `assets/js/sidebar-search.js`
- Modify: `flashcards.html` (script tag + panel mount markup, see Task 6)

**Interfaces:**
- Consumes: `LEVELS` object from `state.js` (`LEVELS[key].dataUrl`, `LEVELS[key].version`, `LEVELS[key].label`), `hskLevelKeys()` from `state.js`, `setActiveStudyWord(word)` from Task 2.
- Produces: `function initSidebarSearch()` (called once on DOMContentLoaded from `flashcards.html`'s init sequence), renders into `#sidebarSearchMount` (a container this task creates inside `#workstationLeft` via JS, since `#workstationLeft` starts empty per Task 1).

- [ ] **Step 1: Write the search index builder and matcher**

Create `assets/js/sidebar-search.js`:
```js
// Left sidebar: debounced instant search across HSK1-6 (2.0) vocab.
let sidebarSearchIndex = null;
let sidebarSearchIndexPromise = null;

const TONE_MARKS = {
  'ā':'a','á':'a','ǎ':'a','à':'a',
  'ē':'e','é':'e','ě':'e','è':'e',
  'ī':'i','í':'i','ǐ':'i','ì':'i',
  'ō':'o','ó':'o','ǒ':'o','ò':'o',
  'ū':'u','ú':'u','ǔ':'u','ù':'u',
  'ǖ':'v','ǘ':'v','ǚ':'v','ǜ':'v','ü':'v',
};
function stripTones(s) {
  return String(s).toLowerCase().replace(/[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]/g, ch => TONE_MARKS[ch] || ch);
}

function buildSidebarSearchIndex() {
  if (sidebarSearchIndexPromise) return sidebarSearchIndexPromise;
  const levelKeys = hskLevelKeys(); // HSK1-6 (2.0) only, excludes topics + HSK30 by design
  sidebarSearchIndexPromise = Promise.all(
    levelKeys.map(key =>
      fetch(LEVELS[key].dataUrl)
        .then(r => r.json())
        .then(words => words.map(w => ({
          hanzi: w.hanzi,
          pinyin: w.pinyin,
          meaning: w.meaning,
          level: LEVELS[key].label,
          pinyinStripped: stripTones(w.pinyin),
        })))
        .catch(() => [])
    )
  ).then(lists => {
    sidebarSearchIndex = lists.flat();
    return sidebarSearchIndex;
  });
  return sidebarSearchIndexPromise;
}

function searchSidebarIndex(query) {
  if (!sidebarSearchIndex || !query.trim()) return [];
  const q = query.trim().toLowerCase();
  const qStripped = stripTones(query);
  return sidebarSearchIndex
    .filter(w =>
      w.hanzi.includes(query.trim()) ||
      w.pinyinStripped.includes(qStripped) ||
      w.meaning.toLowerCase().includes(q)
    )
    .slice(0, 20);
}

function renderSidebarSearchResults(results, container) {
  if (!results.length) {
    container.innerHTML = '<div class="sidebar-search-empty">Không tìm thấy từ nào.</div>';
    container.hidden = false;
    return;
  }
  container.innerHTML = results.map(w => `
    <li class="sidebar-search-result" data-hanzi="${w.hanzi}" tabindex="0">
      <span class="ssr-hanzi">${w.hanzi}</span>
      <span class="ssr-pinyin">${w.pinyin}</span>
      <span class="ssr-level">${w.level}</span>
    </li>
  `).join('');
  container.hidden = false;
}

let sidebarSearchDebounceTimer = null;
function onSidebarSearchInput(value, resultsEl) {
  clearTimeout(sidebarSearchDebounceTimer);
  sidebarSearchDebounceTimer = setTimeout(() => {
    buildSidebarSearchIndex().then(() => {
      const results = searchSidebarIndex(value);
      if (!value.trim()) { resultsEl.hidden = true; resultsEl.innerHTML = ''; return; }
      renderSidebarSearchResults(results, resultsEl);
    });
  }, 300);
}

function initSidebarSearch() {
  const mount = document.getElementById('workstationLeft');
  if (!mount) return;
  const wrap = document.createElement('div');
  wrap.className = 'sidebar-search';
  wrap.innerHTML = `
    <input type="search" id="sidebarSearchInput" class="sidebar-search-input"
      placeholder="Tìm Hán tự, pinyin, nghĩa..." aria-label="Tìm từ vựng">
    <ul id="sidebarSearchResults" class="sidebar-search-results" hidden></ul>
  `;
  mount.appendChild(wrap);

  const input = wrap.querySelector('#sidebarSearchInput');
  const results = wrap.querySelector('#sidebarSearchResults');

  input.addEventListener('input', () => onSidebarSearchInput(input.value, results));
  results.addEventListener('click', e => {
    const li = e.target.closest('.sidebar-search-result');
    if (!li) return;
    const hanzi = li.dataset.hanzi;
    const word = sidebarSearchIndex.find(w => w.hanzi === hanzi);
    if (word) setActiveStudyWord(word);
    results.hidden = true;
  });
}

document.addEventListener('DOMContentLoaded', initSidebarSearch);
```

- [ ] **Step 2: Add sidebar search styles**

Append to `assets/css/workstation.css`:
```css
.sidebar-search { position: relative; }
.sidebar-search-input {
  width: 100%;
  box-sizing: border-box;
  padding: 10px 12px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  background: var(--card-bg);
  color: var(--text-primary);
  font-size: 14px;
}
.sidebar-search-results {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  z-index: 20;
  max-height: 320px;
  overflow-y: auto;
  margin: 0;
  padding: 4px;
  list-style: none;
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}
.sidebar-search-result {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  border-radius: var(--radius-md);
  cursor: pointer;
}
.sidebar-search-result:hover,
.sidebar-search-result:focus {
  background: var(--accent-light);
}
.ssr-hanzi { font-size: 18px; color: var(--text-primary); }
.ssr-pinyin { color: var(--text-secondary); font-size: 13px; }
.ssr-level { margin-left: auto; font-size: 11px; color: var(--text-tertiary); }
.sidebar-search-empty { padding: 12px; color: var(--text-secondary); font-size: 13px; }
```

- [ ] **Step 3: Verify tone-stripping helper directly**

`browser_evaluate`:
```js
() => [stripTones('ài'), stripTones('mǎ'), stripTones('lǜ')]
```
Expected: `["ai", "ma", "lv"]`.

- [ ] **Step 4: Verify empty query and no-match query**

After navigating and letting `initSidebarSearch` run, `browser_evaluate`:
```js
async () => {
  await buildSidebarSearchIndex();
  return [searchSidebarIndex(''), searchSidebarIndex('zzz_no_such_word')];
}
```
Expected: `[[], []]` — both empty arrays, no exceptions.

- [ ] **Step 5: Verify a real match end-to-end in the DOM**

Use `browser_type` to type `"ai"` into `#sidebarSearchInput`, wait ~350ms (debounce), then `browser_snapshot`.
Expected: `#sidebarSearchResults` is visible and contains at least one row with hanzi `爱` (ài, yêu/thích — matches HSK1 entry seen earlier).

Click that result, then `browser_evaluate` `() => activeStudyWord && activeStudyWord.hanzi`.
Expected: `"爱"`.

- [ ] **Step 6: Commit**

```bash
git add assets/js/sidebar-search.js assets/css/workstation.css
git commit -m "feat(workstation): add left sidebar instant search"
```

---

## Task 4: Left sidebar — 214 radicals quick filter

**Files:**
- Create: `assets/js/sidebar-radicals-filter.js`

**Interfaces:**
- Consumes: `RADICAL_STROKE_COUNTS`, `radicalStrokeUrl(set, n)` from `assets/js/radicals-state.js`; `setActiveStudyWord(word)` from Task 2.
- Produces: `function initSidebarRadicalsFilter()`, renders into `#workstationLeft` below the search box.

- [ ] **Step 1: Write the stroke-count filter module**

Create `assets/js/sidebar-radicals-filter.js`:
```js
// Left sidebar: compact 214-radicals quick filter grouped by stroke count.
let sidebarRadicalsCache = {}; // key: `${set}_${strokeCount}` -> array of radical entries

function fetchSidebarRadicalStroke(set, strokeCount) {
  const cacheKey = `${set}_${strokeCount}`;
  if (sidebarRadicalsCache[cacheKey]) return Promise.resolve(sidebarRadicalsCache[cacheKey]);
  return fetch(radicalStrokeUrl(set, strokeCount))
    .then(r => r.json())
    .then(list => { sidebarRadicalsCache[cacheKey] = list; return list; })
    .catch(() => []);
}

function renderSidebarRadicalExamples(radical, container) {
  if (!radical.examples || !radical.examples.length) {
    container.innerHTML = '<div class="sidebar-search-empty">Bộ thủ này chưa có ví dụ.</div>';
    return;
  }
  container.innerHTML = radical.examples.map(ex => `
    <li class="sidebar-search-result" data-hanzi="${ex.hanzi}" tabindex="0">
      <span class="ssr-hanzi">${ex.hanzi}</span>
      <span class="ssr-pinyin">${ex.pinyin}</span>
      <span class="ssr-level">${ex.meaning}</span>
    </li>
  `).join('');
}

function initSidebarRadicalsFilter() {
  const mount = document.getElementById('workstationLeft');
  if (!mount) return;
  const wrap = document.createElement('div');
  wrap.className = 'sidebar-radicals-filter';
  const maxStroke = RADICAL_STROKE_COUNTS.kangxi214;
  const chips = Array.from({ length: maxStroke }, (_, i) => i + 1)
    .map(n => `<button type="button" class="sidebar-stroke-chip" data-stroke="${n}">${n}</button>`)
    .join('');
  wrap.innerHTML = `
    <div class="sidebar-panel-title">214 Bộ thủ</div>
    <div class="sidebar-stroke-chips">${chips}</div>
    <ul class="sidebar-search-results sidebar-radicals-grid" id="sidebarRadicalsGrid"></ul>
    <ul class="sidebar-search-results" id="sidebarRadicalExamples" hidden></ul>
  `;
  mount.appendChild(wrap);

  const grid = wrap.querySelector('#sidebarRadicalsGrid');
  const examplesList = wrap.querySelector('#sidebarRadicalExamples');

  wrap.querySelectorAll('.sidebar-stroke-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      wrap.querySelectorAll('.sidebar-stroke-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const n = Number(chip.dataset.stroke);
      fetchSidebarRadicalStroke('kangxi214', n).then(list => {
        grid.hidden = false;
        examplesList.hidden = true;
        grid.innerHTML = list.map(r => `
          <li class="sidebar-search-result" data-radical="${r.radical}" tabindex="0">
            <span class="ssr-hanzi">${r.radical}</span>
            <span class="ssr-pinyin">${r.pinyin}</span>
            <span class="ssr-level">${r.meaning}</span>
          </li>
        `).join('');
        grid.dataset.strokeList = JSON.stringify(list);
      });
    });
  });

  grid.addEventListener('click', e => {
    const li = e.target.closest('.sidebar-search-result[data-radical]');
    if (!li) return;
    const list = JSON.parse(grid.dataset.strokeList || '[]');
    const radical = list.find(r => r.radical === li.dataset.radical);
    if (radical) renderSidebarRadicalExamples(radical, examplesList);
    examplesList.hidden = false;
  });

  examplesList.addEventListener('click', e => {
    const li = e.target.closest('.sidebar-search-result[data-hanzi]');
    if (!li) return;
    setActiveStudyWord({ hanzi: li.dataset.hanzi, pinyin: '', meaning: '' });
  });
}

document.addEventListener('DOMContentLoaded', initSidebarRadicalsFilter);
```

- [ ] **Step 2: Add styles for the stroke chips**

Append to `assets/css/workstation.css`:
```css
.sidebar-panel-title {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 13px;
  margin-top: 8px;
}
.sidebar-stroke-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.sidebar-stroke-chip {
  border: 1px solid var(--border);
  background: var(--card-bg);
  color: var(--text-secondary);
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 12px;
  cursor: pointer;
}
.sidebar-stroke-chip.active {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}
.sidebar-radicals-grid { position: static; max-height: 240px; }
```

- [ ] **Step 3: Verify stroke-count data loads for a known chip**

`browser_navigate`, then `browser_evaluate`:
```js
async () => {
  const list = await fetchSidebarRadicalStroke('kangxi214', 3);
  return list.length > 0 ? list[0].radical : null;
}
```
Expected: a non-null single-character radical string (stroke-3 kangxi radicals exist per the existing `database/radicals/kangxi_214_radicals/stroke_03.json` file family).

- [ ] **Step 4: Verify click flow in the DOM**

`browser_click` the stroke-3 chip, `browser_snapshot` to confirm `#sidebarRadicalsGrid` populates. Click one radical result, confirm `#sidebarRadicalExamples` populates with that radical's `examples[]`. Click one example, then `browser_evaluate` `() => activeStudyWord && activeStudyWord.hanzi` to confirm it matches the clicked example's hanzi.

- [ ] **Step 5: Commit**

```bash
git add assets/js/sidebar-radicals-filter.js assets/css/workstation.css
git commit -m "feat(workstation): add left sidebar radicals quick filter"
```

---

## Task 5: Left sidebar — starred/weak words + ★ toggle on flashcards

**Files:**
- Create: `assets/js/weak-words.js`
- Modify: `flashcards.html` (add ★ button to the card toolbar, see exact location below)

**Interfaces:**
- Consumes: `setActiveStudyWord(word)`, `onActiveWordChange(fn)`, `activeStudyWord` from Task 2; `currentLevel` global from `state.js`.
- Produces: `function toggleWeakWord(hanzi, level)`, `function isWeakWord(hanzi)`, `function initWeakWordsPanel()`, renders into `#workstationLeft`.

- [ ] **Step 1: Write the weak-words module**

Create `assets/js/weak-words.js`:
```js
// Left sidebar: starred/weak words list, backed by localStorage.
const WEAK_WORDS_KEY = 'hsk_weak_words_v1';

function loadWeakWords() {
  try {
    const raw = localStorage.getItem(WEAK_WORDS_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (e) { return []; }
}

function saveWeakWords(list) {
  try { localStorage.setItem(WEAK_WORDS_KEY, JSON.stringify(list)); } catch (e) {}
}

function isWeakWord(hanzi) {
  return loadWeakWords().some(w => w.hanzi === hanzi);
}

function toggleWeakWord(hanzi, level) {
  const list = loadWeakWords();
  const existingIndex = list.findIndex(w => w.hanzi === hanzi);
  if (existingIndex >= 0) {
    list.splice(existingIndex, 1);
  } else {
    list.push({ hanzi, level: level || currentLevel || '' });
  }
  saveWeakWords(list);
  renderWeakWordsList();
  updateWeakWordToggleButton();
  return existingIndex < 0; // true if now starred
}

function updateWeakWordToggleButton() {
  const btn = document.getElementById('weakWordToggleBtn');
  if (!btn || !activeStudyWord) return;
  const starred = isWeakWord(activeStudyWord.hanzi);
  btn.textContent = starred ? '★ Đã đánh dấu' : '☆ Đánh dấu từ khó';
  btn.classList.toggle('active', starred);
}

function renderWeakWordsList() {
  const container = document.getElementById('weakWordsList');
  if (!container) return;
  const list = loadWeakWords();
  if (!list.length) {
    container.innerHTML = '<div class="sidebar-search-empty">Chưa có từ nào được đánh dấu.</div>';
    return;
  }
  container.innerHTML = list.map(w => `
    <li class="sidebar-search-result weak-word-item" data-hanzi="${w.hanzi}">
      <span class="ssr-hanzi">${w.hanzi}</span>
      <span class="ssr-level">${w.level}</span>
      <button type="button" class="weak-word-remove" data-remove="${w.hanzi}" aria-label="Bỏ đánh dấu ${w.hanzi}">✕</button>
    </li>
  `).join('');
}

function initWeakWordsPanel() {
  const mount = document.getElementById('workstationLeft');
  if (!mount) return;
  const wrap = document.createElement('div');
  wrap.className = 'weak-words-panel';
  wrap.innerHTML = `
    <div class="sidebar-panel-title">Từ khó (đã đánh dấu)</div>
    <ul class="sidebar-search-results weak-words-list" id="weakWordsList"></ul>
  `;
  mount.appendChild(wrap);
  renderWeakWordsList();

  wrap.addEventListener('click', e => {
    const removeBtn = e.target.closest('[data-remove]');
    if (removeBtn) {
      const list = loadWeakWords().filter(w => w.hanzi !== removeBtn.dataset.remove);
      saveWeakWords(list);
      renderWeakWordsList();
      updateWeakWordToggleButton();
      return;
    }
    const item = e.target.closest('.weak-word-item');
    if (item) setActiveStudyWord({ hanzi: item.dataset.hanzi, pinyin: '', meaning: '' });
  });

  onActiveWordChange(updateWeakWordToggleButton);
}

document.addEventListener('DOMContentLoaded', initWeakWordsPanel);
```

- [ ] **Step 2: Add the ★ toggle button to the flashcard toolbar**

In `flashcards.html`, inside `.tool-group` (line 197-201), add a third button:
```html
<div class="tool-group">
  <button class="icon-btn" id="shuffleBtn" onclick="shuffleDeck()">🔀 Xáo trộn</button>
  <button class="icon-btn" id="pinyinToggle" onclick="togglePinyin()">👁 Đang hiện pinyin</button>
  <button class="icon-btn" id="weakWordToggleBtn" onclick="toggleWeakWord(activeStudyWord && activeStudyWord.hanzi, currentLevel)">☆ Đánh dấu từ khó</button>
  <button class="icon-btn" id="transferToggle" onclick="toggleTransferPanel()" aria-controls="transferPanel" aria-expanded="false">💾 Sao lưu</button>
</div>
```

- [ ] **Step 3: Add weak-words list styles**

Append to `assets/css/workstation.css`:
```css
.weak-word-item { position: relative; }
.weak-word-remove {
  border: none;
  background: transparent;
  color: var(--danger-text);
  cursor: pointer;
  font-size: 13px;
  padding: 2px 6px;
}
#weakWordToggleBtn.active { color: var(--accent); }
```

- [ ] **Step 4: Verify toggling and persistence**

`browser_navigate`, open HSK1 flashcards so `activeStudyWord` is set (per Task 2's sync), then `browser_evaluate`:
```js
() => {
  const before = isWeakWord(activeStudyWord.hanzi);
  toggleWeakWord(activeStudyWord.hanzi, currentLevel);
  const after = isWeakWord(activeStudyWord.hanzi);
  return { before, after };
}
```
Expected: `{ before: false, after: true }` (first toggle stars it).

`browser_evaluate` again with the same `toggleWeakWord` call.
Expected: word un-stars (`isWeakWord` returns `false`).

- [ ] **Step 5: Verify remove button in the sidebar list**

Star a word via the ★ button (`browser_click` on `#weakWordToggleBtn`), `browser_snapshot` to confirm it appears in `#weakWordsList`. Click its `✕` remove button, `browser_snapshot` again to confirm it's gone and the empty-state message shows if it was the only entry.

- [ ] **Step 6: Commit**

```bash
git add assets/js/weak-words.js flashcards.html assets/css/workstation.css
git commit -m "feat(workstation): add weak/starred words list and toggle"
```

---

## Task 6: Right sidebar — Hanzi stroke order canvas

**Files:**
- Create: `assets/js/stroke-canvas.js`
- Modify: `flashcards.html` (Hanzi Writer CDN script tag, new module script tags, all in the existing script block)

**Interfaces:**
- Consumes: `onActiveWordChange(fn)` from Task 2; global `HanziWriter` from the CDN script.
- Produces: `function initStrokeCanvas()`, renders into `#workstationRight`.

- [ ] **Step 1: Add the Hanzi Writer CDN script and this task's module script to flashcards.html**

At the end of the existing script block (`flashcards.html`, right before line 434's `<script src="assets/flashcards.js...">`), add, in this exact order (dependency order matters — Hanzi Writer must load before `stroke-canvas.js` executes; all `sidebar-*`/`weak-words.js`/`stroke-canvas.js`/`grammar-breakdown.js` must load after `state.js` for the sync primitives to exist):
```html
<script src="https://cdn.jsdelivr.net/npm/hanzi-writer@3/dist/hanzi-writer.min.js"></script>
<script src="assets/js/sidebar-search.js?v=20260928"></script>
<script src="assets/js/sidebar-radicals-filter.js?v=20260928"></script>
<script src="assets/js/weak-words.js?v=20260928"></script>
<script src="assets/js/stroke-canvas.js?v=20260928"></script>
<script src="assets/js/grammar-breakdown.js?v=20260928"></script>
```
(This single step covers wiring in all five new modules from Tasks 3-7; later tasks assume these tags already exist and only add their own `.js` file content.)

- [ ] **Step 2: Write the stroke canvas module**

Create `assets/js/stroke-canvas.js`:
```js
// Right sidebar: Hanzi Writer stroke-order canvas with animate + quiz mode.
let strokeCanvasWriter = null;

function destroyStrokeCanvasWriter() {
  const el = document.getElementById('strokeCanvasTarget');
  if (el) el.innerHTML = '';
  strokeCanvasWriter = null;
}

function loadStrokeCanvasWord(word) {
  const target = document.getElementById('strokeCanvasTarget');
  const fallback = document.getElementById('strokeCanvasFallback');
  if (!target || !fallback) return;
  destroyStrokeCanvasWriter();
  fallback.hidden = true;

  if (!word || !word.hanzi || typeof HanziWriter === 'undefined') {
    fallback.hidden = false;
    fallback.textContent = !word ? 'Chọn một từ để xem thứ tự nét.' : 'Không thể tải thư viện viết chữ.';
    return;
  }

  const thisChar = word.hanzi[0]; // canvas shows first character of multi-char words
  try {
    strokeCanvasWriter = HanziWriter.create('strokeCanvasTarget', thisChar, {
      width: 200,
      height: 200,
      padding: 10,
      showOutline: true,
      strokeColor: '#2b2926',
    });
  } catch (e) {
    fallback.hidden = false;
    fallback.textContent = 'Không thể tải nét chữ cho ký tự này (mất kết nối mạng hoặc ký tự chưa được hỗ trợ).';
  }
}

function animateStrokeCanvas() {
  if (strokeCanvasWriter) strokeCanvasWriter.animateCharacter();
}

function quizStrokeCanvas() {
  if (strokeCanvasWriter) strokeCanvasWriter.quiz();
}

function initStrokeCanvas() {
  const mount = document.getElementById('workstationRight');
  if (!mount) return;
  const wrap = document.createElement('div');
  wrap.className = 'stroke-canvas-panel';
  wrap.innerHTML = `
    <div class="sidebar-panel-title">Thứ tự nét</div>
    <div class="stroke-canvas-grid" id="strokeCanvasTarget"></div>
    <div class="stroke-canvas-fallback" id="strokeCanvasFallback" hidden></div>
    <div class="stroke-canvas-controls">
      <button type="button" class="icon-btn" id="strokeAnimateBtn">▶ Xem thứ tự nét</button>
      <button type="button" class="icon-btn" id="strokeQuizBtn">✍️ Luyện viết</button>
    </div>
  `;
  mount.appendChild(wrap);

  wrap.querySelector('#strokeAnimateBtn').addEventListener('click', animateStrokeCanvas);
  wrap.querySelector('#strokeQuizBtn').addEventListener('click', quizStrokeCanvas);

  onActiveWordChange(loadStrokeCanvasWord);
  loadStrokeCanvasWord(typeof activeStudyWord !== 'undefined' ? activeStudyWord : null);
}

document.addEventListener('DOMContentLoaded', initStrokeCanvas);
```

- [ ] **Step 3: Add stroke canvas styles (田-grid background)**

Create `assets/css/sidebar-lab.css`:
```css
.stroke-canvas-panel { display: flex; flex-direction: column; gap: 8px; }
.stroke-canvas-grid {
  width: 200px;
  height: 200px;
  background-color: var(--card-bg);
  background-image:
    linear-gradient(to right, var(--border) 1px, transparent 1px),
    linear-gradient(to bottom, var(--border) 1px, transparent 1px),
    linear-gradient(to right, transparent calc(50% - 1px), var(--border) calc(50% - 1px), var(--border) calc(50% + 1px), transparent calc(50% + 1px)),
    linear-gradient(to bottom, transparent calc(50% - 1px), var(--border) calc(50% - 1px), var(--border) calc(50% + 1px), transparent calc(50% + 1px));
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
}
.stroke-canvas-fallback {
  width: 200px;
  padding: 12px;
  color: var(--text-secondary);
  font-size: 13px;
  background: var(--card-bg);
  border: 1px dashed var(--border);
  border-radius: var(--radius-md);
}
.stroke-canvas-controls { display: flex; gap: 8px; }
```

Add its `<link>` in `flashcards.html` after `workstation.css`'s link (Task 1 Step 4):
```html
<link rel="stylesheet" href="assets/css/sidebar-lab.css?v=20260928">
```

- [ ] **Step 4: Verify CDN load and canvas creation**

`browser_navigate`, wait for load, `browser_evaluate`:
```js
() => typeof HanziWriter
```
Expected: `"function"` (confirms CDN script loaded).

Open HSK1 flashcards so `activeStudyWord` becomes non-null (Task 2's sync fires `loadStrokeCanvasWord` via the listener), then `browser_evaluate`:
```js
() => document.getElementById('strokeCanvasTarget').children.length
```
Expected: greater than 0 (Hanzi Writer injects an SVG).

- [ ] **Step 5: Verify fallback path**

`browser_evaluate`:
```js
() => {
  const originalHW = window.HanziWriter;
  window.HanziWriter = undefined;
  loadStrokeCanvasWord({ hanzi: '爱' });
  const fallbackShown = !document.getElementById('strokeCanvasFallback').hidden;
  window.HanziWriter = originalHW;
  return fallbackShown;
}
```
Expected: `true` — fallback message shows when `HanziWriter` is unavailable.

- [ ] **Step 6: Verify rapid word switching doesn't leak instances**

`browser_evaluate`:
```js
() => {
  setActiveStudyWord({ hanzi: '爱' });
  setActiveStudyWord({ hanzi: '好' });
  setActiveStudyWord({ hanzi: '人' });
  return document.getElementById('strokeCanvasTarget').children.length;
}
```
Expected: a small number (Hanzi Writer's own SVG root, not 3x accumulated content) — confirms `destroyStrokeCanvasWriter()`'s `innerHTML = ''` clears prior instances on each change.

- [ ] **Step 7: Commit**

```bash
git add flashcards.html assets/js/stroke-canvas.js assets/css/sidebar-lab.css
git commit -m "feat(workstation): add Hanzi stroke-order canvas to right sidebar"
```

---

## Task 7: Right sidebar — grammar breakdown starter dataset + rendering

**Files:**
- Create: `database/grammar/starter_sentences.json`
- Create: `assets/js/grammar-breakdown.js`

**Interfaces:**
- Consumes: `onActiveWordChange(fn)`, `activeStudyWord` from Task 2.
- Produces: `function initGrammarBreakdown()`, renders into `#workstationRight` below the stroke canvas panel.

- [ ] **Step 1: Author the starter grammar dataset**

Create `database/grammar/starter_sentences.json` with entries covering common HSK1-2 words and at least one entry demonstrating each of 把/被/连...都... per the spec:
```json
[
  {
    "hanzi": "爱",
    "zh": "我爱我的家人。",
    "roles": [
      { "text": "我", "type": "S" },
      { "text": "爱", "type": "V" },
      { "text": "我的家人", "type": "O" }
    ],
    "grammar_point": { "pattern": "S + V + O", "note": "Câu trần thuật cơ bản: chủ ngữ đứng trước động từ, tân ngữ đứng sau." }
  },
  {
    "hanzi": "喝",
    "zh": "他喜欢喝茶。",
    "roles": [
      { "text": "他", "type": "S" },
      { "text": "喜欢", "type": "V" },
      { "text": "喝茶", "type": "O" }
    ],
    "grammar_point": { "pattern": "S + V1 + V2O", "note": "Động từ 喜欢 có thể lấy một cụm động từ khác làm tân ngữ." }
  },
  {
    "hanzi": "把",
    "zh": "我把书放在桌子上。",
    "roles": [
      { "text": "我", "type": "S" },
      { "text": "把书", "type": "M" },
      { "text": "放", "type": "V" },
      { "text": "在桌子上", "type": "O" }
    ],
    "grammar_point": { "pattern": "S + 把 + O + V + 补语", "note": "Câu chữ 把 đưa tân ngữ ra trước động từ để nhấn mạnh kết quả xử lý tân ngữ đó." }
  },
  {
    "hanzi": "被",
    "zh": "杯子被他打破了。",
    "roles": [
      { "text": "杯子", "type": "S" },
      { "text": "被他", "type": "M" },
      { "text": "打破", "type": "V" },
      { "text": "了", "type": "M" }
    ],
    "grammar_point": { "pattern": "S(bị động) + 被 + tác nhân + V", "note": "Câu chữ 被 diễn tả chủ ngữ chịu tác động của hành động, tác nhân gây ra hành động đứng sau 被." }
  },
  {
    "hanzi": "连",
    "zh": "他连一个字都不认识。",
    "roles": [
      { "text": "他", "type": "S" },
      { "text": "连一个字", "type": "M" },
      { "text": "都不认识", "type": "V" }
    ],
    "grammar_point": { "pattern": "连 + N + 都/也 + (不/没) + V", "note": "Cấu trúc 连...都... nhấn mạnh mức độ, thường đi kèm phủ định để nhấn mạnh sự thiếu sót." }
  }
]
```
(This is the initial starter set; more entries can be appended later without code changes, per the spec's starter-set scope.)

- [ ] **Step 2: Write the grammar breakdown module**

Create `assets/js/grammar-breakdown.js`:
```js
// Right sidebar: color-coded S/V/O/M sentence breakdown + grammar note.
let grammarStarterData = null;
let grammarStarterDataPromise = null;

function loadGrammarStarterData() {
  if (grammarStarterDataPromise) return grammarStarterDataPromise;
  grammarStarterDataPromise = fetch('database/grammar/starter_sentences.json')
    .then(r => r.json())
    .then(data => { grammarStarterData = data; return data; })
    .catch(() => { grammarStarterData = []; return []; });
  return grammarStarterDataPromise;
}

const GRAMMAR_ROLE_LABELS = { S: 'Chủ ngữ', V: 'Vị ngữ', O: 'Tân ngữ', M: 'Bổ nghĩa' };

function renderGrammarEntry(entry, container) {
  if (!entry) {
    container.innerHTML = '<div class="sidebar-search-empty">Chưa có phân tích ngữ pháp cho từ này.</div>';
    return;
  }
  const rolesHtml = entry.roles.map(r =>
    `<span class="grammar-role grammar-role-${r.type}" title="${GRAMMAR_ROLE_LABELS[r.type] || r.type}">${r.text}</span>`
  ).join('');
  container.innerHTML = `
    <div class="grammar-sentence">${rolesHtml}</div>
    <div class="grammar-note-card">
      <div class="grammar-note-pattern">${entry.grammar_point.pattern}</div>
      <div class="grammar-note-text">${entry.grammar_point.note}</div>
    </div>
  `;
}

function updateGrammarBreakdown(word) {
  const container = document.getElementById('grammarBreakdownBody');
  if (!container) return;
  if (!word || !grammarStarterData) {
    renderGrammarEntry(null, container);
    return;
  }
  const entry = grammarStarterData.find(e => e.hanzi === word.hanzi);
  renderGrammarEntry(entry, container);
}

function initGrammarBreakdown() {
  const mount = document.getElementById('workstationRight');
  if (!mount) return;
  const wrap = document.createElement('div');
  wrap.className = 'grammar-breakdown-panel';
  wrap.innerHTML = `
    <div class="sidebar-panel-title">Phân tích ngữ pháp</div>
    <div id="grammarBreakdownBody"></div>
  `;
  mount.appendChild(wrap);

  loadGrammarStarterData().then(() => {
    updateGrammarBreakdown(typeof activeStudyWord !== 'undefined' ? activeStudyWord : null);
  });
  onActiveWordChange(updateGrammarBreakdown);
}

document.addEventListener('DOMContentLoaded', initGrammarBreakdown);
```

- [ ] **Step 3: Add grammar breakdown styles**

Append to `assets/css/sidebar-lab.css`:
```css
.grammar-breakdown-panel { display: flex; flex-direction: column; gap: 8px; }
.grammar-sentence {
  font-size: 18px;
  line-height: 1.8;
  padding: 12px;
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
}
.grammar-role { padding: 0 2px; border-radius: 4px; }
.grammar-role-S { color: var(--info-text); background: var(--info-bg); }
.grammar-role-V { color: var(--success-text); background: var(--success-bg); }
.grammar-role-O { color: var(--accent); background: var(--accent-light); }
.grammar-role-M { color: var(--text-secondary); background: var(--border); }
.grammar-note-card {
  padding: 10px 12px;
  background: var(--example-bg);
  border: 1px solid var(--example-border);
  border-radius: var(--radius-md);
}
.grammar-note-pattern { font-weight: 600; color: var(--text-primary); margin-bottom: 4px; }
.grammar-note-text { color: var(--text-secondary); font-size: 13px; }
```

- [ ] **Step 4: Verify JSON parses and dataset loads**

Run: `python3 -c "import json; d = json.load(open('database/grammar/starter_sentences.json')); print(len(d), all('hanzi' in e and 'roles' in e and 'grammar_point' in e for e in d))"`
Expected: `5 True` (or however many entries were authored, all with required fields).

- [ ] **Step 5: Verify rendering for a covered word**

`browser_navigate`, `browser_evaluate`:
```js
async () => {
  await loadGrammarStarterData();
  setActiveStudyWord({ hanzi: '爱' });
  return document.getElementById('grammarBreakdownBody').innerHTML.includes('grammar-role-S');
}
```
Expected: `true`.

- [ ] **Step 6: Verify placeholder for an uncovered word**

`browser_evaluate`:
```js
() => {
  setActiveStudyWord({ hanzi: '这是一个不存在的词' });
  return document.getElementById('grammarBreakdownBody').textContent.includes('Chưa có phân tích ngữ pháp');
}
```
Expected: `true` — confirms the Review Focus item about non-starter-set words is covered.

- [ ] **Step 7: Commit**

```bash
git add database/grammar/starter_sentences.json assets/js/grammar-breakdown.js assets/css/sidebar-lab.css
git commit -m "feat(workstation): add grammar breakdown panel with starter dataset"
```

---

## Task 8: Mobile layout — top search bar/drawer + accordions

**Files:**
- Modify: `assets/css/workstation.css` (mobile-specific rules)
- Modify: `assets/js/sidebar-search.js`, `assets/js/sidebar-radicals-filter.js`, `assets/js/weak-words.js` (wrap left content in a `<dialog>` on mobile)
- Modify: `assets/js/stroke-canvas.js`, `assets/js/grammar-breakdown.js` (wrap right content in `<details>` on mobile)

**Interfaces:**
- Consumes: `document.body.classList.contains('is-desktop-dock')` (Task 1) to decide dialog-vs-inline and accordion-vs-inline rendering, decided once per module at init time and re-checked on the `matchMedia` change event.

- [ ] **Step 1: Add a shared mobile dialog wrapper for the left sidebar**

In `flashcards.html`, add a trigger button and empty `<dialog>` right after the `#workstationLeft` element (from Task 1):
```html
<aside class="workstation-left" id="workstationLeft" aria-label="Tra cứu nhanh"></aside>
<button type="button" id="mobileDockTrigger" class="mobile-dock-trigger">🔍 Tra cứu nhanh</button>
<dialog id="mobileDockDialog" class="mobile-dock-dialog">
  <button type="button" id="mobileDockClose" class="mobile-dock-close" aria-label="Đóng">✕</button>
  <div id="mobileDockDialogBody"></div>
</dialog>
```

- [ ] **Step 2: Update each left-sidebar module to mount into the dialog body on mobile**

In `assets/js/sidebar-search.js`, `assets/js/sidebar-radicals-filter.js`, and `assets/js/weak-words.js`, change the mount-resolution line in each `init*` function from:
```js
const mount = document.getElementById('workstationLeft');
```
to:
```js
const mount = document.body.classList.contains('is-desktop-dock')
  ? document.getElementById('workstationLeft')
  : document.getElementById('mobileDockDialogBody');
```
(Apply this exact change in `initSidebarSearch()`, `initSidebarRadicalsFilter()`, and `initWeakWordsPanel()`.)

- [ ] **Step 3: Wire the dialog open/close triggers**

Add to `assets/js/sidebar-search.js` (co-located since it's the first-loaded of the three left-sidebar modules, keeping the dialog wiring in one place):
```js
function initMobileDockDialog() {
  const trigger = document.getElementById('mobileDockTrigger');
  const dialog = document.getElementById('mobileDockDialog');
  const closeBtn = document.getElementById('mobileDockClose');
  if (!trigger || !dialog || !closeBtn) return;
  trigger.addEventListener('click', () => dialog.showModal());
  closeBtn.addEventListener('click', () => dialog.close());
}
document.addEventListener('DOMContentLoaded', initMobileDockDialog);
```

- [ ] **Step 4: Update each right-sidebar module to mount into a `<details>` accordion on mobile**

In `assets/js/stroke-canvas.js`'s `initStrokeCanvas()`, change:
```js
const mount = document.getElementById('workstationRight');
if (!mount) return;
const wrap = document.createElement('div');
wrap.className = 'stroke-canvas-panel';
```
to:
```js
const isDesktop = document.body.classList.contains('is-desktop-dock');
const mount = isDesktop
  ? document.getElementById('workstationRight')
  : document.getElementById('screenCards');
if (!mount) return;
const wrap = document.createElement(isDesktop ? 'div' : 'details');
wrap.className = 'stroke-canvas-panel';
if (!isDesktop) {
  const summary = document.createElement('summary');
  summary.textContent = 'Thứ tự nét';
  wrap.appendChild(summary);
}
```
And change the subsequent `wrap.innerHTML = ...` assignment to append rather than replace when a `<summary>` was just added — use a separate content div:
```js
const body = document.createElement('div');
body.innerHTML = `
  <div class="stroke-canvas-grid" id="strokeCanvasTarget"></div>
  <div class="stroke-canvas-fallback" id="strokeCanvasFallback" hidden></div>
  <div class="stroke-canvas-controls">
    <button type="button" class="icon-btn" id="strokeAnimateBtn">▶ Xem thứ tự nét</button>
    <button type="button" class="icon-btn" id="strokeQuizBtn">✍️ Luyện viết</button>
  </div>
`;
wrap.appendChild(body);
mount.appendChild(wrap);
```
(Remove the old title `<div class="sidebar-panel-title">Thứ tự nét</div>` from the innerHTML template since desktop still needs a heading — add it back conditionally: `if (isDesktop) { const title = document.createElement('div'); title.className = 'sidebar-panel-title'; title.textContent = 'Thứ tự nét'; wrap.appendChild(title); }` placed before `wrap.appendChild(body)`.)

Apply the equivalent pattern to `assets/js/grammar-breakdown.js`'s `initGrammarBreakdown()`: mount into `#screenCards` as a `<details>` with summary "Phân tích ngữ pháp" when `!isDesktop`, else into `#workstationRight` as today.

- [ ] **Step 5: Add mobile-specific CSS**

Append to `assets/css/workstation.css`:
```css
.mobile-dock-trigger { display: none; }
.mobile-dock-dialog { display: none; }

@media (max-width: 1024px) {
  .mobile-dock-trigger {
    display: block;
    width: calc(100% - 32px);
    margin: 16px;
    padding: 10px;
    border-radius: var(--radius-md);
    border: 1px solid var(--border);
    background: var(--card-bg);
    color: var(--text-primary);
    font-size: 14px;
  }
  .mobile-dock-dialog[open] {
    display: block;
    width: min(90vw, 480px);
    max-height: 80vh;
    overflow-y: auto;
    border-radius: var(--radius-lg);
    border: 1px solid var(--border);
    background: var(--card-bg);
    color: var(--text-primary);
    padding: 16px;
  }
  .mobile-dock-dialog::backdrop { background: rgba(0,0,0,0.4); }
  .mobile-dock-close {
    position: sticky;
    top: 0;
    float: right;
    border: none;
    background: transparent;
    font-size: 16px;
    cursor: pointer;
    color: var(--text-secondary);
  }
  .workstation-left, .workstation-right { display: none; }
}
```

- [ ] **Step 6: Verify desktop path unaffected**

`browser_resize` to `1440x900`, `browser_navigate`, `browser_snapshot`.
Expected: `#mobileDockTrigger` not visible (CSS `display:none` outside the media query at this width since it's above 1024px), search/radicals/weak-words render inline in `.workstation-left` as before, stroke canvas + grammar panel render inline in `.workstation-right`.

- [ ] **Step 7: Verify mobile path**

`browser_resize` to `375x800`, `browser_navigate` (fresh load so init functions read the correct `is-mobile-drawer` class), `browser_snapshot`.
Expected: `.workstation-left`/`.workstation-right` hidden; `#mobileDockTrigger` visible; `<details>` elements for stroke canvas and grammar breakdown appear after the card area inside `#screenCards`.

`browser_click` `#mobileDockTrigger`, `browser_snapshot`.
Expected: `#mobileDockDialog` opens showing search input, radicals chips, and weak-words list stacked inside it.

- [ ] **Step 8: Verify resize mid-session (Review Focus item)**

Starting at `1440x900` with a word active (open HSK1 flashcards), `browser_resize` to `375x800`, then `browser_evaluate` `() => activeStudyWord && activeStudyWord.hanzi`.
Expected: unchanged — the active word survives the breakpoint crossing since it's a `state.js` global, not tied to which container currently renders it.

- [ ] **Step 9: Commit**

```bash
git add flashcards.html assets/css/workstation.css assets/js/sidebar-search.js assets/js/sidebar-radicals-filter.js assets/js/weak-words.js assets/js/stroke-canvas.js assets/js/grammar-breakdown.js
git commit -m "feat(workstation): add mobile drawer/accordion layout for sidebars"
```

---

## Task 9: Full-branch verification pass

**Files:** none (verification only)

- [ ] **Step 1: TypeScript/JS syntax sanity — no TS in this repo, so run a Node syntax check instead**

Run: `for f in assets/js/sidebar-search.js assets/js/sidebar-radicals-filter.js assets/js/weak-words.js assets/js/stroke-canvas.js assets/js/grammar-breakdown.js assets/js/state.js assets/js/flashcard.js; do node --check "$f" || echo "FAIL: $f"; done`
Expected: no `FAIL` lines.

- [ ] **Step 2: Validate all touched/created JSON**

Run: `python3 -c "import json; json.load(open('database/grammar/starter_sentences.json')); print('ok')"`
Expected: `ok`.

- [ ] **Step 3: Check for stray whitespace/conflict markers**

Run: `git diff --check`
Expected: no output.

- [ ] **Step 4: Full desktop walkthrough in browser**

`browser_navigate`, `browser_resize` to `1440x900`. In sequence: type a search query and click a result; click a radical stroke chip and click an example; star a word from the flashcard toolbar and click it from the weak-words list; confirm the stroke canvas and grammar panel update each time (`browser_evaluate` checking `strokeCanvasTarget` content changes and `grammarBreakdownBody` text changes). Check `browser_console_messages` for errors after the full walkthrough.
Expected: no console errors; all four sync sources correctly drive the stroke canvas and grammar panel.

- [ ] **Step 5: Full mobile walkthrough in browser**

`browser_resize` to `375x800`, `browser_navigate` (fresh load). Open the mobile dock dialog, run a search, click a result, close the dialog, confirm the flashcard area reflects the change, open the stroke-order `<details>` and grammar `<details>`, confirm both show the correct word.
Expected: no console errors; no layout overflow (check via `browser_snapshot`).

- [ ] **Step 6: Verify dark/light theme still applies to new panels**

`browser_evaluate`:
```js
() => { toggleTheme(); return document.documentElement.dataset.theme; }
```
Then `browser_snapshot` and visually confirm the search input, radical chips, weak-words list, stroke canvas grid, and grammar role colors all switch to dark-theme-appropriate colors (no hardcoded light-only colors, since all new CSS used `var(--*)` tokens per the Global Constraints).

- [ ] **Step 7: Final commit if any fixes were needed during verification**

```bash
git add -A
git commit -m "fix(workstation): address issues found during full-branch verification"
```
(Skip this step if Steps 1-6 found nothing to fix.)

---

## Self-Review Notes

**Spec coverage:** Layout shell (Task 1), left sidebar search/radicals/weak-words (Tasks 3-5), right sidebar stroke canvas/grammar (Tasks 6-7), sync mechanism (Task 2), mobile behavior (Task 8) — every spec section maps to a task. Theming reuse verified explicitly in Task 9 Step 6.

**Type/interface consistency:** `setActiveStudyWord`/`onActiveWordChange`/`activeStudyWord` names match across state.js, flashcard.js, and all five consuming modules. `radicalStrokeUrl`/`RADICAL_STROKE_COUNTS` names match their actual definitions in `radicals-state.js` (verified by reading the file, not assumed).

**Review Focus coverage confirmed:**
- Empty/no-match search → Task 3 Step 4.
- Rapid word switching / leaked instances → Task 6 Step 6.
- Word with no starter-set grammar data → Task 7 Step 6.
- Mobile↔desktop resize mid-session → Task 8 Step 8.
- Offline/CDN-blocked Hanzi Writer → Task 6 Step 5.
