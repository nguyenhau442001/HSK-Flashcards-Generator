# Streak History Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make streak calculation single-source-of-truth, stop deleting study history, and add a history modal (GitHub-style binary heatmap + streak stats: current/longest/shortest/total days).

**Architecture:** All logic lives in `assets/js/levels.js` (where `studyStreak`/`recordDailyStudy` already live) — no new files for logic. New modal markup is injected via JS (`document.createElement`/`innerHTML`), following the exact pattern `showCelebration()` uses in `assets/js/progress.js`. New CSS file `assets/css/streak-history.css`, imported from `assets/flashcards.css` alongside the existing `celebration.css` import. No new localStorage keys, no timers, no build step — plain script tags, tested via a Node fake-DOM-free harness for the pure functions (`streakStats` has no DOM dependency) and manual browser verification for the modal.

**Tech Stack:** Vanilla JS, vanilla CSS, no bundler, no test framework (verify pure functions via a disposable Node script, verify UI via local HTTP server + browser).

## Global Constraints

- Day counts as "studied" if `days[dateKey]` is a non-empty array (existing format, e.g. `['hsk1:12', 'hsk1:13']`). Do not change this data shape.
- No session-time / hours tracking. Binary studied/not-studied only, per design spec `docs/superpowers/specs/2026-08-08-streak-history-design.md`.
- History must persist forever — remove the 120-day deletion in `recordDailyStudy`.
- Single streak source of truth: `studyStreak(days)` reading from `STUDY_ACTIVITY_KEY`. The welcome toast must not compute its own streak.
- `hsk_visit_history_v1` keeps only `lastVisit` and is used for greeting dedup — no `streak` field.
- Vietnamese UI copy, matching existing tone (see `learningStreak` / `dailyGoalMessage` text in `flashcards.html`).
- Follow existing code style: no semicolons omitted (file uses semicolons), 2-space indent, `const`/`let`, no frameworks.

---

### Task 1: `streakStats()` pure function + stop deleting old history

**Files:**
- Modify: `assets/js/levels.js:98-101` (delete 120-day cleanup block inside `recordDailyStudy`)
- Modify: `assets/js/levels.js` (add `streakStats` function near `studyStreak`, after line 87)
- Test: disposable Node script (not committed) run via `node`, following the verification approach used for the prior radical-overview fix — write assertions, run, delete script after passing

**Interfaces:**
- Consumes: `localDateKey(date)` (existing, `levels.js:2`), `calendarDayDifference(fromKey, toKey)` (existing, `levels.js:9`), `studyStreak(days)` (existing, `levels.js:70`).
- Produces: `streakStats(days)` → `{ current: number, longest: number, shortest: number, totalDaysStudied: number }`. Later tasks (modal rendering) call this exact signature.

- [ ] **Step 1: Remove the 120-day deletion in `recordDailyStudy`**

Current code at `assets/js/levels.js:98-101`:

```js
  Object.keys(activity.days).forEach(dateKey => {
    const age = calendarDayDifference(dateKey, today);
    if (age === null || age < 0 || age > 120) delete activity.days[dateKey];
  });
```

Delete this block entirely. `recordDailyStudy` becomes:

```js
function recordDailyStudy(wordId) {
  if (!currentLevel || wordId === undefined || wordId === null) return;

  const activity = readStudyActivity();
  const today = localDateKey(new Date());
  const learnedWords = new Set(Array.isArray(activity.days[today]) ? activity.days[today] : []);
  learnedWords.add(currentLevel + ':' + String(wordId));
  activity.days[today] = Array.from(learnedWords);

  try { localStorage.setItem(STUDY_ACTIVITY_KEY, JSON.stringify(activity)); } catch (e) {}
  renderLearningDashboard();
}
```

- [ ] **Step 2: Add `streakStats` function**

Insert immediately after `studyStreak` (after `assets/js/levels.js:87`):

```js
function streakStats(days) {
  const studiedKeys = Object.keys(days)
    .filter(key => Array.isArray(days[key]) && days[key].length > 0)
    .sort();

  if (studiedKeys.length === 0) {
    return { current: 0, longest: 0, shortest: 0, totalDaysStudied: 0 };
  }

  const runs = [];
  let runLength = 1;
  for (let i = 1; i < studiedKeys.length; i++) {
    const gap = calendarDayDifference(studiedKeys[i - 1], studiedKeys[i]);
    if (gap === 1) {
      runLength++;
    } else {
      runs.push(runLength);
      runLength = 1;
    }
  }
  runs.push(runLength);

  const current = studyStreak(days);
  const completedRuns = current > 0 ? runs.slice(0, -1) : runs.slice();
  const shortestSource = completedRuns.length > 0 ? completedRuns : runs;

  return {
    current,
    longest: Math.max(...runs),
    shortest: Math.min(...shortestSource),
    totalDaysStudied: studiedKeys.length,
  };
}
```

- [ ] **Step 3: Verify with a disposable Node script**

Create `/tmp/streak-stats-test.js` (do not commit):

```js
const fs = require('fs');
const path = require('path');
const src = fs.readFileSync(path.join(__dirname, '../Users/haunguyen/GitHub/HSK-Flashcards-Generator/assets/js/levels.js'), 'utf8');

// Extract just localDateKey, calendarDayDifference, studyStreak, streakStats via eval in isolated scope
const sandbox = {};
new Function('exports', src + '\nexports.localDateKey=localDateKey;exports.calendarDayDifference=calendarDayDifference;exports.studyStreak=studyStreak;exports.streakStats=streakStats;')(sandbox);

function assertEqual(actual, expected, label) {
  const a = JSON.stringify(actual), e = JSON.stringify(expected);
  if (a !== e) { console.error(`FAIL ${label}: got ${a}, want ${e}`); process.exitCode = 1; }
  else console.log(`PASS ${label}`);
}

const { localDateKey, streakStats } = sandbox;

// Empty
assertEqual(streakStats({}), { current: 0, longest: 0, shortest: 0, totalDaysStudied: 0 }, 'empty');

// Single day studied = today
const today = localDateKey(new Date());
assertEqual(streakStats({ [today]: ['a'] }), { current: 1, longest: 1, shortest: 1, totalDaysStudied: 1 }, 'single day');

// Two runs with a gap: studied 5 days ago and 4 days ago (run of 2, broken), then today (run of 1, current)
const d = n => { const c = new Date(); c.setDate(c.getDate() - n); return localDateKey(c); };
const days = { [d(5)]: ['a'], [d(4)]: ['a'], [today]: ['a'] };
assertEqual(streakStats(days), { current: 1, longest: 2, shortest: 1, totalDaysStudied: 3 }, 'two runs, current broken vs longest');

// Current streak continues: today + yesterday, single run
const days2 = { [d(1)]: ['a'], [today]: ['a'] };
assertEqual(streakStats(days2), { current: 2, longest: 2, shortest: 2, totalDaysStudied: 2 }, 'single in-progress run');
```

Run: `node /tmp/streak-stats-test.js`
Expected: all 4 lines print `PASS`.

- [ ] **Step 4: Delete the disposable test script**

```bash
rm /tmp/streak-stats-test.js
```

- [ ] **Step 5: Commit**

```bash
git add assets/js/levels.js
git commit -m "fix: stop deleting old study history, add streakStats helper"
```

---

### Task 2: Single-source streak in welcome toast

**Files:**
- Modify: `assets/js/levels.js:201-278` (`showWelcomeToast`)

**Interfaces:**
- Consumes: `readStudyActivity()` (existing, `levels.js:44`), `studyStreak(days)` (existing, `levels.js:70`).
- Produces: `showWelcomeToast` no longer writes a `streak` field into `hsk_visit_history_v1`. Task 3/4 (modal) do not depend on this task's internals, only on `streakStats`/`studyStreak` from Task 1.

- [ ] **Step 1: Replace the local streak computation**

In `showWelcomeToast` (`assets/js/levels.js:201-278`), the current block:

```js
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
```

becomes:

```js
  let greeting;
  const firstVisit = !history || !history.lastVisit;
  const streak = studyStreak(readStudyActivity().days);

  if (firstVisit) {
    greeting = 'Chào mừng bạn! Chọn một cấp độ rồi mình chiến thôi 👋';
  } else {
    const dayDifference = calendarDayDifference(history.lastVisit, today);
    const continuedStreak = dayDifference === 1;

    const contextualGreetings = [];
```

(The `contextualGreetings.push(...)` line using `continuedStreak && streak >= 2` below stays unchanged — it already reads the outer `streak` variable, now sourced from `studyStreak`.)

- [ ] **Step 2: Stop persisting `streak` into `hsk_visit_history_v1`**

Current code near the end of `showWelcomeToast`:

```js
  try {
    localStorage.setItem('hsk_visit_history_v1', JSON.stringify({ lastVisit: today, streak }));
    localStorage.setItem('hsk_last_greeting_v1', greeting);
  } catch (e) {}
```

becomes:

```js
  try {
    localStorage.setItem('hsk_visit_history_v1', JSON.stringify({ lastVisit: today }));
    localStorage.setItem('hsk_last_greeting_v1', greeting);
  } catch (e) {}
```

- [ ] **Step 3: Manual verification**

Run a local server and load the app twice on different simulated dates isn't practical manually — instead verify statically:
1. `grep -n "history.streak" assets/js/levels.js` → expect no matches.
2. `grep -n "let streak = studyStreak" assets/js/levels.js` → expect one match inside `showWelcomeToast`.

- [ ] **Step 4: Commit**

```bash
git add assets/js/levels.js
git commit -m "fix: welcome toast streak now sourced from study activity, not visit count"
```

---

### Task 3: History modal CSS

**Files:**
- Create: `assets/css/streak-history.css`
- Modify: `assets/flashcards.css:9` (add `@import url("css/streak-history.css");` after the `celebration.css` import)

**Interfaces:**
- Consumes: existing CSS custom properties `--card-bg`, `--border`, `--radius-lg`, `--text-secondary`, `--accent`, `--success-bg`, `--success-text` (used throughout `level-picker.css`/`celebration.css` — confirm exact names via `grep -n "^:root\|--card-bg\|--success-bg" assets/css/base.css` before writing values that don't exist).
- Produces: class names `.history-overlay`, `.history-box`, `.history-close`, `.history-stats`, `.history-stat`, `.history-heatmap`, `.history-heatmap-grid`, `.history-cell`, `.history-cell.studied`, `.history-cell-tooltip`. Task 4 (JS) generates markup using exactly these class names.

- [ ] **Step 1: Confirm available CSS custom properties**

```bash
grep -n "^\s*--" assets/css/base.css
```

Use only property names that exist in that output when writing the CSS below (substitute if names differ from what's assumed here).

- [ ] **Step 2: Write `assets/css/streak-history.css`**

```css
/* History modal: streak stats + contribution heatmap */
.history-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.48);
  display: flex; align-items: center; justify-content: center;
  z-index: 200; overflow: auto; padding: 24px 12px;
}
.history-box {
  background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius-lg);
  padding: 24px; max-width: 640px; width: 100%; position: relative;
}
.history-close {
  position: absolute; top: 14px; right: 14px;
  background: none; border: none; font-size: 20px; line-height: 1;
  cursor: pointer; color: var(--text-secondary);
}
.history-close:hover { opacity: 0.7; }
.history-title { font-size: 18px; font-weight: 700; margin: 0 0 16px; padding-right: 28px; }
.history-stats {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
  gap: 10px; margin-bottom: 20px;
}
.history-stat {
  background: var(--success-bg); border-radius: 10px; padding: 10px 12px; text-align: center;
}
.history-stat strong { display: block; font-size: 20px; color: var(--success-text); }
.history-stat span { font-size: 11.5px; color: var(--text-secondary); }
.history-heatmap { overflow-x: auto; }
.history-heatmap-grid {
  display: grid; grid-auto-flow: column; grid-template-rows: repeat(7, 12px);
  gap: 3px; width: max-content;
}
.history-cell {
  width: 12px; height: 12px; border-radius: 3px;
  background: var(--border); position: relative;
}
.history-cell.studied { background: var(--accent); }
.history-cell.empty { background: transparent; }
.history-cell:hover .history-cell-tooltip { display: block; }
.history-cell-tooltip {
  display: none; position: absolute; bottom: 130%; left: 50%; transform: translateX(-50%);
  background: var(--card-bg); border: 1px solid var(--border); border-radius: 6px;
  padding: 4px 8px; font-size: 11px; white-space: nowrap; z-index: 1; color: var(--text-secondary);
}
@media (prefers-reduced-motion: reduce) {
  .history-overlay { animation: none; }
}
```

- [ ] **Step 3: Wire the import**

In `assets/flashcards.css`, after line 8 (`@import url("css/celebration.css");`), add:

```css
@import url("css/streak-history.css");
```

- [ ] **Step 4: Manual verification**

```bash
grep -n "streak-history.css" assets/flashcards.css
```
Expected: one match.

- [ ] **Step 5: Commit**

```bash
git add assets/css/streak-history.css assets/flashcards.css
git commit -m "feat: add history modal styles"
```

---

### Task 4: History modal JS + dashboard trigger button

**Files:**
- Modify: `assets/js/levels.js` (add `showHistoryModal`, `buildHeatmapCells` functions, after `streakStats`)
- Modify: `flashcards.html:33` (add trigger button next to `learningStreak`)

**Interfaces:**
- Consumes: `streakStats(days)` and `readStudyActivity()` (Task 1), `localDateKey(date)` (existing).
- Produces: `showHistoryModal()` — global function called from an `onclick` in `flashcards.html`, following the same convention as `quickStartLearning()` (`flashcards.html:57`, `onclick="quickStartLearning()"`).

- [ ] **Step 1: Add the trigger button in `flashcards.html`**

Current (`flashcards.html:33`):

```html
      <div class="learning-streak" id="learningStreak">Bắt đầu chuỗi học</div>
```

becomes:

```html
      <div class="learning-dashboard-header-right">
        <div class="learning-streak" id="learningStreak">Bắt đầu chuỗi học</div>
        <button class="history-trigger" type="button" onclick="showHistoryModal()">Xem lịch sử 📊</button>
      </div>
```

- [ ] **Step 2: Add minimal layout CSS for the new wrapper**

In `assets/css/streak-history.css`, append:

```css
.learning-dashboard-header-right { display: flex; flex-direction: column; align-items: flex-end; gap: 6px; }
.history-trigger {
  background: none; border: 1px solid var(--border); border-radius: 999px;
  padding: 4px 10px; font-size: 11.5px; color: var(--text-secondary); cursor: pointer;
}
.history-trigger:hover { opacity: 0.8; }
```

- [ ] **Step 3: Add `buildHeatmapCells` and `showHistoryModal` to `assets/js/levels.js`**

Insert after `streakStats` (end of Task 1's addition):

```js
function buildHeatmapCells(days, weeksBack) {
  const cursor = new Date();
  cursor.setHours(12, 0, 0, 0);
  const todayDow = cursor.getDay();
  cursor.setDate(cursor.getDate() - todayDow);
  cursor.setDate(cursor.getDate() + 7 - (weeksBack * 7));

  const cells = [];
  for (let i = 0; i < weeksBack * 7; i++) {
    const key = localDateKey(cursor);
    const count = Array.isArray(days[key]) ? days[key].length : 0;
    cells.push({ dateKey: key, count, studied: count > 0, future: cursor > new Date() });
    cursor.setDate(cursor.getDate() + 1);
  }
  return cells;
}

function showHistoryModal() {
  const activity = readStudyActivity();
  const stats = streakStats(activity.days);
  const cells = buildHeatmapCells(activity.days, 52);

  const overlay = document.createElement('div');
  overlay.id = 'historyOverlay';
  overlay.className = 'history-overlay';
  overlay.innerHTML = `
    <div class="history-box">
      <button class="history-close" onclick="document.getElementById('historyOverlay').remove()" aria-label="Đóng">✕</button>
      <div class="history-title">Lịch sử học tập</div>
      <div class="history-stats">
        <div class="history-stat"><strong>${stats.current}</strong><span>Chuỗi hiện tại</span></div>
        <div class="history-stat"><strong>${stats.longest}</strong><span>Chuỗi dài nhất</span></div>
        <div class="history-stat"><strong>${stats.shortest}</strong><span>Chuỗi ngắn nhất</span></div>
        <div class="history-stat"><strong>${stats.totalDaysStudied}</strong><span>Tổng ngày đã học</span></div>
      </div>
      <div class="history-heatmap">
        <div class="history-heatmap-grid">
          ${cells.map(cell => `
            <div class="history-cell ${cell.future ? 'empty' : cell.studied ? 'studied' : ''}">
              ${cell.future ? '' : `<div class="history-cell-tooltip">${cell.dateKey}: ${cell.count} từ</div>`}
            </div>
          `).join('')}
        </div>
      </div>
    </div>`;
  overlay.addEventListener('click', e => { if (e.target === overlay) overlay.remove(); });
  document.body.appendChild(overlay);
}
```

- [ ] **Step 4: Manual verification**

```bash
cd /Users/haunguyen/GitHub/HSK-Flashcards-Generator && python3 -m http.server 8934 &>/dev/null &
sleep 1
curl -s http://localhost:8934/flashcards.html | grep -c "showHistoryModal"
kill %1
```
Expected: output `1` or more (button present in HTML).

Then verify interactively:
1. Open `http://localhost:8934/flashcards.html` in a browser.
2. Click "Xem lịch sử 📊".
3. Confirm modal opens showing 4 stat tiles and a heatmap grid.
4. Click outside the box → modal closes.
5. Click ✕ → modal closes.
6. Hover a studied (colored) cell → tooltip shows date + word count.

- [ ] **Step 5: Commit**

```bash
git add assets/js/levels.js assets/css/streak-history.css flashcards.html
git commit -m "feat: add study history modal with heatmap and streak stats"
```

---

### Task 5: End-to-end verification against the spec

**Files:** none (verification only)

- [ ] **Step 1: Confirm single source of truth**

```bash
grep -n "history.streak\|\.streak =" assets/js/levels.js
```
Expected: no leftover reads of a `streak` field from `hsk_visit_history_v1`.

- [ ] **Step 2: Confirm history is never deleted**

```bash
grep -n "age > 120\|delete activity.days" assets/js/levels.js
```
Expected: no matches.

- [ ] **Step 3: Manual scenario walkthrough**

Using browser devtools console on the running local server:
1. Seed fake history:
```js
localStorage.setItem('hsk_study_activity_v1', JSON.stringify({
  days: {
    '2026-08-03': ['hsk1:1'],
    '2026-08-04': ['hsk1:2'],
    '2026-08-06': ['hsk1:3'],
    '2026-08-07': ['hsk1:4'],
  }
}));
location.reload();
```
2. Open history modal, confirm: Aug 3–4 shown as studied (run of 2, broken by Aug 5 gap), Aug 6–7 studied (run of 2). If "today" in the browser is Aug 8, current streak should be 0 (no entry Aug 8), longest/shortest both 2.
3. Clear seeded data: `localStorage.removeItem('hsk_study_activity_v1'); location.reload();`

- [ ] **Step 4: Final commit if any fixes were needed during verification**

Only if Step 3 revealed a bug — fix, re-verify, then:
```bash
git add -A
git commit -m "fix: address issues found in streak history verification"
```
