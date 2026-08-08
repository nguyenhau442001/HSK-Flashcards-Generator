# Streak history & correctness — design spec

## Problem

Streak display is roughly correct today but has two issues:

1. **Two independent streak calculations** exist:
   - `studyStreak(days)` in [levels.js](../../../assets/js/levels.js) — derived from `STUDY_ACTIVITY_KEY` (days the user actually studied ≥1 word). Used on the dashboard (`learningStreak` node).
   - A second, separate streak counter stored in `hsk_visit_history_v1` — increments on *any visit*, independent of whether the user studied. Used only for the welcome toast copy.

   These can disagree (e.g. user opens the app but studies nothing — visit-streak continues, study-streak doesn't). One source of truth is needed.

2. **No history is kept.** `recordDailyStudy` deletes any day entry older than 120 days (`age > 120`), and there is no UI to view past activity at all. Users cannot see which days they studied, their longest streak, or their shortest streak between breaks.

## Goals

- Single source of truth for streak: derived from `STUDY_ACTIVITY_KEY` (day counts as "học" if it has ≥1 recorded word).
- Keep full history forever (remove the 120-day deletion).
- Add a history view: GitHub-style contribution heatmap (binary: studied / not studied per day) plus streak stats (current, longest, shortest, days studied this month, total days studied).
- No new tracking mechanism (no session-time/heartbeat). Everything derives from data already recorded by `recordDailyStudy`.

## Non-goals

- Do not track session duration / hours online. Rejected during design for complexity/bug-risk vs. value — binary "studied that day" is sufficient for streak and history purposes.
- Do not add a new primary-nav tab. History is a modal launched from the existing dashboard.

## Design

### 1. Data layer (`assets/js/levels.js`)

- `recordDailyStudy(wordId)`: remove the block that deletes `activity.days[dateKey]` entries older than 120 days. Data format (`days[date] = [wordId, ...]`) is unchanged — no migration needed.
- `studyStreak(days)`: unchanged. Already correctly counts backward from today (or yesterday, if today has no entries) while consecutive calendar days have non-empty entries.
- New `streakStats(days)`:
  - Input: the `days` map (`{dateKey: [wordId, ...]}`).
  - Collect all dateKeys with a non-empty array, sort ascending.
  - Walk the sorted list, grouping into consecutive runs (a gap of exactly 1 calendar day continues the run; any larger gap starts a new run).
  - Return `{ current, longest, shortest, totalDaysStudied }` where:
    - `current` = result of `studyStreak(days)` (0 if today and yesterday are both empty).
    - `longest` = max run length across all runs.
    - `shortest` = min run length across all *completed* runs (i.e., excluding the current in-progress run, unless it's the only run).
    - `totalDaysStudied` = count of all dateKeys with entries.

### 2. Welcome toast (`showWelcomeToast`)

- Remove the local streak computation (the `dayDifference`/`continuedStreak`/`streak` block currently keyed off `hsk_visit_history_v1`).
- Call `studyStreak(readStudyActivity().days)` to get the streak for greeting copy (e.g. "chuỗi vẫn còn nóng" condition).
- `hsk_visit_history_v1` is kept only to store `lastVisit` and `lastGreeting` (for greeting dedup) — its `streak` field is dropped.

### 3. History modal (new)

- Trigger: small button next to the `learningStreak` label on the dashboard (e.g. "Xem lịch sử 📊").
- Content:
  - **Heatmap**: ~52 weeks of calendar cells (GitHub contribution graph layout), 2 visual states only — studied vs. not studied (binary color, no gradient). Cells before the user's first-ever recorded day are rendered as empty/muted.
  - **Tooltip** per cell: date + word count studied that day (0 if not studied).
  - **Stats row**: current streak, longest streak, shortest streak, days studied this month, total days studied — all from `streakStats()`.
- Implementation: plain DOM/CSS grid, consistent with existing dashboard styling. No charting library.

## Testing

- Unit-style checks (manual harness or existing dev-server pattern used in prior radical-overview work) for `streakStats`:
  - Empty days → all zeros.
  - Single day studied → current/longest/shortest all 1, no "shortest" from an in-progress run.
  - Multiple runs with a gap → longest/shortest reflect the completed runs correctly, current reflects only the most recent run (or 0 if broken).
- Manual verification: open modal, confirm heatmap renders, confirm welcome toast streak matches dashboard streak (single source of truth).
