// Topic tab: dynamic grid of topic decks, reusing the LEVELS/selectLevel pipeline.
function topicKnownCount(topicKey) {
  const data = readSavedLevelProgress(topicKey);
  return Object.values(data).filter(status => status === 'known').length;
}

function renderTopicGrid() {
  const grid = document.getElementById('topicGrid');
  if (!grid) return;
  const keys = Object.keys(TOPICS);
  if (keys.length === 0) {
    grid.innerHTML = '<div class="loading-text">Chưa có chủ đề nào.</div>';
    return;
  }
  grid.innerHTML = keys.map(key => {
    const topic = TOPICS[key];
    const known = topicKnownCount(key);
    const pct = topic.total > 0 ? (known / topic.total * 100) : 0;
    return `
      <button class="level-card" type="button" ${topic.available ? `onclick="selectLevel('${key}')"` : 'disabled'}>
        <div class="lvl-num">${topic.icon || '🏷️'}</div>
        <div class="lvl-label">${topic.label}</div>
        <div class="lvl-count">${topic.total} từ</div>
        <div class="lvl-mastery-track"><div class="lvl-mastery-fill" style="width:${pct}%"></div></div>
        <div class="lvl-mastery-text">${known} / ${topic.total} đã nhớ</div>
      </button>`;
  }).join('');
}
