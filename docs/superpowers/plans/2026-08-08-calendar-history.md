# Calendar-based Learning History Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the "Lịch sử học tập" modal's bar-chart visualization with a calendar-grid heatmap (month view + year view), a compact 4-card KPI header, and a polished modal shell — without touching any localStorage schema or streak-calculation logic.

**Architecture:** Pure client-side vanilla JS/CSS/HTML, no build step, no framework. All logic lives in `assets/js/levels.js` (global functions, `onclick=` wiring from injected HTML strings, same pattern as the rest of the file). Styling lives in `assets/css/streak-history.css`, using existing CSS custom properties for theming. Verification is done via Node-run sandbox scripts (no test framework in this repo) plus manual browser checks.

**Tech Stack:** Vanilla JavaScript (ES2017+), CSS custom properties, static HTML — no dependencies added.

## Global Constraints

- No changes to `hsk_study_activity_v1` schema or any other localStorage key.
- `studyStreak()` and `streakStats()` logic must not change (only what's rendered from their output may change).
- No new npm/JS dependencies.
- Support desktop and mobile; keep existing dark/light theme system (`--accent`, `--card-bg`, `--border`, etc. from `assets/css/base.css`).
- Month header text: `‹  Tháng {N} · {year}  ›` — Vietnamese only, no Hán month name.
- Vietnamese weekday header: `T2 T3 T4 T5 T6 T7 CN` (Monday-first).
- Legend: `Ít  □ ▨ ▧ ▦ ■  Nhiều`.
- No gradients, no heavy glassmorphism.

---

## File Structure

- **Modify `assets/js/levels.js`**: remove bar-chart-specific functions and state; add grid-building, formatting, and view-state functions; rewrite `renderHistoryModalBody()`.
- **Modify `assets/css/streak-history.css`**: remove bar-chart styles; add KPI card, segmented control, month-grid, year-grid, and modal-shell styles.
- **Modify `flashcards.html`**: none expected structurally — modal body is fully injected by JS — but verified in Task 6.
- No new files.

---

### Task 1: Duration formatting helper

**Files:**
- Modify: `assets/js/levels.js` (add near other small helpers, e.g. after `daySeconds()` at line 65)
- Test: sandbox script run via `node`, not committed

**Interfaces:**
- Produces: `formatStudyDuration(totalMinutes: number): string` — e.g. `formatStudyDuration(0) === '0 phút'`, `formatStudyDuration(45) === '45 phút'`, `formatStudyDuration(272) === '4 giờ 32 phút'`, `formatStudyDuration(120) === '2 giờ'` (omit "0 phút" suffix when remainder is 0).

- [ ] **Step 1: Write the sandbox test script**

Create `/tmp/test-format-duration.js`:

```js
function formatStudyDuration(totalMinutes) {
  const minutes = Math.round(totalMinutes);
  if (minutes <= 0) return '0 phút';
  const hours = Math.floor(minutes / 60);
  const remainder = minutes % 60;
  if (hours === 0) return `${remainder} phút`;
  if (remainder === 0) return `${hours} giờ`;
  return `${hours} giờ ${remainder} phút`;
}

const cases = [
  [0, '0 phút'],
  [45, '45 phút'],
  [272, '4 giờ 32 phút'],
  [120, '2 giờ'],
  [59, '59 phút'],
  [60, '1 giờ'],
  [61, '1 giờ 1 phút'],
];

let failed = 0;
for (const [input, expected] of cases) {
  const actual = formatStudyDuration(input);
  if (actual !== expected) {
    console.log(`FAIL formatStudyDuration(${input}) = "${actual}", expected "${expected}"`);
    failed++;
  }
}
console.log(failed === 0 ? 'ALL PASS' : `${failed} FAILED`);
```

- [ ] **Step 2: Run it to verify the logic**

Run: `node /tmp/test-format-duration.js`
Expected: `ALL PASS`

- [ ] **Step 3: Add the function to `assets/js/levels.js`**

Insert after `daySeconds()` (currently ends at line 65):

```js
function formatStudyDuration(totalMinutes) {
  const minutes = Math.round(totalMinutes);
  if (minutes <= 0) return '0 phút';
  const hours = Math.floor(minutes / 60);
  const remainder = minutes % 60;
  if (hours === 0) return `${remainder} phút`;
  if (remainder === 0) return `${hours} giờ`;
  return `${hours} giờ ${remainder} phút`;
}
```

- [ ] **Step 4: Verify no syntax errors**

Run: `node --check assets/js/levels.js`
Expected: no output (exit code 0)

- [ ] **Step 5: Commit**

```bash
git add assets/js/levels.js
git commit -m "feat: add formatStudyDuration helper for calendar history redesign"
```

---

### Task 2: Month grid builder + intensity bucketing

**Files:**
- Modify: `assets/js/levels.js` (replace `buildMonthBars()` / `monthAverageMinutes()` at lines 142-160 with new functions)
- Test: sandbox script run via `node`

**Interfaces:**
- Consumes: `daySeconds(dayEntry)` (existing, from `levels.js:63-65`), `localDateKey(date)` (existing, from `levels.js:2-7`)
- Produces:
  - `intensityBucket(minutes: number): 0|1|2|3|4` — 0 phút→0, 1–10→1, 11–30→2, 31–60→3, >60→4
  - `buildMonthGrid(days: object, year: number, month: number): Array<{dateKey: string|null, day: number|null, minutes: number, bucket: number, isToday: boolean, isFuture: boolean, inMonth: boolean}>` — flat array of exactly `N * 7` cells (N = number of Monday-first week rows needed to cover the month, i.e. 5 or 6), Monday-first order, padding cells have `inMonth: false, dateKey: null, day: null, minutes: 0, bucket: 0, isToday: false, isFuture: false`.

- [ ] **Step 1: Write the sandbox test script**

Create `/tmp/test-month-grid.js`:

```js
function intensityBucket(minutes) {
  if (minutes <= 0) return 0;
  if (minutes <= 10) return 1;
  if (minutes <= 30) return 2;
  if (minutes <= 60) return 3;
  return 4;
}

function localDateKey(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function daySeconds(dayEntry) {
  return dayEntry && typeof dayEntry.seconds === 'number' ? dayEntry.seconds : 0;
}

// Monday-first weekday index: JS getDay() is Sun=0..Sat=6, we want Mon=0..Sun=6
function mondayFirstIndex(jsDay) {
  return (jsDay + 6) % 7;
}

function buildMonthGrid(days, year, month) {
  const now = new Date();
  now.setHours(0, 0, 0, 0);
  const todayKey = localDateKey(now);

  const firstOfMonth = new Date(year, month, 1);
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const leadingBlanks = mondayFirstIndex(firstOfMonth.getDay());

  const cells = [];
  for (let i = 0; i < leadingBlanks; i++) {
    cells.push({ dateKey: null, day: null, minutes: 0, bucket: 0, isToday: false, isFuture: false, inMonth: false });
  }
  for (let d = 1; d <= daysInMonth; d++) {
    const date = new Date(year, month, d, 12, 0, 0, 0);
    const key = localDateKey(date);
    const minutes = daySeconds(days[key]) / 60;
    const dateOnly = new Date(year, month, d);
    dateOnly.setHours(0, 0, 0, 0);
    cells.push({
      dateKey: key,
      day: d,
      minutes,
      bucket: intensityBucket(minutes),
      isToday: key === todayKey,
      isFuture: dateOnly > now,
      inMonth: true,
    });
  }
  while (cells.length % 7 !== 0) {
    cells.push({ dateKey: null, day: null, minutes: 0, bucket: 0, isToday: false, isFuture: false, inMonth: false });
  }
  return cells;
}

// Test: intensityBucket boundaries
const bucketCases = [
  [0, 0], [1, 1], [10, 1], [10.5, 2], [11, 2], [30, 2], [31, 3], [60, 3], [61, 4], [999, 4],
];
let failed = 0;
for (const [input, expected] of bucketCases) {
  const actual = intensityBucket(input);
  if (actual !== expected) {
    console.log(`FAIL intensityBucket(${input}) = ${actual}, expected ${expected}`);
    failed++;
  }
}

// Test: buildMonthGrid for August 2026 (starts on a Saturday -> 5 leading blanks Mon-first)
// Aug 1 2026 is a Saturday (getDay()=6), mondayFirstIndex(6) = 5
const grid = buildMonthGrid({ '2026-08-08': { seconds: 24 * 60 } }, 2026, 7);
if (grid.length % 7 !== 0) { console.log(`FAIL grid length ${grid.length} not multiple of 7`); failed++; }
const leadingBlankCount = grid.findIndex(c => c.inMonth);
if (leadingBlankCount !== 5) { console.log(`FAIL expected 5 leading blanks for Aug 2026, got ${leadingBlankCount}`); failed++; }
const aug8 = grid.find(c => c.dateKey === '2026-08-08');
if (!aug8 || aug8.minutes !== 24 || aug8.bucket !== 2) { console.log(`FAIL Aug 8 cell wrong:`, aug8); failed++; }
const daysInMonthCount = grid.filter(c => c.inMonth).length;
if (daysInMonthCount !== 31) { console.log(`FAIL expected 31 in-month cells, got ${daysInMonthCount}`); failed++; }

// Test: empty month (no data) — all in-month cells bucket 0
const emptyGrid = buildMonthGrid({}, 2026, 5); // June 2026
const nonZeroBuckets = emptyGrid.filter(c => c.inMonth && c.bucket !== 0);
if (nonZeroBuckets.length !== 0) { console.log(`FAIL empty month has non-zero buckets`); failed++; }

console.log(failed === 0 ? 'ALL PASS' : `${failed} FAILED`);
```

- [ ] **Step 2: Run it to verify the logic**

Run: `node /tmp/test-month-grid.js`
Expected: `ALL PASS`

- [ ] **Step 3: Remove old bar-chart functions and add new ones in `assets/js/levels.js`**

Replace lines 138-160 (the `MONTH_LABELS` const through `monthAverageMinutes()`) with:

```js
function intensityBucket(minutes) {
  if (minutes <= 0) return 0;
  if (minutes <= 10) return 1;
  if (minutes <= 30) return 2;
  if (minutes <= 60) return 3;
  return 4;
}

function mondayFirstIndex(jsDay) {
  return (jsDay + 6) % 7;
}

function buildMonthGrid(days, year, month) {
  const now = new Date();
  now.setHours(0, 0, 0, 0);
  const todayKey = localDateKey(now);

  const firstOfMonth = new Date(year, month, 1);
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const leadingBlanks = mondayFirstIndex(firstOfMonth.getDay());

  const cells = [];
  for (let i = 0; i < leadingBlanks; i++) {
    cells.push({ dateKey: null, day: null, minutes: 0, bucket: 0, isToday: false, isFuture: false, inMonth: false });
  }
  for (let d = 1; d <= daysInMonth; d++) {
    const date = new Date(year, month, d, 12, 0, 0, 0);
    const key = localDateKey(date);
    const minutes = daySeconds(days[key]) / 60;
    const dateOnly = new Date(year, month, d);
    dateOnly.setHours(0, 0, 0, 0);
    cells.push({
      dateKey: key,
      day: d,
      minutes,
      bucket: intensityBucket(minutes),
      isToday: key === todayKey,
      isFuture: dateOnly > now,
      inMonth: true,
    });
  }
  while (cells.length % 7 !== 0) {
    cells.push({ dateKey: null, day: null, minutes: 0, bucket: 0, isToday: false, isFuture: false, inMonth: false });
  }
  return cells;
}
```

Note: `historyModalMonth` (old state var, currently at line 140) is removed here too — it's replaced in Task 4.

- [ ] **Step 4: Verify no syntax errors**

Run: `node --check assets/js/levels.js`
Expected: no output. Note this will still reference now-removed `historyModalMonth`/`MONTH_LABELS` from other functions until Task 4/5 — that's expected; full-file validation happens at the end of Task 5.

- [ ] **Step 5: Commit**

```bash
git add assets/js/levels.js
git commit -m "feat: replace bar-chart data builder with month grid + intensity bucketing"
```

---

### Task 3: Year data aggregation helper

**Files:**
- Modify: `assets/js/levels.js` (add new function near `buildMonthGrid`)
- Test: sandbox script run via `node`

**Interfaces:**
- Consumes: `daySeconds(dayEntry)`, `dayWordCount(dayEntry)` (existing)
- Produces: `yearSummary(days: object, year: number): { studiedDays: number, totalMinutes: number }` — counts distinct studied days (word count > 0) and sums minutes across all 12 months of the given year.

- [ ] **Step 1: Write the sandbox test script**

Create `/tmp/test-year-summary.js`:

```js
function dayWordCount(dayEntry) {
  return dayEntry && Array.isArray(dayEntry.words) ? dayEntry.words.length : 0;
}
function daySeconds(dayEntry) {
  return dayEntry && typeof dayEntry.seconds === 'number' ? dayEntry.seconds : 0;
}

function yearSummary(days, year) {
  let studiedDays = 0;
  let totalMinutes = 0;
  Object.keys(days).forEach(key => {
    if (!key.startsWith(String(year) + '-')) return;
    const entry = days[key];
    if (dayWordCount(entry) > 0) studiedDays++;
    totalMinutes += daySeconds(entry) / 60;
  });
  return { studiedDays, totalMinutes };
}

const days = {
  '2026-01-05': { words: ['a', 'b'], seconds: 600 },
  '2026-08-08': { words: ['c'], seconds: 1440 },
  '2025-12-31': { words: ['d'], seconds: 300 },
  '2026-03-01': { words: [], seconds: 120 },
};

const result = yearSummary(days, 2026);
let failed = 0;
if (result.studiedDays !== 2) { console.log(`FAIL studiedDays = ${result.studiedDays}, expected 2`); failed++; }
if (Math.round(result.totalMinutes) !== 36) { console.log(`FAIL totalMinutes = ${result.totalMinutes}, expected 36`); failed++; }

const emptyResult = yearSummary({}, 2026);
if (emptyResult.studiedDays !== 0 || emptyResult.totalMinutes !== 0) { console.log('FAIL empty year result wrong'); failed++; }

console.log(failed === 0 ? 'ALL PASS' : `${failed} FAILED`);
```

- [ ] **Step 2: Run it to verify the logic**

Run: `node /tmp/test-year-summary.js`
Expected: `ALL PASS`

- [ ] **Step 3: Add the function to `assets/js/levels.js`**

Insert directly after `buildMonthGrid()`:

```js
function yearSummary(days, year) {
  let studiedDays = 0;
  let totalMinutes = 0;
  Object.keys(days).forEach(key => {
    if (!key.startsWith(String(year) + '-')) return;
    const entry = days[key];
    if (dayWordCount(entry) > 0) studiedDays++;
    totalMinutes += daySeconds(entry) / 60;
  });
  return { studiedDays, totalMinutes };
}
```

- [ ] **Step 4: Verify no syntax errors**

Run: `node --check assets/js/levels.js`
Expected: no output

- [ ] **Step 5: Commit**

```bash
git add assets/js/levels.js
git commit -m "feat: add yearSummary aggregation helper"
```

---

### Task 4: View state + navigation functions

**Files:**
- Modify: `assets/js/levels.js` (replace `changeHistoryModalMonth()` at lines 162-168, update `showHistoryModal()` at lines 218-234)

**Interfaces:**
- Consumes: `renderHistoryModalBody()` (rewritten in Task 5, but signature stays `renderHistoryModalBody(): void`)
- Produces:
  - `let historyModalView` (module state, `'month'` or `'year'`)
  - `let historyModalCursor` (module state, `{ year: number, month: number }`)
  - `setHistoryView(view: 'month'|'year'): void`
  - `changeHistoryCursor(delta: number): void` — moves month by `delta` when `historyModalView === 'month'`, moves year by `delta` when `'year'`; both clamp so navigating past the current real month/year is a no-op
  - `jumpToMonth(year: number, month: number): void` — sets `historyModalView = 'month'`, sets cursor, re-renders

- [ ] **Step 1: Replace `historyModalMonth` declaration and `changeHistoryModalMonth()`**

The `let historyModalMonth = null;` line was already removed as part of Task 2's replacement block. Now replace the old `changeHistoryModalMonth()` function (originally at lines 162-168) with:

```js
let historyModalView = 'month';
let historyModalCursor = { year: 0, month: 0 };

function setHistoryView(view) {
  historyModalView = view;
  renderHistoryModalBody();
}

function changeHistoryCursor(delta) {
  const now = new Date();
  if (historyModalView === 'month') {
    const next = new Date(historyModalCursor.year, historyModalCursor.month + delta, 1);
    if (next.getFullYear() > now.getFullYear() || (next.getFullYear() === now.getFullYear() && next.getMonth() > now.getMonth())) return;
    historyModalCursor = { year: next.getFullYear(), month: next.getMonth() };
  } else {
    const nextYear = historyModalCursor.year + delta;
    if (nextYear > now.getFullYear()) return;
    historyModalCursor = { year: nextYear, month: historyModalCursor.month };
  }
  renderHistoryModalBody();
}

function jumpToMonth(year, month) {
  historyModalView = 'month';
  historyModalCursor = { year, month };
  renderHistoryModalBody();
}
```

- [ ] **Step 2: Update `showHistoryModal()` to initialize new state**

In `showHistoryModal()` (currently lines 218-234), replace:

```js
  const now = new Date();
  historyModalMonth = { year: now.getFullYear(), month: now.getMonth() };
```

with:

```js
  const now = new Date();
  historyModalView = 'month';
  historyModalCursor = { year: now.getFullYear(), month: now.getMonth() };
```

- [ ] **Step 3: Verify no syntax errors**

Run: `node --check assets/js/levels.js`
Expected: no output. `renderHistoryModalBody()` still references the old bar-chart markup at this point — that's fixed in Task 5 next, so a browser smoke test isn't meaningful until then.

- [ ] **Step 4: Commit**

```bash
git add assets/js/levels.js
git commit -m "feat: add month/year view-state navigation for history modal"
```

---

### Task 5: Rewrite modal body rendering (month view + year view + KPI header)

**Files:**
- Modify: `assets/js/levels.js` (rewrite `renderHistoryModalBody()`, currently lines 170-216)

**Interfaces:**
- Consumes: `streakStats(days)`, `readStudyActivity()`, `buildMonthGrid(days, year, month)`, `yearSummary(days, year)`, `formatStudyDuration(totalMinutes)`, `historyModalView`, `historyModalCursor`, `setHistoryView`, `changeHistoryCursor`, `jumpToMonth` (all from Tasks 1-4)
- Produces: `renderHistoryModalBody(): void` — same signature as before, called by `showHistoryModal()` and by the new nav/view functions

- [ ] **Step 1: Replace `renderHistoryModalBody()`**

Replace the entire function (lines 170-216 in the original file) with:

```js
const WEEKDAY_LABELS = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN'];

function renderMonthGridHtml(grid) {
  return `
    <div class="history-weekday-row">
      ${WEEKDAY_LABELS.map(label => `<div class="history-weekday">${label}</div>`).join('')}
    </div>
    <div class="history-month-grid">
      ${grid.map(cell => {
        if (!cell.inMonth) return '<div class="history-day-cell empty" aria-hidden="true"></div>';
        const [y, m, d] = cell.dateKey.split('-');
        const displayDate = `${d}/${m}/${y}`;
        const classes = ['history-day-cell', `bucket-${cell.bucket}`];
        if (cell.isToday) classes.push('today');
        if (cell.isFuture) classes.push('future');
        const title = cell.isFuture ? '' : `title="${displayDate}\nĐã học: ${Math.round(cell.minutes)} phút"`;
        return `<div class="${classes.join(' ')}" ${title}>${cell.day}</div>`;
      }).join('')}
    </div>`;
}

function renderMonthView(activity) {
  const { year, month } = historyModalCursor;
  const grid = buildMonthGrid(activity.days, year, month);
  const now = new Date();
  const isCurrentMonth = year === now.getFullYear() && month === now.getMonth();
  const studiedDays = grid.filter(c => c.inMonth && c.bucket > 0).length;
  const totalMinutes = grid.filter(c => c.inMonth).reduce((sum, c) => sum + c.minutes, 0);

  return `
    <div class="history-month-nav">
      <button class="history-month-btn" type="button" onclick="changeHistoryCursor(-1)" aria-label="Tháng trước">‹</button>
      <div class="history-month-title">Tháng ${month + 1} · ${year}</div>
      <button class="history-month-btn" type="button" onclick="changeHistoryCursor(1)" ${isCurrentMonth ? 'disabled' : ''} aria-label="Tháng sau">›</button>
    </div>
    ${renderMonthGridHtml(grid)}
    <div class="history-legend">
      <span>Ít</span>
      <span class="history-legend-swatch bucket-0"></span>
      <span class="history-legend-swatch bucket-1"></span>
      <span class="history-legend-swatch bucket-2"></span>
      <span class="history-legend-swatch bucket-3"></span>
      <span class="history-legend-swatch bucket-4"></span>
      <span>Nhiều</span>
    </div>
    <div class="history-summary">${studiedDays} ngày học · ${formatStudyDuration(totalMinutes)}</div>`;
}

const MINI_MONTH_LABELS = ['Th 1', 'Th 2', 'Th 3', 'Th 4', 'Th 5', 'Th 6', 'Th 7', 'Th 8', 'Th 9', 'Th 10', 'Th 11', 'Th 12'];

function renderYearView(activity) {
  const { year } = historyModalCursor;
  const now = new Date();
  const isCurrentYear = year === now.getFullYear();
  const summary = yearSummary(activity.days, year);

  const months = Array.from({ length: 12 }, (_, month) => {
    const grid = buildMonthGrid(activity.days, year, month);
    return `
      <div class="history-mini-month" role="button" tabindex="0"
        onclick="jumpToMonth(${year}, ${month})"
        onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();jumpToMonth(${year}, ${month});}">
        <div class="history-mini-month-label">${MINI_MONTH_LABELS[month]}</div>
        <div class="history-mini-grid">
          ${grid.map(cell => `<div class="history-mini-cell ${cell.inMonth ? 'bucket-' + cell.bucket : 'empty'} ${cell.isToday ? 'today' : ''}"></div>`).join('')}
        </div>
      </div>`;
  }).join('');

  return `
    <div class="history-month-nav">
      <button class="history-month-btn" type="button" onclick="changeHistoryCursor(-1)" aria-label="Năm trước">‹</button>
      <div class="history-month-title">${year}</div>
      <button class="history-month-btn" type="button" onclick="changeHistoryCursor(1)" ${isCurrentYear ? 'disabled' : ''} aria-label="Năm sau">›</button>
    </div>
    <div class="history-year-grid">${months}</div>
    <div class="history-summary">${summary.studiedDays} ngày học · ${formatStudyDuration(summary.totalMinutes)}</div>`;
}

function renderHistoryModalBody() {
  const body = document.getElementById('historyModalBody');
  if (!body) return;

  const activity = readStudyActivity();
  const stats = streakStats(activity.days);
  const totalMinutesAllTime = Object.values(activity.days).reduce((sum, entry) => sum + daySeconds(entry) / 60, 0);

  body.innerHTML = `
    <div class="history-kpi-row">
      <div class="history-kpi"><strong>🔥 ${stats.current}</strong><span>Chuỗi hiện tại</span></div>
      <div class="history-kpi"><strong>🏆 ${stats.longest}</strong><span>Chuỗi dài nhất</span></div>
      <div class="history-kpi"><strong>📅 ${stats.totalDaysStudied}</strong><span>Ngày đã học</span></div>
      <div class="history-kpi"><strong>⏱ ${formatStudyDuration(totalMinutesAllTime)}</strong><span>Tổng thời gian</span></div>
    </div>
    <div class="history-view-switcher" role="tablist">
      <button type="button" role="tab" class="history-view-btn ${historyModalView === 'month' ? 'active' : ''}" aria-selected="${historyModalView === 'month'}" onclick="setHistoryView('month')">Tháng</button>
      <button type="button" role="tab" class="history-view-btn ${historyModalView === 'year' ? 'active' : ''}" aria-selected="${historyModalView === 'year'}" onclick="setHistoryView('year')">Năm</button>
    </div>
    <div class="history-view-body">
      ${historyModalView === 'month' ? renderMonthView(activity) : renderYearView(activity)}
    </div>`;
}
```

Note: `⏱ ${formatStudyDuration(...)}` — the KPI numeral for the time card is a formatted string, not a raw number like the other three cards; the CSS in Task 7 must accommodate a longer string in that slot without breaking the compact layout.

- [ ] **Step 2: Verify no syntax errors**

Run: `node --check assets/js/levels.js`
Expected: no output

- [ ] **Step 3: Commit**

```bash
git add assets/js/levels.js
git commit -m "feat: rewrite history modal body with calendar heatmap month/year views"
```

---

### Task 6: Modal shell polish + Escape key handling

**Files:**
- Modify: `assets/js/levels.js` (update `showHistoryModal()`, lines 218-234 in the original file)

**Interfaces:**
- Consumes: `renderHistoryModalBody()` (Task 5)
- Produces: `showHistoryModal(): void` (same signature, adds Escape-to-close)

- [ ] **Step 1: Replace `showHistoryModal()`**

```js
function closeHistoryModal() {
  const overlay = document.getElementById('historyOverlay');
  if (overlay) overlay.remove();
  document.removeEventListener('keydown', handleHistoryModalKeydown);
}

function handleHistoryModalKeydown(e) {
  if (e.key === 'Escape') closeHistoryModal();
}

function showHistoryModal() {
  const now = new Date();
  historyModalView = 'month';
  historyModalCursor = { year: now.getFullYear(), month: now.getMonth() };

  const overlay = document.createElement('div');
  overlay.id = 'historyOverlay';
  overlay.className = 'history-overlay';
  overlay.innerHTML = `
    <div class="history-box" role="dialog" aria-modal="true" aria-label="Lịch sử học tập">
      <button class="history-close" onclick="closeHistoryModal()" aria-label="Đóng">✕</button>
      <div class="history-title">Lịch sử học tập</div>
      <div id="historyModalBody"></div>
    </div>`;
  overlay.addEventListener('click', e => { if (e.target === overlay) closeHistoryModal(); });
  document.body.appendChild(overlay);
  document.addEventListener('keydown', handleHistoryModalKeydown);
  renderHistoryModalBody();
}
```

- [ ] **Step 2: Verify no syntax errors**

Run: `node --check assets/js/levels.js`
Expected: no output

- [ ] **Step 3: Full-file review for stray references**

Run: `grep -n "historyModalMonth\|MONTH_LABELS\|buildMonthBars\|monthAverageMinutes\|changeHistoryModalMonth" assets/js/levels.js`
Expected: no matches (all old names fully removed)

- [ ] **Step 4: Commit**

```bash
git add assets/js/levels.js
git commit -m "feat: add Escape-to-close and dialog semantics to history modal"
```

---

### Task 7: CSS rewrite — KPI cards, segmented control, calendar grids, modal shell

**Files:**
- Modify: `assets/css/streak-history.css` (full rewrite of file contents, same file)

**Interfaces:**
- Consumes: CSS custom properties from `assets/css/base.css`: `--bg`, `--card-bg`, `--border`, `--text-primary`, `--text-secondary`, `--text-tertiary`, `--accent`, `--accent-light`, `--radius-lg`, `--radius-md`
- Produces: class selectors matching the HTML emitted in Task 5/6: `.history-overlay`, `.history-box`, `.history-close`, `.history-title`, `.history-kpi-row`, `.history-kpi`, `.history-view-switcher`, `.history-view-btn`, `.history-view-body`, `.history-month-nav`, `.history-month-btn`, `.history-month-title`, `.history-weekday-row`, `.history-weekday`, `.history-month-grid`, `.history-day-cell` (+ `.bucket-0..4`, `.today`, `.future`, `.empty`), `.history-legend`, `.history-legend-swatch`, `.history-summary`, `.history-year-grid`, `.history-mini-month`, `.history-mini-month-label`, `.history-mini-grid`, `.history-mini-cell`

- [ ] **Step 1: Write the full replacement CSS file**

```css
/* History modal: KPI header, view switcher, calendar heatmap (month + year) */
.learning-dashboard-header-right { display: flex; flex-direction: row; align-items: center; gap: 8px; }
.history-trigger {
  background: none; border: 1px solid var(--border); border-radius: 999px;
  padding: 4px 10px; font-size: 11.5px; color: var(--text-secondary); cursor: pointer;
}
.history-trigger:hover { opacity: 0.8; }
.history-trigger:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

.history-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.48);
  display: flex; align-items: center; justify-content: center;
  z-index: 200; overflow: auto; padding: 24px 12px;
}
.history-box {
  background: var(--card-bg); border: 1px solid var(--border); border-radius: 24px;
  padding: 32px; max-width: 900px; width: 100%; height: auto; position: relative;
}
.history-close {
  position: absolute; top: 16px; right: 16px;
  background: none; border: none; font-size: 20px; line-height: 1;
  cursor: pointer; color: var(--text-secondary); border-radius: 6px; padding: 4px;
}
.history-close:hover { opacity: 0.7; }
.history-close:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.history-title { font-size: 19px; font-weight: 700; margin: 0 0 20px; padding-right: 32px; }

/* KPI header */
.history-kpi-row {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 10px; margin-bottom: 20px;
}
.history-kpi {
  background: var(--bg); border: 1px solid var(--border); border-radius: var(--radius-md);
  padding: 12px 14px; text-align: center;
}
.history-kpi strong { display: block; font-size: 19px; font-weight: 700; color: var(--text-primary); white-space: nowrap; }
.history-kpi span { font-size: 11px; color: var(--text-secondary); }

/* Segmented view switcher */
.history-view-switcher {
  display: inline-flex; border: 1px solid var(--border); border-radius: 999px;
  padding: 3px; gap: 2px; margin-bottom: 18px;
}
.history-view-btn {
  background: none; border: none; border-radius: 999px; padding: 6px 16px;
  font-size: 13px; color: var(--text-secondary); cursor: pointer;
}
.history-view-btn.active { background: var(--accent); color: #fff; }
.history-view-btn:not(.active):hover { opacity: 0.7; }
.history-view-btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

/* Month/year nav */
.history-month-nav {
  display: flex; align-items: center; justify-content: center; gap: 14px; margin-bottom: 14px;
}
.history-month-btn {
  background: none; border: 1px solid var(--border); border-radius: 999px;
  width: 30px; height: 30px; font-size: 15px; color: var(--text-primary); cursor: pointer;
}
.history-month-btn:hover:not(:disabled) { opacity: 0.7; }
.history-month-btn:disabled { opacity: 0.3; cursor: not-allowed; }
.history-month-btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.history-month-title { font-size: 15px; font-weight: 600; min-width: 140px; text-align: center; }

/* Month view grid */
.history-weekday-row, .history-month-grid {
  display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px;
}
.history-weekday {
  font-size: 10.5px; color: var(--text-tertiary); text-align: center; padding-bottom: 4px;
}
.history-day-cell {
  aspect-ratio: 1; display: flex; align-items: center; justify-content: center;
  border-radius: 6px; font-size: 11px; color: var(--text-primary);
  border: 1px solid var(--border); background: transparent; cursor: default;
}
.history-day-cell.empty { border: none; background: transparent; }
.history-day-cell.bucket-1 { background: color-mix(in srgb, var(--accent) 15%, transparent); border-color: transparent; }
.history-day-cell.bucket-2 { background: color-mix(in srgb, var(--accent) 35%, transparent); border-color: transparent; }
.history-day-cell.bucket-3 { background: color-mix(in srgb, var(--accent) 60%, transparent); border-color: transparent; color: #fff; }
.history-day-cell.bucket-4 { background: var(--accent); border-color: transparent; color: #fff; }
.history-day-cell.today { border: 2px solid var(--accent); font-weight: 700; }
.history-day-cell.future { opacity: 0.35; }

/* Legend + summary */
.history-legend {
  display: flex; align-items: center; justify-content: center; gap: 4px;
  margin-top: 14px; font-size: 10.5px; color: var(--text-tertiary);
}
.history-legend-swatch {
  width: 11px; height: 11px; border-radius: 3px; border: 1px solid var(--border);
  display: inline-block;
}
.history-legend-swatch.bucket-0 { background: transparent; }
.history-legend-swatch.bucket-1 { background: color-mix(in srgb, var(--accent) 15%, transparent); border-color: transparent; }
.history-legend-swatch.bucket-2 { background: color-mix(in srgb, var(--accent) 35%, transparent); border-color: transparent; }
.history-legend-swatch.bucket-3 { background: color-mix(in srgb, var(--accent) 60%, transparent); border-color: transparent; }
.history-legend-swatch.bucket-4 { background: var(--accent); border-color: transparent; }
.history-summary {
  text-align: center; font-size: 12.5px; color: var(--text-secondary); margin-top: 10px;
}

/* Year view */
.history-year-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;
}
.history-mini-month {
  border: 1px solid var(--border); border-radius: var(--radius-md); padding: 10px;
  cursor: pointer;
}
.history-mini-month:hover { border-color: var(--accent); }
.history-mini-month:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.history-mini-month-label { font-size: 11.5px; font-weight: 600; margin-bottom: 6px; text-align: center; }
.history-mini-grid {
  display: grid; grid-template-columns: repeat(7, 1fr); gap: 2px;
}
.history-mini-cell {
  aspect-ratio: 1; border-radius: 2px; background: transparent; border: 1px solid var(--border);
}
.history-mini-cell.empty { border: none; }
.history-mini-cell.bucket-1 { background: color-mix(in srgb, var(--accent) 15%, transparent); border-color: transparent; }
.history-mini-cell.bucket-2 { background: color-mix(in srgb, var(--accent) 35%, transparent); border-color: transparent; }
.history-mini-cell.bucket-3 { background: color-mix(in srgb, var(--accent) 60%, transparent); border-color: transparent; }
.history-mini-cell.bucket-4 { background: var(--accent); border-color: transparent; }
.history-mini-cell.today { outline: 1.5px solid var(--accent); outline-offset: -1.5px; }

@media (max-width: 700px) {
  .history-year-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 480px) {
  .history-box { padding: 20px; border-radius: 18px; }
  .history-year-grid { grid-template-columns: 1fr; }
  .history-kpi strong { font-size: 16px; }
}

@media (prefers-reduced-motion: reduce) {
  .history-overlay { animation: none; }
}
```

- [ ] **Step 2: Verify file is well-formed CSS**

Run: `python3 -c "import re; content = open('assets/css/streak-history.css').read(); opens = content.count('{'); closes = content.count('}'); print('balanced' if opens == closes else f'MISMATCH: {opens} opens vs {closes} closes')"`
Expected: `balanced`

- [ ] **Step 3: Commit**

```bash
git add assets/css/streak-history.css
git commit -m "feat: rewrite history modal CSS for calendar heatmap and KPI cards"
```

---

### Task 8: Browser verification pass

**Files:** none modified — verification only, using the `run` skill or direct browser open.

**Interfaces:** none new.

- [ ] **Step 1: Open the app**

Use the `run` skill (or open `flashcards.html` directly in a browser) to launch the app locally.

- [ ] **Step 2: Seed test data via browser devtools console**

To check "1 studied day" and "month with many days" scenarios without waiting on real usage, run in the browser console:

```js
localStorage.setItem('hsk_study_activity_v1', JSON.stringify({
  days: {
    '2026-08-01': { words: ['a'], seconds: 300 },
    '2026-08-03': { words: ['a','b'], seconds: 900 },
    '2026-08-04': { words: ['a','b','c'], seconds: 2400 },
    '2026-08-08': { words: ['a'], seconds: 1440 },
    '2025-11-15': { words: ['a'], seconds: 600 },
  }
}));
location.reload();
```

- [ ] **Step 3: Verify KPI header**

Open the history modal (via the trigger button). Confirm 4 cards show: 🔥 current streak, 🏆 longest streak, 📅 total days studied, ⏱ formatted total duration (not raw minutes/seconds). Confirm "Chuỗi ngắn nhất" is gone.

- [ ] **Step 4: Verify month view**

Confirm: Monday-first weekday header `T2 T3 T4 T5 T6 T7 CN`; Aug 8 2026 cell is visibly the darkest bucket (24 min → bucket 2, medium); Aug 1 (5 min → bucket 1) lighter; today (if system date is Aug 8 2026) has a distinct border; dates after today are subdued/non-interactive; hovering a studied day shows tooltip with `dd/mm/yyyy` and `Đã học: N phút`; header reads `Tháng 8 · 2026` (no Hán text); legend and summary line render below grid.

- [ ] **Step 5: Verify empty month**

Navigate to a month with no data (e.g. July 2026). Confirm all cells empty/bordered, summary reads `0 ngày học · 0 phút`, no JS errors in console.

- [ ] **Step 6: Verify month navigation boundary**

Navigate forward until reaching the real current month; confirm the "next month" button becomes disabled and does not advance further.

- [ ] **Step 7: Verify year view**

Click "Năm" segment. Confirm 12 mini-calendars render in a grid, Aug 2026 mini-month visibly shows its studied-day cells, year summary line shows aggregated stats. Click on a mini-month (e.g. Nov 2025) — confirm it switches to Month view showing November 2025 with the seeded Nov 15 cell visible.

- [ ] **Step 8: Verify year navigation boundary**

Navigate the year view forward until reaching the current real year; confirm "next year" is disabled.

- [ ] **Step 9: Verify dark/light theme**

Toggle the app's theme control (or `prefers-color-scheme` in devtools). Confirm intensity buckets remain visually distinct in both themes, no unstyled/invisible elements.

- [ ] **Step 10: Verify mobile viewport**

Resize browser (or devtools device toolbar) to ~375px width. Confirm: year grid collapses to 1 column, month grid remains 7 columns and fits without horizontal scroll, modal padding shrinks per the `max-width: 480px` rule, tap (click, since real touch isn't simulated) on a day cell shows tooltip content is still accessible (native `title` — acceptable for this codebase's existing pattern).

- [ ] **Step 11: Verify Escape key closes modal**

With the modal open, press `Escape`. Confirm it closes and the `keydown` listener doesn't linger (reopen and close again via the X button to confirm no duplicate-listener errors accumulate — check console for repeated firing).

- [ ] **Step 12: Verify streak calculation untouched**

Confirm the welcome toast and dashboard streak badge (outside the modal) still show the same streak numbers as before this change — these read from `studyStreak()`/`streakStats()` which were not modified.

- [ ] **Step 13: Clean up seeded test data**

In the browser console:

```js
localStorage.removeItem('hsk_study_activity_v1');
location.reload();
```

Confirm the app returns to its real prior state (or empty state, matching whatever was there before Step 2) — this step exists specifically because Step 2 overwrote real user data in localStorage for testing; if the developer running this had genuine study history before testing, that data was lost as of Step 2 and cannot be recovered by this step. Flag this to the user rather than silently reloading.

- [ ] **Step 14: No commit** — this task is verification-only, no files changed.

---

## Self-Review Notes

- **Spec coverage:** KPI header (Task 5/7), view switcher (Task 5/7), month view incl. heatmap/tooltip/nav/legend/summary (Tasks 2/5/7), year view incl. grid/click-to-jump/summary (Tasks 3/5/7), modal polish incl. sizing/close/keyboard (Task 6/7), removal of old bar-chart code (Tasks 2/6 verification grep) — all covered.
- **Placeholder scan:** no TBD/TODO; all code blocks are complete, runnable.
- **Type consistency:** `buildMonthGrid` cell shape (`dateKey, day, minutes, bucket, isToday, isFuture, inMonth`) used consistently across Task 2 (producer), Task 5 (`renderMonthGridHtml`, `renderYearView` consumers). `historyModalCursor` shape `{year, month}` consistent across Tasks 4/5. Function names (`setHistoryView`, `changeHistoryCursor`, `jumpToMonth`, `formatStudyDuration`, `intensityBucket`, `yearSummary`) match between producing and consuming tasks.
- **Data safety flag:** Task 8 Step 2 seeds `hsk_study_activity_v1` in the browser for manual QA, which overwrites whatever real activity data exists in that browser profile. Step 13 calls this out explicitly rather than pretending it's a clean round-trip — if this is run against a profile with real data, back it up first (`copy(localStorage.getItem('hsk_study_activity_v1')))` in devtools before Step 2).
