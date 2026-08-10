# Fast-Review (⚡ Ôn nhanh) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a third "⚡ Ôn nhanh" tab to the flashcard screen that runs a Memrise-style, 20-second-per-question, 3-lives speed quiz over not-yet-known words, updating the same `progress`/streak data the flashcard tab uses.

**Architecture:** New `assets/js/fast-review.js` module (pool building, timer, question rendering/grading, screen transitions) and `assets/css/fast-review.css` (start/session/result screens), wired into `flashcards.html` as a third view alongside the existing `'cards'` / `'overview'` views. `setViewMode` in `vocabulary-overview.js` is extended to accept `'review'`. No new persistence — reuses `progress`, `saveProgress()`, `recordDailyStudy()`.

**Tech Stack:** Vanilla JS (ES2017, no build step, no bundler), plain CSS with custom properties, static HTML. No test framework exists in this repo (confirmed: no `package.json`, no JS test files) — verification is manual, in-browser, per the project's existing convention (see CLAUDE.md: "start the dev server and use the feature in a browser before reporting the task as complete").

## Global Constraints

- Timer is fixed at 20s per question, not configurable (spec: "nó nên bắt đầu bằng một con số cố định ví dụ 20s").
- Lives: exactly 3. Wrong answer OR timeout both cost 1 life.
- Word pool: current level's `WORDS` filtered to `progress[w.id] !== 'known'`, shuffled once at session start, no repeats within a session.
- Question type is chosen per-question, ~50/50 random between "type pinyin" and "multiple choice" (no forced alternation).
- Pinyin typed-answer matching: case-insensitive, tone-mark-stripped, whitespace-collapsed loose match.
- Multiple choice: 4 buttons (1 correct pinyin-with-tone-marks + 3 random distractors from same level), click to answer.
- Every answered question calls `recordDailyStudy(wordId)` and `saveProgress()`, and sets `progress[wordId]` to `'known'` (correct) or `'unknown'` (wrong/timeout) — same mechanism the flashcard tab already uses.
- Session ends when lives hit 0 or pool is exhausted, whichever first.
- All user-facing copy in Vietnamese, matching existing app tone (see `flashcard.js`, `progress.js` for examples).
- No new localStorage keys, no new theme colors — reuse `--accent`, `--success-text`, `--danger-text`, `--success-bg`, `--danger-bg`, `--border`, `--card-bg`, `--radius-lg`, `--radius-md` from `assets/css/base.css`.
- Follow existing code style: no semicolonless lines, 2-space indent, inline `onclick="fn()"` handlers matching the rest of the codebase (not addEventListener-based), matching `flashcard.js`/`progress.js` conventions.

---

### Task 1: State variables and pinyin-matching utility

**Files:**
- Modify: `assets/js/state.js` (append after line 44, the existing `overviewStatus` global)
- Create: `assets/js/fast-review.js` (new file, first section only in this task)
- Modify: `flashcards.html:332` (add `<script src="assets/js/fast-review.js"></script>` after the existing `flashcards.js` script tag — actually before it, alongside other feature modules at line 322-326, so it loads before `assets/flashcards.js` entry point)

**Interfaces:**
- Produces: `stripTonePinyin(text)` — string → normalized string (lowercase, tone marks stripped to base vowel, whitespace collapsed to single spaces, trimmed).
- Produces: `pinyinLooseMatch(input, target)` — (string, string) → boolean.
- Produces new globals in `state.js`: `reviewPool`, `reviewIndex`, `reviewLives`, `reviewScore`, `reviewStreak`, `reviewBestStreak`, `reviewTimer`, `reviewTimeLeft`, `reviewCurrentQuestion`, `reviewAnswered`.

This task has no UI yet — it's pure logic, verified via browser console.

- [ ] **Step 1: Add fast-review state globals to `state.js`**

Open `assets/js/state.js` and add after line 44 (`let overviewStatus = 'all';`):

```javascript
let reviewPool = [];
let reviewIndex = 0;
let reviewLives = 3;
let reviewScore = 0;
let reviewStreak = 0;
let reviewBestStreak = 0;
let reviewTimer = null;
let reviewTimeLeft = 20;
let reviewCurrentQuestion = null;
let reviewAnswered = false;
```

- [ ] **Step 2: Create `assets/js/fast-review.js` with the pinyin-matching utility**

```javascript
// Fast-review (speed quiz) mode: pool building, timer, grading, screen transitions.
const REVIEW_TONE_MARKS = {
  'ā':'a','á':'a','ǎ':'a','à':'a',
  'ē':'e','é':'e','ě':'e','è':'e',
  'ī':'i','í':'i','ǐ':'i','ì':'i',
  'ō':'o','ó':'o','ǒ':'o','ò':'o',
  'ū':'u','ú':'u','ǔ':'u','ù':'u',
  'ǖ':'v','ǘ':'v','ǚ':'v','ǜ':'v','ü':'v',
};

function stripTonePinyin(text) {
  return String(text || '')
    .toLowerCase()
    .split('')
    .map(ch => REVIEW_TONE_MARKS[ch] || ch)
    .join('')
    .replace(/\s+/g, ' ')
    .trim();
}

function pinyinLooseMatch(input, target) {
  return stripTonePinyin(input) === stripTonePinyin(target);
}
```

- [ ] **Step 3: Wire the script into `flashcards.html`**

In `flashcards.html`, find the script block around line 319-332. Insert the new script tag after `vocabulary-overview.js` (line 322) and before `flashcard.js` (line 323), since fast-review depends on `state.js`/`storage.js`/`levels.js` but should load before the entry-point `assets/flashcards.js`:

```html
<script src="assets/js/vocabulary-overview.js"></script>
<script src="assets/js/fast-review.js"></script>
<script src="assets/js/flashcard.js"></script>
```

- [ ] **Step 4: Manually verify in browser console**

Run: open `flashcards.html` in a browser (e.g. `python3 -m http.server 8000` from repo root, then visit `http://localhost:8000/flashcards.html`), open devtools console, run:

```javascript
stripTonePinyin("Nǐ Hǎo")   // expect "ni hao"
pinyinLooseMatch("ni hao", "nǐ hǎo")  // expect true
pinyinLooseMatch("nihao", "nǐ hǎo")   // expect false (space required)
pinyinLooseMatch("  NI   HAO  ", "nǐ hǎo") // expect true
```

Expected: all four calls return the values noted in the comments.

- [ ] **Step 5: Commit**

```bash
git add assets/js/state.js assets/js/fast-review.js flashcards.html
git commit -m "feat: add fast-review state and pinyin loose-matching utility"
```

---

### Task 2: HTML scaffold — third tab and review panel container

**Files:**
- Modify: `flashcards.html:135-140` (view-tabs row)
- Modify: `flashcards.html` (add `#reviewView` panel after `#overviewView`, which per current numbering ends around line 210 — locate the closing `</div>` of `overviewView` and insert after it)
- Modify: `flashcards.html:15` (stylesheet import — actually `assets/flashcards.css` already `@import`s component sheets, so this task adds the import there instead)
- Modify: `assets/flashcards.css` (add `@import url("css/fast-review.css");`)
- Create: `assets/css/fast-review.css` (empty placeholder with a header comment; populated in Task 4)

**Interfaces:**
- Consumes: none new.
- Produces: DOM elements `#reviewTab`, `#reviewView`, `#reviewStart`, `#reviewSession`, `#reviewResult` (three sub-screens inside `#reviewView`, toggled via `hidden`), that Task 3/4 code will populate and control.

- [ ] **Step 1: Add the tab button**

In `flashcards.html`, locate the `view-tabs` block (lines 135-140):

```html
    <div class="view-tabs" role="tablist" aria-label="Chế độ xem">
      <button id="flashcardTab" class="view-tab active" role="tab" aria-selected="true"
        aria-controls="studyView" onclick="setViewMode('cards')">🗂 Học flashcard</button>
      <button id="overviewTab" class="view-tab" role="tab" aria-selected="false"
        aria-controls="overviewView" onclick="setViewMode('overview')">📋 Tổng quan từ vựng</button>
    </div>
```

Replace with:

```html
    <div class="view-tabs" role="tablist" aria-label="Chế độ xem">
      <button id="flashcardTab" class="view-tab active" role="tab" aria-selected="true"
        aria-controls="studyView" onclick="setViewMode('cards')">🗂 Học flashcard</button>
      <button id="overviewTab" class="view-tab" role="tab" aria-selected="false"
        aria-controls="overviewView" onclick="setViewMode('overview')">📋 Tổng quan từ vựng</button>
      <button id="reviewTab" class="view-tab" role="tab" aria-selected="false"
        aria-controls="reviewView" onclick="setViewMode('review')">⚡ Ôn nhanh</button>
    </div>
```

- [ ] **Step 2: Add the `#reviewView` container**

Find the end of the `#overviewView` block in `flashcards.html` (it is the last child of `#screenCards`, closing right before the outer `</div>` that closes `screenCards`). Insert a new sibling `<div id="reviewView">` immediately after `#overviewView`'s closing `</div>`, containing three empty sub-screens:

```html
    <div id="reviewView" role="tabpanel" aria-labelledby="reviewTab" hidden>
      <div id="reviewStart"></div>
      <div id="reviewSession" hidden></div>
      <div id="reviewResult" hidden></div>
    </div>
```

Run `grep -n "overviewView\|screenCards" flashcards.html` first to find the exact line number of `#overviewView`'s closing tag before editing, since line numbers shift as earlier tasks edit the file.

- [ ] **Step 3: Create the CSS file and wire the import**

Create `assets/css/fast-review.css`:

```css
/* Fast-review (⚡ Ôn nhanh) — start/session/result screens */
```

In `assets/flashcards.css`, add after the last `@import` line (`@import url("css/streak-history.css");`):

```css
@import url("css/fast-review.css");
```

- [ ] **Step 4: Manually verify**

Run: serve the app (`python3 -m http.server 8000` from repo root), open `http://localhost:8000/flashcards.html`, pick any level. Confirm the "⚡ Ôn nhanh" tab appears as a third tab and is clickable (it will show a blank panel — that's expected, `setViewMode` doesn't know about `'review'` yet so clicking currently does nothing since `setViewMode` rejects unknown modes; this is fixed in Task 3).

Expected: tab renders correctly styled (same pill shape as the other two tabs), no console errors on page load.

- [ ] **Step 5: Commit**

```bash
git add flashcards.html assets/flashcards.css assets/css/fast-review.css
git commit -m "feat: scaffold fast-review tab and panel containers"
```

---

### Task 3: Wire `setViewMode('review')` and the start screen

**Files:**
- Modify: `assets/js/vocabulary-overview.js:2-30` (`setViewMode`)
- Modify: `assets/js/fast-review.js` (append start-screen rendering + pool-building logic)

**Interfaces:**
- Consumes: `stripTonePinyin`/`pinyinLooseMatch` (Task 1), `currentLevel`, `WORDS`, `progress`, `LEVELS` (existing globals), `reviewPool`/`reviewIndex`/`reviewLives`/`reviewScore`/`reviewStreak`/`reviewBestStreak` (Task 1 state).
- Produces: `setViewMode` now accepts `'review'`. `renderReviewStart()` — no args, renders into `#reviewStart`. `buildReviewPool()` — no args, returns `Array<number>` of `WORDS` indices, also assigns to `reviewPool`. `startReviewSession()` — no args, begins a session (stub call in this task; full session logic lands in Task 4, but the function must exist and be referenced by the start screen's button so Task 4 can fill it in without touching this task's HTML again).

- [ ] **Step 1: Extend `setViewMode` to accept `'review'`**

In `assets/js/vocabulary-overview.js`, replace the full `setViewMode` function (lines 2-30):

```javascript
function setViewMode(mode) {
  if (!currentLevel || !['cards', 'overview', 'review'].includes(mode)) return;

  stopSpeech();
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
}
```

- [ ] **Step 2: Add pool builder and start-screen renderer to `fast-review.js`**

Append to `assets/js/fast-review.js`:

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

- [ ] **Step 3: Add a stub `startReviewSession` so the button doesn't error**

Append to `assets/js/fast-review.js` (this is intentionally minimal — Task 4 replaces it with the full session engine):

```javascript
function startReviewSession() {
  reviewIndex = 0;
  reviewLives = 3;
  reviewScore = 0;
  reviewStreak = 0;
  reviewBestStreak = 0;
  document.getElementById('reviewStart').hidden = true;
  document.getElementById('reviewSession').hidden = false;
  document.getElementById('reviewSession').textContent = 'Phiên ôn tập sẽ được xây dựng ở bước tiếp theo.';
}
```

- [ ] **Step 4: Manually verify**

Run: serve the app, open a level with at least one non-`known` word (e.g. a fresh level with nothing marked yet), click "⚡ Ôn nhanh". Confirm the rule list renders with the correct pool count. Click "Bắt đầu" and confirm it switches to the (stub) session panel without console errors.

Then mark every word in a small test scenario as known (or check a level where you've already completed everything) and reopen the tab — confirm the empty-state message renders instead.

Expected: no console errors in either case; pool count in the rules list matches `WORDS.length - (known count)` for the level.

- [ ] **Step 5: Commit**

```bash
git add assets/js/vocabulary-overview.js assets/js/fast-review.js
git commit -m "feat: add fast-review start screen and pool builder"
```

---

### Task 4: Session engine — timer, question rendering, grading

**Files:**
- Modify: `assets/js/fast-review.js` (replace the Task 3 stub `startReviewSession`, add question generation, timer, answer handling)

**Interfaces:**
- Consumes: `reviewPool`, `reviewIndex`, `reviewLives`, `reviewScore`, `reviewStreak`, `reviewBestStreak`, `reviewTimer`, `reviewTimeLeft`, `reviewCurrentQuestion`, `reviewAnswered` (Task 1 state), `stripTonePinyin`/`pinyinLooseMatch` (Task 1), `WORDS`, `progress`, `saveProgress()` (from `storage.js`), `recordDailyStudy()` (from `progress.js`).
- Produces: `startReviewSession()` (replaces Task 3 stub — same name/signature, no args), `renderReviewQuestion()`, `pickReviewQuestionType()` → `'type' | 'choice'`, `buildReviewChoices(correctIdx)` → `Array<number>` (4 word indices, one correct, shuffled), `submitReviewTypeAnswer()`, `submitReviewChoice(chosenIdx)`, `reviewTick()`, `gradeReviewAnswer(isCorrect)`, `endReviewSession()` — no args, shows `#reviewResult` (calls into Task 5's `renderReviewResult()`, so Task 5 must define that function name exactly).

- [ ] **Step 1: Replace the stub `startReviewSession` and add the question-type/choice builders**

In `assets/js/fast-review.js`, delete the Task 3 stub `startReviewSession` function and replace it with:

```javascript
function startReviewSession() {
  reviewIndex = 0;
  reviewLives = 3;
  reviewScore = 0;
  reviewStreak = 0;
  reviewBestStreak = 0;
  document.getElementById('reviewStart').hidden = true;
  document.getElementById('reviewResult').hidden = true;
  document.getElementById('reviewSession').hidden = false;
  renderReviewQuestion();
}

function pickReviewQuestionType() {
  return Math.random() < 0.5 ? 'type' : 'choice';
}

function buildReviewChoices(correctWordIdx) {
  const others = [];
  for (let i = 0; i < WORDS.length; i++) {
    if (i !== correctWordIdx) others.push(i);
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

- [ ] **Step 2: Add the question renderer**

Append to `assets/js/fast-review.js`:

```javascript
function renderReviewQuestion() {
  if (reviewTimer) { clearInterval(reviewTimer); reviewTimer = null; }
  if (reviewLives <= 0 || reviewIndex >= reviewPool.length) { endReviewSession(); return; }

  const wordIdx = reviewPool[reviewIndex];
  const word = WORDS[wordIdx];
  const type = pickReviewQuestionType();
  reviewCurrentQuestion = { wordIdx, type };
  reviewAnswered = false;
  reviewTimeLeft = 20;

  const livesHtml = '♥'.repeat(reviewLives) + '♡'.repeat(3 - reviewLives);
  const header = `
    <div class="review-header">
      <div class="review-lives" aria-label="${reviewLives} mạng còn lại">${livesHtml}</div>
      <div class="review-progress-text">${reviewIndex + 1} / ${reviewPool.length}</div>
    </div>
    <div class="review-timer-track"><div class="review-timer-fill" id="reviewTimerFill"></div></div>
    <div class="review-question-word">
      <div class="review-hanzi">${word.hanzi}</div>
      <div class="review-meaning">${word.meaning}</div>
    </div>`;

  let bodyHtml;
  if (type === 'type') {
    bodyHtml = `
      <div class="review-answer-area">
        <input type="text" id="reviewTypeInput" class="review-type-input"
          autocomplete="off" autocapitalize="off" spellcheck="false"
          placeholder="Gõ pinyin (không dấu)..."
          onkeydown="if(event.key==='Enter') submitReviewTypeAnswer()">
        <button class="review-submit-btn" onclick="submitReviewTypeAnswer()">Trả lời</button>
      </div>
      <div class="review-feedback" id="reviewFeedback"></div>`;
  } else {
    const choiceIdxs = buildReviewChoices(wordIdx);
    bodyHtml = `
      <div class="review-choices">
        ${choiceIdxs.map(i => `
          <button class="review-choice-btn" data-word-idx="${i}" onclick="submitReviewChoice(${i})">
            ${WORDS[i].pinyin}
          </button>`).join('')}
      </div>
      <div class="review-feedback" id="reviewFeedback"></div>`;
  }

  document.getElementById('reviewSession').innerHTML = header + bodyHtml;

  const input = document.getElementById('reviewTypeInput');
  if (input) input.focus();

  reviewTimer = setInterval(reviewTick, 1000);
  updateReviewTimerBar();
}

function updateReviewTimerBar() {
  const fill = document.getElementById('reviewTimerFill');
  if (!fill) return;
  const pct = Math.max(0, (reviewTimeLeft / 20) * 100);
  fill.style.width = pct + '%';
  fill.classList.toggle('review-timer-low', reviewTimeLeft <= 5);
}

function reviewTick() {
  reviewTimeLeft -= 1;
  updateReviewTimerBar();
  if (reviewTimeLeft <= 0) {
    clearInterval(reviewTimer);
    reviewTimer = null;
    gradeReviewAnswer(false);
  }
}
```

- [ ] **Step 3: Add answer submission and grading**

Append to `assets/js/fast-review.js`:

```javascript
function submitReviewTypeAnswer() {
  if (reviewAnswered) return;
  const input = document.getElementById('reviewTypeInput');
  const word = WORDS[reviewCurrentQuestion.wordIdx];
  const isCorrect = pinyinLooseMatch(input.value, word.pinyin);
  gradeReviewAnswer(isCorrect);
}

function submitReviewChoice(chosenIdx) {
  if (reviewAnswered) return;
  const isCorrect = chosenIdx === reviewCurrentQuestion.wordIdx;
  gradeReviewAnswer(isCorrect);
}

function gradeReviewAnswer(isCorrect) {
  if (reviewAnswered) return;
  reviewAnswered = true;
  if (reviewTimer) { clearInterval(reviewTimer); reviewTimer = null; }

  const wordIdx = reviewCurrentQuestion.wordIdx;
  const word = WORDS[wordIdx];
  progress[word.id] = isCorrect ? 'known' : 'unknown';
  saveProgress();
  recordDailyStudy(word.id);

  if (isCorrect) {
    reviewScore += 1;
    reviewStreak += 1;
    if (reviewStreak > reviewBestStreak) reviewBestStreak = reviewStreak;
  } else {
    reviewLives -= 1;
    reviewStreak = 0;
  }

  const feedback = document.getElementById('reviewFeedback');
  if (feedback) {
    feedback.textContent = isCorrect ? 'Chính xác!' : `Sai rồi. Đáp án: ${word.pinyin}`;
    feedback.className = 'review-feedback show ' + (isCorrect ? 'review-feedback--correct' : 'review-feedback--wrong');
  }
  document.querySelectorAll('.review-choice-btn').forEach(btn => {
    btn.disabled = true;
    if (Number(btn.dataset.wordIdx) === wordIdx) btn.classList.add('review-choice-btn--correct');
  });

  setTimeout(() => {
    reviewIndex += 1;
    renderReviewQuestion();
  }, 900);
}
```

- [ ] **Step 4: Manually verify**

Run: serve the app, start a review session. Verify:
- Timer bar counts down visibly over 20s and turns into the "low" state near the end (check class `review-timer-low` appears in devtools when `reviewTimeLeft <= 5`).
- Typing the correct pinyin (no tones, e.g. "ai" for 爱) and pressing Enter shows "Chính xác!" and advances after ~0.9s.
- Typing a wrong answer decrements a heart and shows the correct answer.
- Multiple-choice questions render 4 clickable buttons; clicking the correct one shows success, clicking wrong decrements a heart and highlights the correct button.
- Letting the timer hit 0 without answering counts as wrong (heart lost, feedback shown).
- Losing all 3 hearts calls `endReviewSession()` — confirm in console that it's called (Task 5 implements its body; for now it's fine if this throws `ReferenceError: endReviewSession is not defined`, expected until Task 5 lands, but note it in the review so Task 5 fixes it).

Expected: all behaviors above match except the final `endReviewSession` call, which is completed by Task 5.

- [ ] **Step 5: Commit**

```bash
git add assets/js/fast-review.js
git commit -m "feat: add fast-review session engine (timer, questions, grading)"
```

---

### Task 5: Result screen and CSS

**Files:**
- Modify: `assets/js/fast-review.js` (add `endReviewSession()` and `renderReviewResult()`)
- Modify: `assets/css/fast-review.css` (full styling for start/session/result screens)

**Interfaces:**
- Consumes: `reviewScore`, `reviewPool`, `reviewBestStreak` (Task 1/4 state), `renderReviewStart()` (Task 3), `setViewMode` (Task 3).
- Produces: `endReviewSession()`, `renderReviewResult()` — both no-arg.

- [ ] **Step 1: Add `endReviewSession` and `renderReviewResult` to `fast-review.js`**

`reviewIndex` is incremented (in Task 4's `gradeReviewAnswer` → `renderReviewQuestion` flow) once per answered question, right after grading. By the time `endReviewSession` fires — either lives hit 0 or `reviewIndex >= reviewPool.length` — `reviewIndex` already equals the count of answered questions, capped at the pool size. So the total answered is simply `Math.min(reviewIndex, reviewPool.length)`.

```javascript
function endReviewSession() {
  if (reviewTimer) { clearInterval(reviewTimer); reviewTimer = null; }
  document.getElementById('reviewSession').hidden = true;
  renderReviewResult();
}

function renderReviewResult() {
  const result = document.getElementById('reviewResult');
  result.hidden = false;
  const total = Math.min(reviewIndex, reviewPool.length);
  const survived = reviewLives > 0;

  result.innerHTML = `
    <div class="review-result">
      <div class="review-result-icon">${survived ? '🏁' : '💔'}</div>
      <div class="review-result-title">${survived ? 'Hoàn thành!' : 'Hết mạng!'}</div>
      <div class="review-result-stats">
        <div class="review-result-stat">
          <div class="review-result-num">${reviewScore}</div>
          <div class="review-result-lbl">câu đúng</div>
        </div>
        <div class="review-result-stat">
          <div class="review-result-num">${total}</div>
          <div class="review-result-lbl">tổng số câu</div>
        </div>
        <div class="review-result-stat">
          <div class="review-result-num">${reviewBestStreak}</div>
          <div class="review-result-lbl">chuỗi đúng dài nhất</div>
        </div>
      </div>
      <div class="review-result-actions">
        <button class="review-again-btn" onclick="renderReviewStart()">Chơi lại</button>
        <button class="review-back-btn" onclick="setViewMode('cards')">Về flashcard</button>
      </div>
    </div>`;
}
```

- [ ] **Step 2: Write the CSS**

Replace the contents of `assets/css/fast-review.css` (currently just the header comment from Task 2) with:

```css
/* Fast-review (⚡ Ôn nhanh) — start/session/result screens */
.review-intro, .review-empty, .review-result {
  background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius-lg);
  padding: 28px 22px; text-align: center; max-width: 420px; margin: 12px auto;
}
.review-intro-icon, .review-empty-icon, .review-result-icon { font-size: 44px; line-height: 1; margin-bottom: 10px; }
.review-intro-title, .review-empty-title, .review-result-title { font-size: 19px; font-weight: 700; margin-bottom: 12px; }
.review-empty-msg { font-size: 14px; color: var(--text-secondary); line-height: 1.5; }
.review-rules { text-align: left; margin: 0 0 20px; padding-left: 20px; color: var(--text-secondary); font-size: 14px; line-height: 1.7; }
.review-rules strong { color: var(--text-primary); }
.review-start-btn, .review-again-btn {
  background: var(--accent); color: #fff; border: none; border-radius: 999px;
  padding: 11px 28px; font-size: 14.5px; font-weight: 600; cursor: pointer;
}
.review-start-btn:hover, .review-again-btn:hover { opacity: 0.9; }
.review-back-btn {
  background: transparent; color: var(--text-secondary); border: 1px solid var(--border); border-radius: 999px;
  padding: 11px 28px; font-size: 14.5px; font-weight: 500; cursor: pointer;
}

.review-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.review-lives { font-size: 18px; letter-spacing: 2px; color: var(--danger-text); }
.review-progress-text { font-size: 13px; color: var(--text-secondary); }

.review-timer-track { height: 6px; background: var(--border); border-radius: 999px; overflow: hidden; margin-bottom: 18px; }
.review-timer-fill { height: 100%; background: var(--accent); width: 100%; transition: width 1s linear; }
.review-timer-fill.review-timer-low { background: var(--danger-solid); }

.review-question-word { text-align: center; margin-bottom: 22px; }
.review-hanzi { font-size: 48px; font-weight: 600; line-height: 1.2; }
.review-meaning { font-size: 15px; color: var(--text-secondary); margin-top: 4px; }

.review-answer-area { display: flex; gap: 8px; }
.review-type-input {
  flex: 1; padding: 11px 14px; font-size: 15px; border: 1px solid var(--border);
  border-radius: var(--radius-md); background: var(--bg); color: var(--text-primary);
}
.review-type-input:focus { outline: 2px solid var(--accent); outline-offset: 1px; }
.review-submit-btn {
  background: var(--accent); color: #fff; border: none; border-radius: var(--radius-md);
  padding: 0 18px; font-size: 14px; font-weight: 600; cursor: pointer;
}

.review-choices { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.review-choice-btn {
  padding: 14px 10px; font-size: 15px; border: 1px solid var(--border); border-radius: var(--radius-md);
  background: var(--card-bg); color: var(--text-primary); cursor: pointer;
}
.review-choice-btn:disabled { cursor: default; }
.review-choice-btn--correct { background: var(--success-bg); border-color: var(--success-text); color: var(--success-text); }

.review-feedback { min-height: 22px; text-align: center; margin-top: 14px; font-size: 14px; font-weight: 600; opacity: 0; }
.review-feedback.show { opacity: 1; }
.review-feedback--correct { color: var(--success-text); }
.review-feedback--wrong { color: var(--danger-text); }

.review-result-stats { display: flex; justify-content: center; gap: 24px; margin: 18px 0 24px; }
.review-result-num { font-size: 26px; font-weight: 700; color: var(--accent); }
.review-result-lbl { font-size: 12px; color: var(--text-secondary); margin-top: 2px; }
.review-result-actions { display: flex; gap: 10px; justify-content: center; }

@media (prefers-reduced-motion: reduce) {
  .review-timer-fill { transition: none; }
}
```

- [ ] **Step 3: Manually verify full flow end-to-end**

Run: serve the app, open a level, go to "⚡ Ôn nhanh", click "Bắt đầu". Play through:
- Answer a few correctly and a few incorrectly (mix of typed and multiple-choice questions) until either lives reach 0 or the pool is exhausted.
- Confirm the result screen shows correct/total/best-streak numbers that match what happened during play.
- Click "Chơi lại" — confirm it rebuilds the pool (words just marked `known` should no longer appear; words marked `unknown` should reappear) and returns to the start screen (not directly restarting), matching `renderReviewStart()`'s behavior.
- Click "Về flashcard" — confirm it switches to the flashcard tab via `setViewMode('cards')` and the previously-taken quiz's `known`/`unknown` marks are reflected in the flashcard tab's stat counts (`s-known`/`s-unknown`) and filter buttons.
- Switch to "📋 Tổng quan từ vựng" and back to confirm no layout break from the third tab.
- Resize to a narrow mobile width (or use devtools device toolbar) and confirm the choice grid and timer bar remain usable.
- Toggle dark mode (if the app has a theme toggle — confirm via `assets/js/theme.js`) and confirm all fast-review colors adapt (no hardcoded colors were used, only CSS custom properties, so this should pass by construction).

Expected: full session completes without console errors; progress updates are visible on the flashcard tab immediately after switching; dark mode renders correctly.

- [ ] **Step 4: Commit**

```bash
git add assets/js/fast-review.js assets/css/fast-review.css
git commit -m "feat: add fast-review result screen and full styling"
```

---

## Post-plan note

This plan intentionally has no automated test suite because the codebase has none (confirmed during planning: no `package.json`, no `*.test.js`, no CI config referencing JS tests). All verification steps are manual, in-browser, consistent with how every other feature in this codebase (history modal, radicals mode, vocabulary overview) has been built and verified per the git log.
