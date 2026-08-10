# Fast-Review (⚡ Ôn nhanh) — Design Spec

## Purpose

A Memrise-style speed-review mode: timed, forced-recall drilling on the words a
learner hasn't mastered yet, distinct from the untimed flip-card study mode
already in the app.

## Entry point

New third tab in the existing `view-tabs` row on the flashcard screen
(`flashcards.html`), alongside "🗂 Học flashcard" and "📋 Tổng quan từ vựng":

```html
<button id="reviewTab" class="view-tab" role="tab" aria-selected="false"
  aria-controls="reviewView" onclick="setViewMode('review')">⚡ Ôn nhanh</button>
```

`setViewMode(mode)` in `assets/js/vocabulary-overview.js` gains `'review'` as a
third accepted mode, following the same show/hide + `aria-selected` toggling
already used for `'cards'` / `'overview'`. Selecting the tab does **not**
auto-start a session — it shows the start screen (see below).

## Word pool

On session start, build the pool from the *current level's* `WORDS`, filtered
to `progress[w.id] !== 'known'` (covers both `'unknown'` and never-seen
words) — independent of whatever filter is active on the flashcard tab.

- Pool shuffled once per session (Fisher–Yates, same algorithm as
  `shuffleDeck`), each word appears at most once per session.
- If the pool is empty (everything already `known`), show a congratulatory
  empty state instead of a start screen — no session possible.

## Session rules

- **Lives**: 3 (♥♥♥), shown as icons in the session header.
- **Per-question timer**: fixed 20s countdown bar. Reaching 0 auto-submits as
  wrong (same as an incorrect answer).
- **Wrong answer or timeout**: −1 life, word's `progress[id] = 'unknown'`.
- **Correct answer**: `progress[id] = 'known'`. No life gained/lost.
- Every answered question (right or wrong) calls the existing
  `recordDailyStudy(wordId)` and `saveProgress()` — fast-review counts toward
  the same streak/history data as normal study, no new storage schema.
- **Session ends** when lives reach 0, or the pool is exhausted (all words in
  the session's shuffled pool answered) — whichever comes first.
- No pause/resume; leaving the tab (`setViewMode` to another tab) abandons
  the in-progress session without penalty beyond whatever was already scored.

## Question types (random per question, ~50/50)

Both types show the word's `hanzi` and Vietnamese `meaning` as context.

1. **Type pinyin** — text input, submit via Enter or a "Trả lời" button.
   Matching is case-insensitive, tone-mark-stripped, whitespace-collapsed
   loose match against the word's `pinyin` field (e.g. "ni hao" matches
   "nǐ hǎo"). Client-side tone-stripping table mirrors the one already used
   in `tools/normalize_expected_pinyin.py`, reimplemented in JS (no shared
   runtime between Python and browser).
2. **Multiple choice** — 4 buttons showing pinyin (with tone marks) as
   written in the data; 1 correct + 3 distractors drawn randomly from other
   words in the same level (excluding duplicates). Click to answer;
   immediate right/wrong feedback (same color language as existing
   known/unknown buttons: `--success-text` / `--danger-text`).

Each question picks its type randomly when rendered — no back-to-back-same
guarantee needed, plain random is fine (matches "xen kẽ" / interleaved intent).

## Screens

1. **Start screen** (shown on tab select): short rule summary (20s/câu, 3
   mạng, ưu tiên từ chưa nhớ), word count in pool, "Bắt đầu" button. Empty
   pool → congratulatory message instead, no start button.
2. **Session screen**: header with ♥ lives + countdown bar + progress
   ("câu N"), question body (hanzi + meaning + input or 4 choices), immediate
   feedback flash (correct/incorrect) before advancing to next question.
3. **Result screen**: correct/total, longest correct streak within the
   session, words reviewed. Two actions: "Chơi lại" (rebuild pool, new
   session) and "Về flashcard" (`setViewMode('cards')`).

## Files

- `assets/js/fast-review.js` — new module: pool building, timer, question
  rendering, answer checking, scoring, screen transitions. Follows existing
  module boundaries (state lives in `state.js`-style globals scoped to this
  file, reuses `saveProgress`/`recordDailyStudy`/`checkCelebration` from
  `progress.js`).
- `assets/css/fast-review.css` — new stylesheet for start/session/result
  screens, timer bar, lives, choice buttons. Reuses existing CSS custom
  properties (`--accent`, `--success-text`, `--danger-text`, etc.) for
  theme consistency — no new color tokens.
- `flashcards.html` — add the tab button, the `#reviewView` panel container,
  and the new stylesheet `<link>`.
- `assets/js/vocabulary-overview.js` — extend `setViewMode` to accept
  `'review'`.
- `assets/js/state.js` — add fast-review state variables (session pool,
  index, lives, score, timer handle) alongside existing globals.

## Explicitly out of scope

- No custom timer-length setting (fixed 20s).
- No cross-level review (pool is always the currently open level).
- No new localStorage schema — reuses `progress` and daily-study recording
  exactly as the flashcard tab does.
- No typed Vietnamese-meaning question type (pinyin match only, per design
  discussion — free-text meaning matching is unreliable to grade).
