# Fast-Review Cross-Level Redesign — Design Spec

## Purpose

Move Fast-Review (⚡ Ôn nhanh) out of the single-level flashcard screen and
into its own primary tab, so a session can drill words across a cumulative
range of HSK levels (e.g. "up through HSK4" = HSK1+2+3+4 combined) instead of
being locked to whichever level the learner currently has open. Supersedes
the "no cross-level review" constraint in `2026-08-10-fast-review-design.md`.

## Entry point

New third primary tab, alongside the existing `📚 Từ vựng` / `部 Bộ thủ`:

```html
<button id="primaryTabReview" class="primary-tab" role="tab" aria-selected="false"
  aria-controls="screenReviewPicker" onclick="setPrimaryTab('review')">⚡ Ôn nhanh</button>
```

`setPrimaryTab(tab)` in `assets/js/radicals.js` gains `'review'` as a third
branch, following the same show/hide + `aria-selected` toggling already used
for `'vocab'` / `'radicals'`:

- Show `#screenReviewPicker` (new top-level screen, sibling of `screenPicker`
  / `screenRadicalHub`), hide the other two.
- Leaving `'review'` for another primary tab calls `abandonReviewSession()`
  (already implemented) so a live session's timer/interval is torn down —
  same guard used for the existing `setViewMode` / `goBackToPicker` cleanup.

The old third tab inside the per-level flashcard screen (`view-tabs` row,
`reviewTab` button, `setViewMode('review')` branch) is removed entirely —
Fast-Review no longer lives inside a single level's screen.

## Range picker screen (`#screenReviewPicker`)

Replaces the old per-level "start screen" as the first thing shown on
entering the tab. A slider with 6 stops (HSK1..HSK6). Moving to stop N means
"review every word from HSK1 through HSKN combined." Below the slider, show
the live cumulative word count (sum of `LEVELS[level].total` for the selected
range) so the learner sees scope before committing. A "Bắt đầu" button
starts loading.

No auto-start on tab entry — same non-auto-start principle as the original
design, just moved up a level.

## Data loading — Web Worker

New file `assets/js/fast-review-worker.js`. Given the array of level keys in
range (e.g. `['hsk1','hsk2','hsk3','hsk4']`), the worker:

1. `fetch`es each level's `dataUrl` in parallel (`Promise.all`).
2. Tags every word with its origin level: `{...word, _level: 'hsk2'}`.
3. Posts back one merged array via `postMessage`.

Rationale: word `id` collides across level files (each level's JSON restarts
at `id: 1`), so `_level` is required to disambiguate and to know which
level's progress store a given word's grading result belongs to. Loading
happens off the main thread so the UI thread stays free while HSK5/HSK6
(1300 / 2500 words) load; the main thread shows a loading skeleton in
`#screenReviewPicker` while waiting for the worker's message.

The main thread owns a single worker instance for the review flow, created
lazily on first "Bắt đầu" press, reused for subsequent range changes
("Chơi lại" with a different range doesn't need a fresh worker).

## State — dedicated to Fast-Review, isolated from flashcard-mode globals

Flashcard mode's `WORDS` / `progress` / `currentLevel` globals stay
untouched — they're single-level by design and Fast-Review must not corrupt
them by reassigning across a multi-level session.

New state in `assets/js/state.js`:

- `reviewWordPool` — flat array of `{..word fields.., _level}` for every
  word across the selected range (before pool-filtering; the shuffled
  per-session subset is computed from this, same as today).
- `reviewProgressByLevel` — `{ hsk1: {...}, hsk2: {...}, ... }`, one entry
  per level in the active range, each populated by reading that level's
  existing `hsk_<level>_progress_v2` localStorage key (reuses
  `readSavedLevelProgress(level)` from `levels.js`, already exists and is
  exactly this shape).

## Pool building

`buildReviewPool()` changes source: iterate `reviewWordPool` (not the
single-level `WORDS`), keep index `i` if
`reviewProgressByLevel[reviewWordPool[i]._level][reviewWordPool[i].id] !== 'known'`.
Shuffle: unchanged (Fisher–Yates).

## Grading / persistence

`gradeReviewAnswer()` changes where it writes: instead of the global
`progress[word.id]` + `saveProgress()` (which target `currentLevel`'s store),
it writes to `reviewProgressByLevel[word._level][word.id]` and persists via
a small helper that mirrors `saveProgress()` but targets the word's own
level's storage key (`hsk_<level>_progress_v2`), independent of whatever
`currentLevel` currently is (which may be `null` — Fast-Review no longer
requires a level to be "open" in the flashcard-mode sense).

`recordDailyStudy(word.id)` and `checkCelebration()` calls are unchanged —
both already operate on cross-cutting daily-activity data, not per-level
state, so they compose fine with a multi-level pool. (`checkCelebration`'s
"all words known" check is scoped to the flashcard mode's single-level
`WORDS`/`progress` globals and is irrelevant here — it simply won't fire
during a cross-level session, which is correct: there's no single-level
completion event to celebrate.)

## Session / question / result screens

Timer, lives, question-type selection (type/choice), pinyin loose-matching,
and homophone-safe distractor selection (`buildReviewChoices`) are unchanged
in mechanics — only their data source moves from `WORDS[idx]` to
`reviewWordPool[idx]` (which carries `_level` alongside the original word
fields, so `WORDS[i].pinyin`-style lookups become
`reviewWordPool[i].pinyin` etc.).

Result screen actions change:

- **"Chơi lại"** — rebuild pool from the *same* range (no new fetch,
  `reviewWordPool` is already loaded), start a new session. Unchanged
  behavior, just re-scoped.
- **"Về flashcard"** → replaced with **"Chọn lại phạm vi"**, which returns
  to `#screenReviewPicker` (the slider), not the flashcard screen. To leave
  Fast-Review entirely, the learner uses the always-visible `📚 Từ vựng`
  primary tab — no dedicated exit button needed on the result screen.

## Files

- `assets/js/fast-review-worker.js` — new. Parallel multi-level fetch +
  tagging, runs off main thread.
- `assets/js/fast-review.js` — pool builder, grading, and screen-render
  functions updated to read from `reviewWordPool` / `reviewProgressByLevel`
  instead of `WORDS` / `progress`; range-picker render/slider logic added.
- `assets/js/state.js` — add `reviewWordPool`, `reviewProgressByLevel`,
  worker instance handle.
- `assets/js/radicals.js` — `setPrimaryTab` gains the `'review'` branch.
- `assets/js/levels.js` — remove the `reviewTab` / `setViewMode('review')`
  wiring inside the per-level flashcard screen (superseded).
- `flashcards.html` — add `#primaryTabReview` button, add
  `#screenReviewPicker` top-level screen, remove the old `reviewTab` button
  and `#reviewView` panel from inside `#screenCards`.
- `assets/css/fast-review.css` — add range-picker/slider styles; existing
  session/result styles carry over unchanged (same class names, different
  data source).

## Explicitly out of scope

- No change to flashcard mode's single-level `WORDS`/`progress` model.
- No change to per-level progress storage schema — still one
  `hsk_<level>_progress_v2` key per level; Fast-Review just reads/writes
  several of them in one session instead of one.
- No caching of previously-loaded ranges across page reloads — each
  "Bắt đầu" press (after a fresh page load) re-fetches via the worker. (A
  "Chơi lại" within the same page session reuses the already-loaded pool.)
- No partial/lazy range loading (e.g. streaming HSK1 first while HSK6 still
  loads) — the picker screen waits for the full range before enabling
  session start.
