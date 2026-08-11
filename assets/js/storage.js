// Local persistence for the currently selected HSK level.
function loadState() {
  try {
    const p = localStorage.getItem(storageKey('progress'));
    if (p) progress = JSON.parse(p);
  } catch (e) {}
  try {
    const pref = localStorage.getItem(storageKey('prefs'));
    if (pref) {
      const parsed = JSON.parse(pref);
      if (typeof parsed.showPinyin === 'boolean') showPinyin = parsed.showPinyin;
      if (Array.isArray(parsed.order) && parsed.order.length === WORDS.length) order = parsed.order;
    }
  } catch (e) {}
  filteredOrder = order.slice();
}
function saveProgress() {
  try { localStorage.setItem(storageKey('progress'), JSON.stringify(progress)); } catch (e) {}
}
function saveLevelProgress(level, progressObj) {
  try { localStorage.setItem('hsk_' + level + '_progress_v2', JSON.stringify(progressObj)); } catch (e) {}
}
function savePrefs() {
  try { localStorage.setItem(storageKey('prefs'), JSON.stringify({ showPinyin, order })); } catch (e) {}
}
