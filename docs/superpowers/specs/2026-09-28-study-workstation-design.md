# Study Workstation — 3-Column Desktop Layout

Date: 2026-09-28
Status: Approved design, pending implementation plan

## Goal

Refactor the HSK Flashcards app into a responsive 3-column "Study
Workstation" on desktop (Left: Reference Dock, Middle: existing Core
Learning Hub, Right: Interactive Study Lab), while keeping a clean
single-column mobile experience. Sync the active word across all three
columns. Preserve existing dark-mode theming and card aesthetic.

## Context / constraints discovered

- App is a plain-JS, no-build, no-framework SPA (`flashcards.html` +
  `assets/js/*.js` loaded as ordered globals + `assets/css/*.css`
  per-module stylesheets). New work follows this same pattern — no new
  framework or state-management library.
- A dedicated "Bộ thủ" (radicals) primary tab with full
  flashcard/overview modes **already exists** (`radicals.js`,
  `radicals-state.js`, `radical-card.js`, `database/radicals/*`). It
  stays as-is. The new left-sidebar radicals filter is a second,
  compact, independent consumer of the same existing radical JSON data
  — not a replacement.
- No Hán-Việt (Sino-Vietnamese reading) field exists anywhere in
  `database/vocabs/*.json`. Scoped out of the search popover for this
  phase (Hanzi / Pinyin / Vietnamese meaning / HSK level only).
- No stroke-order data exists locally. Stroke Order Canvas uses Hanzi
  Writer loaded from the `cdn.jsdelivr.net` CDN, which fetches
  per-character stroke data from its companion `hanzi-writer-data` CDN
  on demand. No local data, no backend.
- No grammar-role-tagged sentence data exists. Scoped to a new curated
  starter dataset (~30-50 HSK1-2 sentences), not full-corpus coverage.
- Vocab entry schema (reference):
  `{id, hanzi, pinyin, meaning, example_zh, example_py, expected_pinyin, example_vi}`.
- Existing global state lives in `assets/js/state.js` (e.g.
  `currentLevel`, `WORDS`, `order`, `idx`, `progress`). New sync state
  follows the same convention.

## 1. Layout shell & breakpoints

A `.workstation` CSS Grid wraps the app's existing content region.
Single column by default; 3 columns only above 1025px.

```css
.workstation {
  display: grid;
  grid-template-columns: 1fr;
  max-width: 1440px;
  margin: 0 auto;
}
@media (min-width: 1025px) {
  .workstation {
    grid-template-columns: 25% 50% 25%;
    grid-template-areas: "left middle right";
  }
  .workstation-left   { grid-area: left; }
  .workstation-middle { grid-area: middle; }
  .workstation-right  { grid-area: right; }
}
```

- **Middle column**: existing dashboard, primary tabs, all screens
  (`#screenVocabHub`, `#screenCards`, `#screenRadicalHub`, etc.),
  footer — re-parented into `.workstation-middle`, otherwise
  unchanged.
- **Left column** (desktop ≥1025px): Reference Dock rendered inline
  in `.workstation-left`.
- **Right column** (desktop ≥1025px): Interactive Study Lab rendered
  inline in `.workstation-right`.
- **Mobile (<768px, and generally <1025px)**: grid stays 1 column.
  - Left panel content becomes a top search bar (always visible) plus
    a "Bộ lọc" button that opens a `<dialog>` containing the radicals
    filter and weak-words list.
  - Right panel content becomes `<details>` accordions placed after
    the flashcard/card area.
  - Same DOM at both sizes — a `matchMedia('(min-width: 1025px)')`
    listener toggles a class (`is-desktop-dock` / `is-mobile-drawer`)
    that CSS uses to decide inline-vs-dialog/accordion presentation.
    No duplicated markup.

## 2. Left sidebar — Reference Dock

New files: `assets/js/sidebar-search.js`, `assets/js/weak-words.js`,
`assets/css/workstation.css`.

### Instant search

- Lazily builds one flat search index on first sidebar interaction, by
  fetching each `LEVELS[key].dataUrl` for HSK1–6 (2.0) only (HSK3.0
  and topic decks excluded from v1 to bound scope) and flattening to
  `{hanzi, pinyin, meaning, level}`.
- Debounced input (300ms). Matches by hanzi substring, pinyin
  (accent/tone-insensitive via a small tone-strip helper), and
  Vietnamese meaning substring.
- Results render in a popover list under the input, capped at ~20
  rows, each showing Hanzi / Pinyin / HSK level.
- Clicking a result calls `setActiveStudyWord(word)`.

### 214 Radicals quick filter

- Reuses existing `database/radicals/*` JSON (already loaded by
  `radicals.js`) — no new data.
- Compact grid/drawer of radicals grouped by `stroke_count`, with
  stroke-count filter chips.
- Clicking a radical shows its existing `examples[]` array as a mini
  word list; clicking an example calls `setActiveStudyWord`.

### Starred / Weak Words list

- New `localStorage` key `hsk_weak_words` (follows existing
  `storage.js` conventions), storing an array of `{hanzi, level}`.
- A new ★ toggle button added to the existing flashcard UI
  (`card-interactions.js`) writes to this list.
- Sidebar section lists starred words with inline ✕ remove buttons;
  clicking a word calls `setActiveStudyWord`.

## 3. Right sidebar — Interactive Study Lab

New files: `assets/js/stroke-canvas.js`,
`assets/js/grammar-breakdown.js`, `assets/css/sidebar-lab.css`,
`database/grammar/starter_sentences.json`.

### Hanzi Stroke Order Canvas

- Loads Hanzi Writer from
  `https://cdn.jsdelivr.net/npm/hanzi-writer@3/dist/hanzi-writer.min.js`
  (added to `flashcards.html`'s script list).
- Fixed 200×200 container with a CSS-drawn 田-grid background
  (`linear-gradient`/`border`, not an image).
- Subscribes to `onActiveWordChange`: destroys the previous writer
  instance and creates a new one for `word.hanzi` on every change.
- Two controls: "▶ Xem thứ tự nét" (stroke animation) and "✍️ Luyện
  viết" (interactive quiz mode via Hanzi Writer's built-in `quiz()`).
- If the CDN's per-character stroke fetch fails (offline, or
  character not covered), shows an inline fallback message instead of
  a blank box.

### Sentence & Grammar Breakdown

- Curated starter dataset `database/grammar/starter_sentences.json`:
  ~30-50 HSK1-2 sentences (reusing hanzi from existing `example_zh`
  fields where possible), each tagged:
  `{zh, roles: [{text, type: 'S'|'V'|'O'|'M'}], grammar_point: {pattern, note}}`.
- On `onActiveWordChange`, looks up whether the active word's hanzi
  appears in the starter set.
  - If found: renders color-coded spans (S=blue, V=green, O=orange,
    M=gray) plus a grammar-note card (e.g. 把, 被, 连...都...).
  - If not found: shows a placeholder — "Chưa có phân tích ngữ pháp
    cho từ này" — rather than an empty or broken panel.

## 4. State sync mechanism

`state.js` additions:

```js
let activeStudyWord = null;
const activeWordListeners = [];
function onActiveWordChange(fn) { activeWordListeners.push(fn); }
function setActiveStudyWord(word) {
  activeStudyWord = word;
  activeWordListeners.forEach(fn => fn(word));
}
```

- `card-interactions.js`'s existing navigation path (shuffle/next/prev)
  gets one added call to `setActiveStudyWord(WORDS[order[idx]])`, so
  the middle hub is a sync source as well as a sink.
- `stroke-canvas.js` and `grammar-breakdown.js` each call
  `onActiveWordChange` once at load to subscribe.
- Left sidebar's search results, radical examples, and weak-words
  clicks all funnel through `setActiveStudyWord`.
- Net effect: any of the four surfaces (search result, radical
  example, weak word, flashcard nav) can drive the other three.

## Theming

No new CSS variables. New panels consume the existing `colors.*` /
`--*` custom-property tokens already defined in `base.css`, so the
existing dark/light theme toggle (`theme.js`) applies for free.

## Files touched

**New:**
- `assets/js/sidebar-search.js`
- `assets/js/weak-words.js`
- `assets/js/stroke-canvas.js`
- `assets/js/grammar-breakdown.js`
- `assets/css/workstation.css`
- `assets/css/sidebar-lab.css`
- `database/grammar/starter_sentences.json`

**Edited:**
- `flashcards.html` — grid wrapper markup, new script tag(s) + Hanzi
  Writer CDN tag
- `assets/js/state.js` — sync primitives
  (`activeStudyWord`/`onActiveWordChange`/`setActiveStudyWord`)
- `assets/js/card-interactions.js` — fire sync on nav; add ★ toggle
  button

**Untouched (reused as-is):**
- `radicals.js`, `radicals-state.js`, `radical-card.js`,
  `database/radicals/*` — existing dedicated Bộ thủ tab stays exactly
  as it is today.

## Out of scope (this phase)

- Hán-Việt readings (not in source data).
- HSK 3.0 / topic decks in the unified search index.
- Full grammar-role coverage beyond the curated starter set.
- Any new JS framework or state-management library.
