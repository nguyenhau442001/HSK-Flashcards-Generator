# Calendar-based Learning History Redesign

## Problem

The current "Lịch sử học tập" modal (`showHistoryModal()` in `assets/js/levels.js`) renders a per-day bar chart of study minutes for the selected month. With sparse data this produces mostly empty bars and reads like a stats dashboard rather than a learning history. It also lacks a year-level overview.

## Goals

Replace the bar chart with a calendar-grid heatmap (month + year views), tighten the KPI header, and polish the modal shell — while leaving all data storage and streak-calculation logic untouched.

## Non-goals

- No changes to `hsk_study_activity_v1` schema or any localStorage key.
- No changes to `studyStreak()` / `streakStats()` calculation logic.
- No new dependencies.
- No video/asset rendering.

## Data (unchanged)

- `STUDY_ACTIVITY_KEY = 'hsk_study_activity_v1'` → `{ days: { 'YYYY-MM-DD': { words: string[], seconds: number } } }`
- `readStudyActivity()`, `dayWordCount()`, `daySeconds()`, `studyStreak(days)`, `streakStats(days)` are reused as-is.
- `streakStats()` continues to compute `shortest` — it is simply not rendered anymore.

## State

Replace module-level `historyModalMonth` with:

```js
let historyModalView = 'month'; // 'month' | 'year'
let historyModalCursor = { year, month }; // month is 0-indexed, used by both views
```

`showHistoryModal()` initializes `historyModalView = 'month'` and `historyModalCursor` to the current year/month, same as today.

## KPI Header

Four compact stat cards, replacing the current 4-card block (which included "Chuỗi ngắn nhất"):

- 🔥 Chuỗi hiện tại: `stats.current` ngày
- 🏆 Chuỗi dài nhất: `stats.longest` ngày
- 📅 Ngày đã học: `stats.totalDaysStudied` ngày
- ⏱ Tổng thời gian: formatted from `sum(daySeconds(day) for all days)/60` → e.g. `4 giờ 32 phút` or `45 phút` if under an hour. New small helper `formatStudyDuration(totalMinutes)`.

Styling: subtle background (existing `--bg` or low-opacity `--accent-light`, not the current heavy `--success-bg` green), number is the primary visual weight (large/bold), label is smaller/secondary (`--text-secondary`).

## View Switcher

Segmented control `[ Tháng ] [ Năm ]` above the calendar area. Default: Tháng. Clicking a segment sets `historyModalView` and re-renders. Styled as a pill toggle using existing border/accent tokens (no new colors).

## Month View

Calendar grid, Monday-first: header row `T2 T3 T4 T5 T6 T7 CN`.

- Leading/trailing padding cells (days outside the month) render empty — no number, no border, not interactive, not hoverable.
- Each in-month day is one cell. Intensity mapped from that day's minutes into 5 buckets using `--accent` at increasing opacity (0 handled as "empty" style, not accent):
  - 0 phút → empty (border only, e.g. `var(--border)`)
  - 1–10 → accent @ ~0.15
  - 11–30 → accent @ ~0.35
  - 31–60 → accent @ ~0.6
  - >60 → accent @ 1.0
- Today gets a distinct border (e.g. 2px `--accent` outline), independent of intensity fill.
- Future dates (relative to real "now") are visually disabled/subdued and not interactive.
- Hover (desktop) / tap (mobile) shows a tooltip: `"dd/mm/yyyy"` + `"Đã học: N phút"`. Implemented via native `title` attribute, consistent with the existing `.history-bar-col` tooltip pattern — no new tooltip library.
- Header: `‹  Tháng {N} · {year}  ›` (Vietnamese only — no Hán month name, to avoid the redundant "Tháng 8 · 八月" pairing which restates the same month twice). Prev/next buttons disabled at appropriate boundaries (next disabled when viewing current month; no lower bound needed but keep simple guard consistent with existing `changeHistoryModalMonth`).
- Below the grid: compact legend `Ít  □ ▨ ▧ ▦ ■  Nhiều` mapped to the same 5 buckets, plus a summary line: `"{N} ngày học · {duration}"` for the visible month (reusing `formatStudyDuration`).

`MONTH_LABELS` (existing Hán array) is no longer used for the header text; keep the array only if still referenced elsewhere, otherwise remove it (grep confirms it's only used in the modal header — remove it).

## Year View

Header: `‹ {year} ›`, prev/next navigate `historyModalCursor.year`; next disabled when viewing the current calendar year.

Body: 12 mini calendar-heatmaps (one per month), same 5-level intensity logic as month view, no per-cell tooltips required at this scale (optional, skip for simplicity), each mini-calendar has a compact month label (`Th 8`) at its top.

Layout: CSS grid, `repeat(auto-fit, minmax(...))` or explicit breakpoints — 3–4 columns desktop, 1–2 columns mobile, following the existing `max-width: 480/520px` breakpoint convention used elsewhere in this codebase.

Clicking anywhere inside a mini-calendar (header or any day cell) sets `historyModalView = 'month'` and `historyModalCursor = { year, month: thatMonth }`, then re-renders.

Year summary below the grid: `"{N} ngày học · {duration}"` aggregated across the whole year.

## Modal Shell

- Desktop: `max-width: 900px`, `height: auto`, `padding: 28–32px`, `border-radius: 24px`.
- Clean hierarchy: title, close button, segmented control, view body.
- No gradients, no heavy glassmorphism — flat surface using existing `--card-bg` / `--border` tokens, consistent with the rest of the app's style.
- Close button, nav buttons get clear hover/focus states (`:focus-visible` outline using `--accent`).
- Keyboard: `Escape` closes the modal (new `keydown` listener added on open, removed on close). Left/Right arrow keys navigate month/year when the modal has focus (nice-to-have, low risk — skip if it conflicts with existing global key handlers; verify no collision with flashcard keyboard shortcuts before wiring, since those are likely inactive while the modal overlay is open but should be double-checked).
- Mobile: modal remains scrollable overlay as today; grid/cells shrink via existing `max-width: 480/520px` breakpoint pattern.

## Code Changes

**`assets/js/levels.js`**
- Remove: `buildMonthBars()`, `monthAverageMinutes()`, `MONTH_LABELS` (grep-confirmed used only at the old header line being replaced), old `historyModalMonth` state, `changeHistoryModalMonth()` (replaced).
- Add: `historyModalView`, `historyModalCursor` state; `formatStudyDuration(totalMinutes)`; `buildMonthGrid(days, year, month)` (returns Mon-first grid with padding cells + intensity bucket + future flag); `intensityBucket(minutes)`; `changeHistoryCursor(delta)` (month or year depending on `historyModalView`); `setHistoryView(view)`; `renderHistoryModalBody()` rewritten to branch on `historyModalView`; `renderMonthView()`, `renderYearView()` render helpers; `jumpToMonth(year, month)` for year→month click.
- Keep untouched: `readStudyActivity`, `dayWordCount`, `daySeconds`, `studyStreak`, `streakStats`, `recordDailyStudy`, `recordStudySeconds`, `startStudyHeartbeat`, `showHistoryModal` (only its body-render call changes).

**`assets/css/streak-history.css`**
- Remove: `.history-stat` (green block variant), `.history-chart-wrap`, `.history-y-axis*`, `.history-bar-chart`, `.history-avg-line`, `.history-bar*`, `.history-axis-caption`, old `.history-box` sizing.
- Add: KPI card styles, segmented control styles, month-grid + day-cell styles (5 intensity levels via `--accent` opacity), today-border style, future-day style, legend styles, year-grid + mini-calendar styles, updated `.history-box` sizing (900px/28-32px/24px radius), focus-visible states, mobile breakpoint rules.

**`flashcards.html`**
- No structural change expected beyond what `showHistoryModal()` already injects dynamically; verify no stale references to removed chart class names.

## Testing

Manual verification in-browser (per goal's checklist):
1. Dataset with exactly 1 studied day — month view shows 1 filled cell, correct stats, no crashes on empty months elsewhere.
2. Month with zero data — grid renders all-empty cells, summary shows "0 ngày học · 0 phút".
3. Month with many studied days across varying intensities — all 5 buckets visually distinguishable.
4. Month and year navigation — boundaries (future) correctly disabled, cursor state consistent across view switches.
5. Dark and light theme — intensity opacity steps remain legible in both.
6. Mobile viewport — grid columns collapse per breakpoint, tap tooltip works, modal remains scrollable.
7. No video/asset build steps triggered — UI-only change.

No automated test suite exists for this UI in the repo; verification is manual via the `run` skill launching `flashcards.html`.
