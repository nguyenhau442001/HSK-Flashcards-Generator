# Fast-Review Cross-Level Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move Fast-Review (⚡ Ôn nhanh) out of the per-level flashcard screen into its own primary tab with a range slider (HSK1..HSKN cumulative), loading multiple levels' word data off the main thread via a Web Worker and grading against each word's own level's progress store.

**Architecture:** New primary tab (`setPrimaryTab('review')`) shows a new top-level screen `#screenReviewPicker` with a range slider. "Bắt đầu" spins up `assets/js/fast-review-worker.js`, which fetches every level's `dataUrl` in the selected range in parallel and tags each word with `_level`. The main thread stores the merged array in `reviewWordPool` and a per-level progress map in `reviewProgressByLevel` (read once via the existing `readSavedLevelProgress(level)`). Session/timer/grading logic in `assets/js/fast-review.js` is repointed from the single-level `WORDS`/`progress` globals to these new cross-level structures; grading writes back to the correct level's own `hsk_<level>_progress_v2` key via a new `saveLevelProgress(level, progressObj)` helper. The old in-flashcard-screen review tab (`reviewTab` button, `#reviewView` panel, `setViewMode('review')` branch) is removed.

**Tech Stack:** Vanilla JS (ES2017, no build step, no bundler, no framework), a dedicated Web Worker (no bundler needed — plain `new Worker('assets/js/fast-review-worker.js')`, same-origin script), plain CSS with custom properties, static HTML. No test framework exists in this repo (no `package.json`, no JS test files) — pure-logic pieces are verified via `node --check` (syntax) and isolated `node -e` snippets (behavior), same convention as the original fast-review plan; DOM/worker-dependent pieces are verified by manual source trace plus browser console when a browser is available.

## Global Constraints

- Word `id` collides across level JSON files (each restarts at `id: 1`) — every cross-level word reference must carry `_level` and all lookups (`reviewProgressByLevel[_level][id]`) must use the pair, never `id` alone.
- Flashcard mode's `WORDS` / `progress` / `currentLevel` globals must not be reassigned or mutated by Fast-Review — Fast-Review gets its own globals (`reviewWordPool`, `reviewProgressByLevel`).
- `recordDailyStudy(wordId)` currently keys its activity entry off the global `currentLevel` (`levels.js:370-382`) and no-ops entirely when `currentLevel` is `null` — since Fast-Review no longer requires a level to be "open," this function must accept an explicit level parameter, defaulting to `currentLevel` so the two existing call sites in `progress.js` are unaffected.
- Session mechanics (3 lives, 20s timer, ~50/50 question type, pinyin loose-match, homophone-safe distractors, `checkCelebration`/`recordDailyStudy` per answer) are unchanged — only the data source changes from `WORDS[idx]` to `reviewWordPool[idx]`.
- No new localStorage keys beyond what already exists per level (`hsk_<level>_progress_v2`) — Fast-Review reads/writes several of those in one session, never a new combined key.
- All user-facing copy in Vietnamese, matching existing app tone.
- Follow existing code style: 2-space indent, inline `onclick="fn()"` handlers, no semicolonless lines, matching `levels.js`/`fast-review.js`/`radicals.js` conventions.
- CSS: reuse existing theme custom properties (`--accent`, `--border`, `--card-bg`, `--text-secondary`, `--radius-md`, `--radius-lg`, etc.) — no new color tokens.

---

### Task 1: `recordDailyStudy` accepts an explicit level

**Files:**
- Modify: `assets/js/levels.js:370-382`

**Interfaces:**
- Produces: `recordDailyStudy(wordId, level = currentLevel)` — same external behavior for existing callers (level defaults to the global), but now callable with an explicit level for cross-level contexts.

This is a small, isolated, backward-compatible signature change — safe to land and verify before anything else depends on it.

- [ ] **Step 1: Change the function signature and body**

In `assets/js/levels.js`, replace:

```javascript
function recordDailyStudy(wordId) {
  if (!currentLevel || wordId === undefined || wordId === null) return;

  const activity = readStudyActivity();
  const today = localDateKey(new Date());
  const dayEntry = activity.days[today] || { words: [], seconds: 0 };
  const learnedWords = new Set(dayEntry.words);
  learnedWords.add(currentLevel + ':' + String(wordId));
  activity.days[today] = { words: Array.from(learnedWords), seconds: dayEntry.seconds };

  try { localStorage.setItem(STUDY_ACTIVITY_KEY, JSON.stringify(activity)); } catch (e) {}
  renderLearningDashboard();
}
```

with:

```javascript
function recordDailyStudy(wordId, level = currentLevel) {
  if (!level || wordId === undefined || wordId === null) return;

  const activity = readStudyActivity();
  const today = localDateKey(new Date());
  const dayEntry = activity.days[today] || { words: [], seconds: 0 };
  const learnedWords = new Set(dayEntry.words);
  learnedWords.add(level + ':' + String(wordId));
  activity.days[today] = { words: Array.from(learnedWords), seconds: dayEntry.seconds };

  try { localStorage.setItem(STUDY_ACTIVITY_KEY, JSON.stringify(activity)); } catch (e) {}
  renderLearningDashboard();
}
```

- [ ] **Step 2: Syntax check**

Run: `node --check assets/js/levels.js`
Expected: no output (success).

- [ ] **Step 3: Verify existing call sites are unaffected**

Run: `grep -n "recordDailyStudy(" assets/js/progress.js`
Expected: both call sites still read `recordDailyStudy(WORDS[wIdx].id);` — single-argument form, which now relies on the new default parameter and behaves identically to before (since `currentLevel` is set in those flashcard-mode code paths).

- [ ] **Step 4: Commit**

```bash
git add assets/js/levels.js
git commit -m "refactor: recordDailyStudy accepts explicit level, defaults to currentLevel"
```

---

### Task 2: `saveLevelProgress` helper for writing any level's progress store

**Files:**
- Modify: `assets/js/storage.js` (append after `saveProgress`, line 19)

**Interfaces:**
- Consumes: nothing new — mirrors the existing `storageKey('progress')` pattern but parameterized.
- Produces: `saveLevelProgress(level, progressObj)` — writes `progressObj` to `hsk_<level>_progress_v2`, independent of the global `currentLevel`.

- [ ] **Step 1: Add the helper**

In `assets/js/storage.js`, after the existing `saveProgress` function (line 19), add:

```javascript
function saveLevelProgress(level, progressObj) {
  try { localStorage.setItem('hsk_' + level + '_progress_v2', JSON.stringify(progressObj)); } catch (e) {}
}
```

- [ ] **Step 2: Syntax check**

Run: `node --check assets/js/storage.js`
Expected: no output (success).

- [ ] **Step 3: Verify key format matches the existing reader**

Run: `grep -n "hsk_.*_progress_v2" assets/js/levels.js assets/js/storage.js`
Expected: both `readSavedLevelProgress` (in `levels.js`) and the new `saveLevelProgress` (in `storage.js`) construct the identical key string `'hsk_' + level + '_progress_v2'`.

- [ ] **Step 4: Commit**

```bash
git add assets/js/storage.js
git commit -m "feat: add saveLevelProgress helper for writing any level's progress store"
```

---

### Task 3: Remove the old in-flashcard-screen review tab

**Files:**
- Modify: `flashcards.html:140-141` (remove `reviewTab` button)
- Modify: `flashcards.html:211-215` (remove `#reviewView` panel)
- Modify: `assets/js/vocabulary-overview.js:1-47` (`setViewMode` — remove the `'review'` branch and the `abandonReviewSession()` call tied to it)
- Modify: `assets/css/flashcard.css:4-8` (`.view-tabs` — revert to 2-column grid now that only 2 tabs live there)

**Interfaces:**
- Consumes: none new.
- Produces: `setViewMode(mode)` now only accepts `'cards'` / `'overview'` (its original two-mode contract, matching the very first fast-review implementation before the in-screen review tab was added).

This task intentionally regresses the in-screen tab before Task 4+ adds the new primary-tab-based entry point — keeps each task's diff reviewable in isolation, and the app is left in a valid (if temporarily Fast-Review-less) state between commits.

- [ ] **Step 1: Remove the `reviewTab` button from `flashcards.html`**

Delete these lines (140-141):

```html
      <button id="reviewTab" class="view-tab" role="tab" aria-selected="false"
        aria-controls="reviewView" onclick="setViewMode('review')">⚡ Ôn nhanh</button>
```

- [ ] **Step 2: Remove the `#reviewView` panel from `flashcards.html`**

Delete these lines (211-215, immediately before the closing `</div>` of `#screenCards`):

```html
    <div id="reviewView" role="tabpanel" aria-labelledby="reviewTab" hidden>
      <div id="reviewStart"></div>
      <div id="reviewSession" hidden></div>
      <div id="reviewResult" hidden></div>
    </div>
```

- [ ] **Step 3: Remove the `'review'` branch from `setViewMode`**

In `assets/js/vocabulary-overview.js`, current function:

```javascript
function setViewMode(mode) {
  if (!currentLevel || !['cards', 'overview', 'review'].includes(mode)) return;

  stopSpeech();
  if (mode !== 'review') abandonReviewSession();
  currentView = mode;
  const showOverview = mode === 'overview';
  const showReview = mode === 'review';
  const studyView = document.getElementById('studyView');
  const overviewView = document.getElementById('overviewView');
  const reviewView = document.getElementById('reviewView');
  const flashcardTab = document.getElementById('flashcardTab');
  const overviewTab = document.getElementById('overviewTab');
  const reviewTab = document.getElementById('reviewTab');

  studyView.hidden = showOverview || showReview;
  overviewView.hidden = !showOverview;
  reviewView.hidden = !showReview;
  flashcardTab.classList.toggle('active', mode === 'cards');
  overviewTab.classList.toggle('active', showOverview);
  reviewTab.classList.toggle('active', showReview);
  flashcardTab.setAttribute('aria-selected', String(mode === 'cards'));
  overviewTab.setAttribute('aria-selected', String(showOverview));
  reviewTab.setAttribute('aria-selected', String(showReview));
  document.getElementById('appTitle').textContent = showOverview
    ? LEVELS[currentLevel].label + ' · Tổng quan'
    : showReview
      ? LEVELS[currentLevel].label + ' · Ôn nhanh'
      : LEVELS[currentLevel].label + ' Flashcards';

  if (showOverview) {
    const searchInput = document.getElementById('overviewSearch');
    const statusSelect = document.getElementById('overviewStatus');
    searchInput.value = overviewQuery;
    statusSelect.value = overviewStatus;
    renderOverview();
  }

  if (showReview) {
    renderReviewStart();
  }

  if (mode === 'cards') {
    setFilter(currentFilter);
  }
}
```

Replace with:

```javascript
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
```

- [ ] **Step 4: Revert `.view-tabs` to a 2-column grid**

In `assets/css/flashcard.css`, change:

```css
.view-tabs {
  display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 4px;
```

to:

```css
.view-tabs {
  display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 4px;
```

- [ ] **Step 5: Syntax check**

Run: `node --check assets/js/vocabulary-overview.js`
Expected: no output (success).

- [ ] **Step 6: Verify no dangling references**

Run: `grep -rn "reviewTab\|reviewView\|setViewMode('review')" flashcards.html assets/js/*.js`
Expected: no matches (all references removed).

- [ ] **Step 7: Commit**

```bash
git add flashcards.html assets/js/vocabulary-overview.js assets/css/flashcard.css
git commit -m "refactor: remove in-flashcard-screen review tab ahead of primary-tab redesign"
```

---

### Task 4: `#screenReviewPicker` HTML scaffold + primary tab button

**Files:**
- Modify: `flashcards.html:72-77` (primary tabs row — add third tab button)
- Modify: `flashcards.html` (add `#screenReviewPicker` as a new screen, sibling of `#screenPicker`/`#screenRadicalHub`, placed after `#screenRadicalCards`'s closing block — check current end-of-screens location with `grep -n "SCREEN" flashcards.html` first since line numbers shift after Task 3's edits)
- Modify: `assets/css/radicals.css:2-4` (`.primary-tabs` — 2 columns → 3)

**Interfaces:**
- Produces: DOM elements `#primaryTabReview`, `#screenReviewPicker`, `#reviewRangeSlider`, `#reviewRangeLabel`, `#reviewRangeCount`, `#reviewRangeStart` (button) — consumed by Task 6's `setPrimaryTab` wiring and Task 7's slider logic.

No JS behavior wired yet — this task is pure markup/CSS, verified by grep and visual structure check (no live interactivity to test until Task 6-7).

- [ ] **Step 1: Add the third primary tab button**

In `flashcards.html`, in the `.primary-tabs` block, change:

```html
  <div class="primary-tabs" id="primaryTabs" role="tablist" aria-label="Chế độ học">
    <button id="primaryTabVocab" class="primary-tab active" role="tab" aria-selected="true"
      aria-controls="screenPicker" onclick="setPrimaryTab('vocab')">📚 Từ vựng</button>
    <button id="primaryTabRadicals" class="primary-tab" role="tab" aria-selected="false"
      aria-controls="screenRadicalHub" onclick="setPrimaryTab('radicals')">部 Bộ thủ</button>
  </div>
```

to:

```html
  <div class="primary-tabs" id="primaryTabs" role="tablist" aria-label="Chế độ học">
    <button id="primaryTabVocab" class="primary-tab active" role="tab" aria-selected="true"
      aria-controls="screenPicker" onclick="setPrimaryTab('vocab')">📚 Từ vựng</button>
    <button id="primaryTabRadicals" class="primary-tab" role="tab" aria-selected="false"
      aria-controls="screenRadicalHub" onclick="setPrimaryTab('radicals')">部 Bộ thủ</button>
    <button id="primaryTabReview" class="primary-tab" role="tab" aria-selected="false"
      aria-controls="screenReviewPicker" onclick="setPrimaryTab('review')">⚡ Ôn nhanh</button>
  </div>
```

- [ ] **Step 2: Locate the end of the screens block**

Run: `grep -n "SCREEN\|^</div>$" flashcards.html | head -20`

Find the closing `</div>` of `#screenRadicalCards` (the last screen block, "SCREEN 4: Radical flashcards").

- [ ] **Step 3: Add `#screenReviewPicker` after the last screen block**

Insert immediately after `#screenRadicalCards`'s closing `</div>` (before whatever follows — likely a script section or the closing `</div>` of `.app`):

```html
  <!-- SCREEN 5: Fast-review range picker -->
  <div id="screenReviewPicker" style="display:none">
    <div class="review-range-picker">
      <div class="review-range-title">⚡ Chọn phạm vi ôn nhanh</div>
      <div class="review-range-sub">Kéo để chọn ôn từ HSK1 đến cấp độ nào</div>
      <div class="review-range-slider-wrap">
        <input type="range" id="reviewRangeSlider" min="1" max="6" value="1" step="1"
          aria-label="Chọn cấp độ cao nhất để ôn" oninput="updateReviewRangeLabel(this.value)">
        <div class="review-range-label" id="reviewRangeLabel">HSK1</div>
      </div>
      <div class="review-range-count" id="reviewRangeCount">150 từ</div>
      <button class="review-range-start-btn" id="reviewRangeStart" onclick="startReviewRangeLoad()">Bắt đầu</button>
    </div>
    <div id="reviewPickerBody"></div>
  </div>
```

Note: `#reviewPickerBody` is where Task 5's loading skeleton and Task 8's start-screen/session/result screens will render — kept separate from the always-visible slider controls above it, so the slider stays visible while loading feedback appears below it.

- [ ] **Step 4: Widen `.primary-tabs` to 3 columns**

In `assets/css/radicals.css`, change:

```css
.primary-tabs {
  display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px;
  margin: 16px 0 20px;
}
```

to:

```css
.primary-tabs {
  display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px;
  margin: 16px 0 20px;
}
```

- [ ] **Step 5: Verify structure**

Run: `grep -n "primaryTabReview\|screenReviewPicker\|reviewRangeSlider\|reviewRangeStart" flashcards.html`
Expected: 5 matches — the tab button, the screen div, the slider input, its label, and the start button, all present.

- [ ] **Step 6: Commit**

```bash
git add flashcards.html assets/css/radicals.css
git commit -m "feat: scaffold fast-review range-picker screen and third primary tab"
```

---

### Task 5: Range-picker CSS

**Files:**
- Create: `assets/css/fast-review-picker.css`
- Modify: `flashcards.html` (add `<link>` for the new stylesheet, alongside the existing `fast-review.css` link)

**Interfaces:**
- Consumes: DOM structure from Task 4 (`.review-range-picker`, `.review-range-slider-wrap`, etc.)
- Produces: visual styling only, no new JS-facing interfaces.

- [ ] **Step 1: Check where `fast-review.css` is currently linked**

Run: `grep -n "fast-review" flashcards.html`

- [ ] **Step 2: Create the new stylesheet**

Write `assets/css/fast-review-picker.css`:

```css
/* Fast-review range-picker screen: slider, count, start button. */
.review-range-picker {
  max-width: 420px; margin: 32px auto 0; padding: 24px 20px;
  border: 1px solid var(--border); border-radius: var(--radius-lg);
  background: var(--card-bg); text-align: center;
}
.review-range-title { font-size: 19px; font-weight: 700; margin-bottom: 6px; }
.review-range-sub { font-size: 13px; color: var(--text-secondary); margin-bottom: 20px; }

.review-range-slider-wrap { margin-bottom: 8px; }
#reviewRangeSlider {
  width: 100%; accent-color: var(--accent); cursor: pointer;
}
.review-range-label {
  font-size: 22px; font-weight: 700; color: var(--accent); margin-top: 10px;
}
.review-range-count { font-size: 13px; color: var(--text-secondary); margin-bottom: 20px; }

.review-range-start-btn {
  width: 100%; padding: 12px; border: 0; border-radius: var(--radius-md);
  background: var(--accent); color: #fff; font: inherit; font-size: 15px;
  font-weight: 700; cursor: pointer;
}
.review-range-start-btn:hover { opacity: 0.9; }
.review-range-start-btn:disabled { opacity: 0.5; cursor: wait; }
```

- [ ] **Step 3: Link the stylesheet in `flashcards.html`**

Find the existing `fast-review.css` `<link>` tag and add the new one immediately after it:

```html
<link rel="stylesheet" href="assets/css/fast-review-picker.css">
```

- [ ] **Step 4: Verify the link was added correctly**

Run: `grep -n "fast-review" flashcards.html`
Expected: two `<link>` lines, `fast-review.css` and `fast-review-picker.css`.

- [ ] **Step 5: Commit**

```bash
git add assets/css/fast-review-picker.css flashcards.html
git commit -m "feat: add fast-review range-picker CSS"
```

---

### Task 6: `setPrimaryTab` gains the `'review'` branch; slider label/count logic

**Files:**
- Modify: `assets/js/radicals.js:27-36` (`setPrimaryTab`)
- Modify: `assets/js/fast-review.js` (add `updateReviewRangeLabel`, called by the slider's `oninput`)

**Interfaces:**
- Consumes: `LEVELS` (from `state.js`, has `.label` and `.total` per level key `hsk1`..`hsk6`).
- Produces: `updateReviewRangeLabel(sliderValue)` — string/number → updates `#reviewRangeLabel` and `#reviewRangeCount` text content. Called both by the slider's `oninput` and once on tab-entry to initialize the display.
- Produces: `setPrimaryTab` now handles `'review'`, showing `#screenReviewPicker` and calling `updateReviewRangeLabel(document.getElementById('reviewRangeSlider').value)` to sync the display on entry.

- [ ] **Step 1: Add `updateReviewRangeLabel` to `fast-review.js`**

Add near the top of `assets/js/fast-review.js`, after the existing `pinyinLooseMatch` function (before `buildReviewPool`):

```javascript
const REVIEW_RANGE_LEVELS = ['hsk1', 'hsk2', 'hsk3', 'hsk4', 'hsk5', 'hsk6'];

function updateReviewRangeLabel(sliderValue) {
  const n = Number(sliderValue);
  const levels = REVIEW_RANGE_LEVELS.slice(0, n);
  const totalWords = levels.reduce((sum, lvl) => sum + LEVELS[lvl].total, 0);
  document.getElementById('reviewRangeLabel').textContent =
    n === 1 ? 'HSK1' : `HSK1 – HSK${n}`;
  document.getElementById('reviewRangeCount').textContent = `${totalWords} từ`;
}
```

- [ ] **Step 2: Extend `setPrimaryTab` with the `'review'` branch**

In `assets/js/radicals.js`, replace:

```javascript
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
```

with:

```javascript
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
```

- [ ] **Step 3: Syntax check**

Run: `node --check assets/js/radicals.js && node --check assets/js/fast-review.js`
Expected: no output (success) from both.

- [ ] **Step 4: Verify the range-label math in isolation**

Run:

```bash
node -e "
const LEVELS = { hsk1:{total:150}, hsk2:{total:150}, hsk3:{total:300}, hsk4:{total:600}, hsk5:{total:1300}, hsk6:{total:2500} };
const REVIEW_RANGE_LEVELS = ['hsk1','hsk2','hsk3','hsk4','hsk5','hsk6'];
function total(n) { return REVIEW_RANGE_LEVELS.slice(0,n).reduce((s,l)=>s+LEVELS[l].total,0); }
console.log(total(1), total(4), total(6));
"
```

Expected output: `150 1200 4900` (150; 150+150+300+600=1200; sum of all six = 4900).

- [ ] **Step 5: Commit**

```bash
git add assets/js/radicals.js assets/js/fast-review.js
git commit -m "feat: wire review primary tab and range-slider label/count logic"
```

---

### Task 7: State additions for cross-level pool and progress

**Files:**
- Modify: `assets/js/state.js` (append after `reviewSessionLive`, line 55)

**Interfaces:**
- Produces new globals: `reviewWordPool` (array), `reviewProgressByLevel` (object), `reviewLoadedRangeMax` (number, tracks which `n` the currently-loaded pool corresponds to, so "Chơi lại" can detect whether the range changed and needs a re-fetch), `reviewWorker` (Worker instance or `null`).

- [ ] **Step 1: Add the new globals**

In `assets/js/state.js`, after line 55 (`let reviewSessionLive = false;`), add:

```javascript
let reviewWordPool = [];
let reviewProgressByLevel = {};
let reviewLoadedRangeMax = 0;
let reviewWorker = null;
```

- [ ] **Step 2: Syntax check**

Run: `node --check assets/js/state.js`
Expected: no output (success).

- [ ] **Step 3: Commit**

```bash
git add assets/js/state.js
git commit -m "feat: add cross-level fast-review state globals"
```

---

### Task 8: Web Worker for parallel multi-level fetch

**Files:**
- Create: `assets/js/fast-review-worker.js`

**Interfaces:**
- Consumes (via `postMessage` from main thread): `{ levels: string[], dataUrls: string[] }` — parallel arrays, `dataUrls[i]` is the fetch URL for `levels[i]`.
- Produces (via `postMessage` to main thread): on success, `{ ok: true, words: Array<word & {_level: string}> }`; on failure, `{ ok: false, error: string }`.

Workers can't access the page's `LEVELS` global, so the main thread sends the exact `dataUrls` to fetch — the worker doesn't need to know about `LEVELS` at all.

- [ ] **Step 1: Write the worker script**

Create `assets/js/fast-review-worker.js`:

```javascript
// Fast-review worker: fetches multiple level word lists in parallel off the main thread.
self.onmessage = async function (e) {
  const { levels, dataUrls } = e.data;
  try {
    const results = await Promise.all(dataUrls.map(url => fetch(url).then(res => {
      if (!res.ok) throw new Error('fetch failed: ' + url);
      return res.json();
    })));
    const words = [];
    for (let i = 0; i < results.length; i++) {
      const level = levels[i];
      for (const word of results[i]) {
        words.push({ ...word, _level: level });
      }
    }
    self.postMessage({ ok: true, words });
  } catch (err) {
    self.postMessage({ ok: false, error: String(err && err.message || err) });
  }
};
```

- [ ] **Step 2: Syntax check**

Run: `node --check assets/js/fast-review-worker.js`
Expected: no output (success).

- [ ] **Step 3: Verify the tagging logic in isolation (simulating the worker's merge step without actual Worker/fetch APIs)**

Run:

```bash
node -e "
const results = [
  [{id:1,hanzi:'爱',pinyin:'ài'}, {id:2,hanzi:'八',pinyin:'bā'}],
  [{id:1,hanzi:'阿姨',pinyin:'āyí'}],
];
const levels = ['hsk1', 'hsk3'];
const words = [];
for (let i = 0; i < results.length; i++) {
  const level = levels[i];
  for (const word of results[i]) words.push({ ...word, _level: level });
}
console.log(JSON.stringify(words));
console.log('unique keys:', new Set(words.map(w => w._level + ':' + w.id)).size === words.length);
"
```

Expected: JSON array of 3 words each with a `_level` field (`hsk1`, `hsk1`, `hsk3`), and `unique keys: true` confirming the `(_level, id)` compound key has no collisions even though `id: 1` appears twice.

- [ ] **Step 4: Commit**

```bash
git add assets/js/fast-review-worker.js
git commit -m "feat: add fast-review-worker for parallel multi-level word loading"
```

---

### Task 9: Range load orchestration — `startReviewRangeLoad`, progress map building, pool builder update

**Files:**
- Modify: `assets/js/fast-review.js` (add `startReviewRangeLoad`, update `buildReviewPool`)

**Interfaces:**
- Consumes: `reviewWorker`, `reviewWordPool`, `reviewProgressByLevel`, `reviewLoadedRangeMax` (from Task 7); `readSavedLevelProgress(level)` (existing, `levels.js:35-42`); the worker's message contract (from Task 8).
- Produces: `startReviewRangeLoad()` — reads the slider value, spins up (or reuses) `reviewWorker`, populates `reviewWordPool` and `reviewProgressByLevel`, then calls `renderReviewStart()` (updated in Task 10) once loaded.
- Produces: `buildReviewPool()` — **signature change** from the original single-level version: now reads from `reviewWordPool` instead of `WORDS`, and checks `reviewProgressByLevel[word._level][word.id]` instead of `progress[WORDS[i].id]`.

- [ ] **Step 1: Replace `buildReviewPool`**

In `assets/js/fast-review.js`, replace:

```javascript
function buildReviewPool() {
  const pool = [];
  for (let i = 0; i < WORDS.length; i++) {
    if (progress[WORDS[i].id] !== 'known') pool.push(i);
  }
  for (let i = pool.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [pool[i], pool[j]] = [pool[j], pool[i]];
  }
  return pool;
}
```

with:

```javascript
function buildReviewPool() {
  const pool = [];
  for (let i = 0; i < reviewWordPool.length; i++) {
    const word = reviewWordPool[i];
    const levelProgress = reviewProgressByLevel[word._level] || {};
    if (levelProgress[word.id] !== 'known') pool.push(i);
  }
  for (let i = pool.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [pool[i], pool[j]] = [pool[j], pool[i]];
  }
  return pool;
}
```

(Note: `reviewPool` still stores *indices into `reviewWordPool`*, same shape as before when it indexed into `WORDS` — downstream code in Task 10/11 that does `reviewPool[reviewIndex]` to get an index, then looks up the word, keeps working with only the source array swapped.)

- [ ] **Step 2: Add `startReviewRangeLoad`**

Add after `buildReviewPool`:

```javascript
function startReviewRangeLoad() {
  const slider = document.getElementById('reviewRangeSlider');
  const n = Number(slider.value);
  const levels = REVIEW_RANGE_LEVELS.slice(0, n);

  const startBtn = document.getElementById('reviewRangeStart');
  const body = document.getElementById('reviewPickerBody');
  startBtn.disabled = true;
  body.innerHTML = '<div class="loading-text">Đang tải dữ liệu...</div>';

  if (reviewLoadedRangeMax === n && reviewWordPool.length > 0) {
    startBtn.disabled = false;
    renderReviewStart();
    return;
  }

  reviewProgressByLevel = {};
  for (const level of levels) {
    reviewProgressByLevel[level] = readSavedLevelProgress(level);
  }

  if (!reviewWorker) {
    reviewWorker = new Worker('assets/js/fast-review-worker.js');
  }

  reviewWorker.onmessage = function (e) {
    startBtn.disabled = false;
    if (!e.data.ok) {
      body.innerHTML = '<div class="error-text">Không thể tải dữ liệu. Vui lòng thử lại.</div>';
      return;
    }
    reviewWordPool = e.data.words;
    reviewLoadedRangeMax = n;
    renderReviewStart();
  };

  reviewWorker.postMessage({
    levels,
    dataUrls: levels.map(level => LEVELS[level].dataUrl),
  });
}
```

- [ ] **Step 3: Syntax check**

Run: `node --check assets/js/fast-review.js`
Expected: no output (success).

- [ ] **Step 4: Verify `buildReviewPool`'s filtering logic in isolation**

Run:

```bash
node -e "
let reviewWordPool = [
  { id: 1, _level: 'hsk1' },
  { id: 2, _level: 'hsk1' },
  { id: 1, _level: 'hsk3' },
];
let reviewProgressByLevel = { hsk1: { 1: 'known', 2: 'unknown' }, hsk3: {} };

function buildReviewPool() {
  const pool = [];
  for (let i = 0; i < reviewWordPool.length; i++) {
    const word = reviewWordPool[i];
    const levelProgress = reviewProgressByLevel[word._level] || {};
    if (levelProgress[word.id] !== 'known') pool.push(i);
  }
  return pool;
}

const pool = buildReviewPool();
console.log(JSON.stringify(pool));
console.log('expected [1, 2] (indices of hsk1:2-unknown and hsk3:1-unseen):', JSON.stringify(pool) === JSON.stringify([1,2]));
"
```

Expected: `[1,2]` and `true` — index 0 (`hsk1` id 1, `known`) is correctly excluded; indices 1 and 2 (unknown / never-seen) are kept. (Shuffle is omitted from this isolated check since it's already covered by the original fast-review plan's verification and is unchanged here.)

- [ ] **Step 5: Commit**

```bash
git add assets/js/fast-review.js
git commit -m "feat: add cross-level range loading and repoint buildReviewPool at reviewWordPool"
```

---

### Task 10: Repoint session/question rendering at `reviewWordPool`

**Files:**
- Modify: `assets/js/fast-review.js` (`renderReviewStart`, `startReviewSession`, `renderReviewQuestion`, `buildReviewChoices`, `submitReviewTypeAnswer`)

**Interfaces:**
- Consumes: `reviewWordPool`, `reviewPool` (indices into `reviewWordPool`), `reviewCurrentQuestion` (unchanged shape: `{ wordIdx, type }`, where `wordIdx` is now an index into `reviewWordPool`).
- Produces: no new interfaces — internal rewiring only. `renderReviewStart` now renders into `#reviewPickerBody` instead of the old `#reviewStart` (which no longer exists after Task 3).

- [ ] **Step 1: Update `renderReviewStart`**

Replace:

```javascript
function renderReviewStart() {
  document.getElementById('reviewSession').hidden = true;
  document.getElementById('reviewResult').hidden = true;
  const start = document.getElementById('reviewStart');
  start.hidden = false;

  const pool = buildReviewPool();
  reviewPool = pool;

  if (pool.length === 0) {
    start.innerHTML = `
      <div class="review-empty">
        <div class="review-empty-icon">🎉</div>
        <div class="review-empty-title">Bạn đã thuộc hết từ ở cấp độ này!</div>
        <div class="review-empty-msg">Không còn từ nào để ôn nhanh. Hãy học thêm từ mới hoặc chuyển cấp độ khác.</div>
      </div>`;
    return;
  }

  start.innerHTML = `
    <div class="review-intro">
      <div class="review-intro-icon">⚡</div>
      <div class="review-intro-title">Ôn nhanh</div>
      <ul class="review-rules">
        <li>Mỗi câu có <strong>20 giây</strong> để trả lời</li>
        <li>Bạn có <strong>3 mạng</strong> — trả lời sai hoặc hết giờ sẽ mất 1 mạng</li>
        <li>Gõ pinyin hoặc chọn đáp án đúng, xen kẽ ngẫu nhiên</li>
        <li><strong>${pool.length}</strong> từ chưa nhớ đang chờ ôn</li>
      </ul>
      <button class="review-start-btn" onclick="startReviewSession()">Bắt đầu</button>
    </div>`;
}
```

with:

```javascript
function renderReviewStart() {
  const body = document.getElementById('reviewPickerBody');
  body.innerHTML = `
    <div id="reviewSession" hidden></div>
    <div id="reviewResult" hidden></div>
    <div id="reviewStart"></div>`;
  const start = document.getElementById('reviewStart');

  const pool = buildReviewPool();
  reviewPool = pool;

  if (pool.length === 0) {
    start.innerHTML = `
      <div class="review-empty">
        <div class="review-empty-icon">🎉</div>
        <div class="review-empty-title">Bạn đã thuộc hết từ trong phạm vi này!</div>
        <div class="review-empty-msg">Không còn từ nào để ôn nhanh. Hãy học thêm từ mới hoặc chọn phạm vi rộng hơn.</div>
      </div>`;
    return;
  }

  start.innerHTML = `
    <div class="review-intro">
      <div class="review-intro-icon">⚡</div>
      <div class="review-intro-title">Ôn nhanh</div>
      <ul class="review-rules">
        <li>Mỗi câu có <strong>20 giây</strong> để trả lời</li>
        <li>Bạn có <strong>3 mạng</strong> — trả lời sai hoặc hết giờ sẽ mất 1 mạng</li>
        <li>Gõ pinyin hoặc chọn đáp án đúng, xen kẽ ngẫu nhiên</li>
        <li><strong>${pool.length}</strong> từ chưa nhớ đang chờ ôn</li>
      </ul>
      <button class="review-start-btn" onclick="startReviewSession()">Bắt đầu</button>
    </div>`;
}
```

- [ ] **Step 2: Update `buildReviewChoices` to read from `reviewWordPool`**

Replace:

```javascript
function buildReviewChoices(correctWordIdx) {
  const correctPinyin = stripTonePinyin(WORDS[correctWordIdx].pinyin);
  const others = [];
  for (let i = 0; i < WORDS.length; i++) {
    if (i !== correctWordIdx && stripTonePinyin(WORDS[i].pinyin) !== correctPinyin) others.push(i);
  }
  for (let i = others.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [others[i], others[j]] = [others[j], others[i]];
  }
  const distractors = others.slice(0, 3);
  const choices = [correctWordIdx, ...distractors];
  for (let i = choices.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [choices[i], choices[j]] = [choices[j], choices[i]];
  }
  return choices;
}
```

with:

```javascript
function buildReviewChoices(correctWordIdx) {
  const correctPinyin = stripTonePinyin(reviewWordPool[correctWordIdx].pinyin);
  const others = [];
  for (let i = 0; i < reviewWordPool.length; i++) {
    if (i !== correctWordIdx && stripTonePinyin(reviewWordPool[i].pinyin) !== correctPinyin) others.push(i);
  }
  for (let i = others.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [others[i], others[j]] = [others[j], others[i]];
  }
  const distractors = others.slice(0, 3);
  const choices = [correctWordIdx, ...distractors];
  for (let i = choices.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [choices[i], choices[j]] = [choices[j], choices[i]];
  }
  return choices;
}
```

- [ ] **Step 3: Update `renderReviewQuestion`'s word lookups**

Find (inside `renderReviewQuestion`):

```javascript
  const wordIdx = reviewPool[reviewIndex];
  const word = WORDS[wordIdx];
```

Replace with:

```javascript
  const wordIdx = reviewPool[reviewIndex];
  const word = reviewWordPool[wordIdx];
```

Find the multiple-choice rendering block inside the same function:

```javascript
    const choiceIdxs = buildReviewChoices(wordIdx);
    bodyHtml = `
      <div class="review-choices">
        ${choiceIdxs.map(i => `
          <button class="review-choice-btn" data-word-idx="${i}" onclick="submitReviewChoice(${i})">
            ${WORDS[i].pinyin}
          </button>`).join('')}
      </div>
      <div class="review-feedback" id="reviewFeedback"></div>`;
```

Replace the `WORDS[i].pinyin` reference:

```javascript
    const choiceIdxs = buildReviewChoices(wordIdx);
    bodyHtml = `
      <div class="review-choices">
        ${choiceIdxs.map(i => `
          <button class="review-choice-btn" data-word-idx="${i}" onclick="submitReviewChoice(${i})">
            ${reviewWordPool[i].pinyin}
          </button>`).join('')}
      </div>
      <div class="review-feedback" id="reviewFeedback"></div>`;
```

- [ ] **Step 4: Update `submitReviewTypeAnswer`'s word lookup**

Find:

```javascript
function submitReviewTypeAnswer() {
  if (reviewAnswered) return;
  const input = document.getElementById('reviewTypeInput');
  const word = WORDS[reviewCurrentQuestion.wordIdx];
  const isCorrect = pinyinLooseMatch(input.value, word.pinyin);
  gradeReviewAnswer(isCorrect);
}
```

Replace with:

```javascript
function submitReviewTypeAnswer() {
  if (reviewAnswered) return;
  const input = document.getElementById('reviewTypeInput');
  const word = reviewWordPool[reviewCurrentQuestion.wordIdx];
  const isCorrect = pinyinLooseMatch(input.value, word.pinyin);
  gradeReviewAnswer(isCorrect);
}
```

- [ ] **Step 5: Syntax check**

Run: `node --check assets/js/fast-review.js`
Expected: no output (success).

- [ ] **Step 6: Verify no remaining `WORDS[` references inside fast-review.js**

Run: `grep -n "WORDS\[" assets/js/fast-review.js`
Expected: no matches (all replaced with `reviewWordPool[`) except inside `gradeReviewAnswer`, which is handled in Task 11.

- [ ] **Step 7: Commit**

```bash
git add assets/js/fast-review.js
git commit -m "refactor: repoint fast-review question rendering at reviewWordPool"
```

---

### Task 11: Repoint grading at per-level progress, result screen navigation

**Files:**
- Modify: `assets/js/fast-review.js` (`gradeReviewAnswer`, `renderReviewResult`)

**Interfaces:**
- Consumes: `saveLevelProgress(level, progressObj)` (from Task 2), `recordDailyStudy(wordId, level)` (from Task 1), `reviewProgressByLevel`.
- Produces: `gradeReviewAnswer` no longer touches the flashcard-mode `progress`/`saveProgress()` globals. Result screen's "Về flashcard" button becomes "Chọn lại phạm vi" wired to `renderReviewRangePicker()` (new), and a separate always-available exit is the `📚 Từ vựng` primary tab (no button needed).

- [ ] **Step 1: Update `gradeReviewAnswer`**

Find:

```javascript
function gradeReviewAnswer(isCorrect) {
  if (reviewAnswered) return;
  reviewAnswered = true;
  if (reviewTimer) { clearInterval(reviewTimer); reviewTimer = null; }

  const wordIdx = reviewCurrentQuestion.wordIdx;
  const word = WORDS[wordIdx];
  progress[word.id] = isCorrect ? 'known' : 'unknown';
  saveProgress();
  recordDailyStudy(word.id);
  checkCelebration();
```

Replace the middle block with:

```javascript
function gradeReviewAnswer(isCorrect) {
  if (reviewAnswered) return;
  reviewAnswered = true;
  if (reviewTimer) { clearInterval(reviewTimer); reviewTimer = null; }

  const wordIdx = reviewCurrentQuestion.wordIdx;
  const word = reviewWordPool[wordIdx];
  if (!reviewProgressByLevel[word._level]) reviewProgressByLevel[word._level] = {};
  reviewProgressByLevel[word._level][word.id] = isCorrect ? 'known' : 'unknown';
  saveLevelProgress(word._level, reviewProgressByLevel[word._level]);
  recordDailyStudy(word.id, word._level);
```

(The `checkCelebration()` call is removed — it reads the flashcard-mode's single-level `WORDS`/`progress` globals, which are unrelated to a cross-level review session; there's no single-level "100% known" event to detect here.)

- [ ] **Step 2: Add `renderReviewRangePicker` and update the result screen's action buttons**

Find:

```javascript
      <div class="review-result-actions">
        <button class="review-again-btn" onclick="renderReviewStart()">Chơi lại</button>
        <button class="review-back-btn" onclick="setViewMode('cards')">Về flashcard</button>
      </div>
    </div>`;
}
```

Replace with:

```javascript
      <div class="review-result-actions">
        <button class="review-again-btn" onclick="renderReviewStart()">Chơi lại</button>
        <button class="review-back-btn" onclick="renderReviewRangePicker()">Chọn lại phạm vi</button>
      </div>
    </div>`;
}

function renderReviewRangePicker() {
  document.getElementById('reviewPickerBody').innerHTML = '';
}
```

- [ ] **Step 3: Syntax check**

Run: `node --check assets/js/fast-review.js`
Expected: no output (success).

- [ ] **Step 4: Verify no remaining references to flashcard-mode globals inside fast-review.js**

Run: `grep -n "\bprogress\[\|saveProgress()\|\bWORDS\[" assets/js/fast-review.js`
Expected: no matches — confirms `gradeReviewAnswer` and all other functions in this file no longer touch the single-level `progress`/`WORDS` globals.

- [ ] **Step 5: Verify the grading logic in isolation**

Run:

```bash
node -e "
let reviewProgressByLevel = { hsk1: {}, hsk3: {} };
const savedKeys = [];
function saveLevelProgress(level, obj) { savedKeys.push(level); }
function recordDailyStudy(id, level) { console.log('recorded', level, id); }

function gradeReviewAnswer(word, isCorrect) {
  if (!reviewProgressByLevel[word._level]) reviewProgressByLevel[word._level] = {};
  reviewProgressByLevel[word._level][word.id] = isCorrect ? 'known' : 'unknown';
  saveLevelProgress(word._level, reviewProgressByLevel[word._level]);
  recordDailyStudy(word.id, word._level);
}

gradeReviewAnswer({ id: 5, _level: 'hsk3' }, true);
gradeReviewAnswer({ id: 5, _level: 'hsk1' }, false);
console.log(JSON.stringify(reviewProgressByLevel));
console.log('saved to both levels independently:', savedKeys.join(',') === 'hsk3,hsk1');
"
```

Expected output shows `recorded hsk3 5` and `recorded hsk1 5`, the progress object shows `{"hsk1":{"5":"unknown"},"hsk3":{"5":"known"}}` (same numeric id, different levels, no collision), and `saved to both levels independently: true`.

- [ ] **Step 6: Commit**

```bash
git add assets/js/fast-review.js
git commit -m "feat: grade cross-level review answers into each word's own level progress store"
```

---

### Task 12: `abandonReviewSession` and `goBackToPicker` cleanup review

**Files:**
- Modify: `assets/js/levels.js` (`goBackToPicker` — verify/adjust the existing `abandonReviewSession()` call is still correct)
- Read-only check: `assets/js/fast-review.js` (`abandonReviewSession`, already correct from prior work)

**Interfaces:**
- Consumes: `abandonReviewSession()` (already exists, unchanged signature).

This task is a verification pass, not new code — Task 6 already added an `abandonReviewSession()` call to `setPrimaryTab` when leaving `'review'` for another primary tab. `goBackToPicker()` (the "← Chọn cấp độ khác" button inside the single-level flashcard screen) is a separate code path that returns to `screenPicker`, not `screenReviewPicker` — it cannot be reached while a review session is live (Fast-Review no longer lives inside a level's flashcard screen), so its existing `abandonReviewSession()` call is now technically redundant but harmless (the guard inside `abandonReviewSession` is idempotent). Leave it as-is; removing it saves nothing and risks nothing being missed if entry points change again later.

- [ ] **Step 1: Confirm `abandonReviewSession` is idempotent**

Run: `grep -n "function abandonReviewSession" -A 5 assets/js/fast-review.js`
Expected:

```javascript
function abandonReviewSession() {
  if (reviewTimer) { clearInterval(reviewTimer); reviewTimer = null; }
  reviewAnswered = true;
  reviewSessionLive = false;
}
```

Confirm: calling this multiple times in a row, or when no session is live (`reviewTimer` already `null`), produces no error and no observable side effect beyond the (already-false) flags being reset — safe to call from multiple entry points.

- [ ] **Step 2: Confirm `setPrimaryTab`'s new cleanup call (Task 6) covers the only live-session exit path**

Run: `grep -n "abandonReviewSession()" assets/js/*.js`
Expected: two matches — one in `setPrimaryTab` (Task 6, guards tab switches away from `'review'`), one in `goBackToPicker` (pre-existing, now unreachable during a live session but harmless).

- [ ] **Step 3: No commit needed for this task** — verification only, no file changes.

---

### Task 13: Manual verification pass and cleanup of stale `.review-back-btn` copy expectations

**Files:**
- Read-only verification across: `flashcards.html`, `assets/js/fast-review.js`, `assets/js/fast-review-worker.js`, `assets/js/radicals.js`, `assets/js/levels.js`, `assets/js/storage.js`, `assets/js/state.js`, `assets/css/*.css`

**Interfaces:** none — this task produces no new code, only confirms the prior 12 tasks compose correctly.

- [ ] **Step 1: Full syntax check across every modified JS file**

Run:

```bash
for f in assets/js/state.js assets/js/storage.js assets/js/levels.js assets/js/radicals.js assets/js/vocabulary-overview.js assets/js/fast-review.js assets/js/fast-review-worker.js; do
  node --check "$f" && echo "OK $f"
done
```

Expected: `OK <file>` for all seven files.

- [ ] **Step 2: Confirm no orphaned DOM id references**

Run:

```bash
grep -o 'getElementById(.[a-zA-Z]*.)'  assets/js/fast-review.js | sort -u
```

For each id printed, confirm it exists in `flashcards.html` via `grep -n "id=\"<id>\"" flashcards.html`. Expected ids: `reviewPickerBody`, `reviewStart`, `reviewSession`, `reviewResult`, `reviewTimerFill`, `reviewTypeInput`, `reviewFeedback`, `reviewRangeSlider`, `reviewRangeLabel`, `reviewRangeCount`, `reviewRangeStart`. Note `reviewSession`/`reviewResult`/`reviewStart` are created dynamically by `renderReviewStart()`'s `body.innerHTML` assignment (Task 10, Step 1) rather than existing statically in `flashcards.html` — confirm that assignment runs before any code tries to `getElementById` them (it does: `startReviewRangeLoad` → `renderReviewStart` → the three divs are created → `start.innerHTML` is set — all synchronous, same call stack).

- [ ] **Step 3: Confirm the full click-path chain compiles logically, end to end**

Trace and confirm each link by reading the relevant function (no code changes, just confirm the chain holds):

1. `setPrimaryTab('review')` → shows `#screenReviewPicker`, calls `updateReviewRangeLabel`.
2. User drags slider → `oninput="updateReviewRangeLabel(this.value)"` updates label/count live.
3. User clicks "Bắt đầu" → `startReviewRangeLoad()` → worker fetches → `onmessage` sets `reviewWordPool`/`reviewLoadedRangeMax` → `renderReviewStart()`.
4. `renderReviewStart()` → `buildReviewPool()` (reads `reviewWordPool`/`reviewProgressByLevel`) → renders intro or empty state.
5. User clicks "Bắt đầu" (session) → `startReviewSession()` → `renderReviewQuestion()` (reads `reviewWordPool[reviewPool[reviewIndex]]`).
6. User answers → `gradeReviewAnswer()` (writes `reviewProgressByLevel[word._level][word.id]`, calls `saveLevelProgress`/`recordDailyStudy`) → `setTimeout` → next question or `endReviewSession()`.
7. `endReviewSession()` → `renderReviewResult()` → "Chơi lại" re-enters step 4 with the same pool; "Chọn lại phạm vi" → `renderReviewRangePicker()` clears `#reviewPickerBody`, leaving the always-visible slider/Bắt đầu controls above it as the way back into step 2-3.
8. User clicks `📚 Từ vựng` primary tab at any point → `setPrimaryTab('vocab')` → `abandonReviewSession()` runs (Task 6) before hiding `#screenReviewPicker`.

Expected: every arrow above is backed by an actual function call verified to exist in the current file contents (cross-check with the diffs from Tasks 1-11) — no missing link.

- [ ] **Step 4: If a browser is available, do a live smoke test**

Run: `python3 -m http.server 8791` from the repo root, open `http://localhost:8791/flashcards.html`, click `⚡ Ôn nhanh`, drag the slider to HSK2, click "Bắt đầu", answer 2-3 questions (mix of typed and multiple-choice), let one timeout, finish or lose the session, click "Chọn lại phạm vi", change the range to HSK1, start again, then switch to `📚 Từ vựng` mid-session and confirm (via browser devtools Network/Performance, or simply waiting past 20s and checking `localStorage.getItem('hsk_hsk2_progress_v2')` didn't change) that the abandoned session's timer stopped.

If no browser is available (confirmed in this repo's environment history — no Chromium/Chrome install), skip this step and rely on Steps 1-3's static verification, and say so explicitly rather than claiming a live test was performed.

- [ ] **Step 5: Final commit if any fixes were needed during verification**

Only if Steps 1-4 surfaced an issue requiring a code change:

```bash
git add -A
git commit -m "fix: <describe the specific issue found during verification>"
```

If no issues were found, no commit is needed for this task.
