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
