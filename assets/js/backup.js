// Export and import progress snapshots between devices.
function exportProgress() {
  const data = JSON.stringify({ level: currentLevel, progress, order, showPinyin }, null, 2);
  const blob = new Blob([data], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'hsk_progress_' + currentLevel + '.json';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function importProgress(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(e) {
    try {
      const data = JSON.parse(e.target.result);
      if (data.level && data.level !== currentLevel) {
        if (!confirm('Bản sao này thuộc cấp độ ' + data.level.toUpperCase() + ', không phải ' + currentLevel.toUpperCase() + '. Vẫn khôi phục?')) return;
      }
      if (!confirm('Khôi phục tiến trình từ một bản sao đã tải trước đó. Tiến trình hiện tại có thể bị thay thế.')) return;
      if (data.progress) progress = data.progress;
      if (Array.isArray(data.order) && data.order.length === WORDS.length) order = data.order;
      if (typeof data.showPinyin === 'boolean') showPinyin = data.showPinyin;
      saveProgress();
      savePrefs();
      renderLearningDashboard();
      const btn = document.getElementById('pinyinToggle');
      btn.textContent = showPinyin ? '👁 Đang hiện pinyin' : '🙈 Chế độ thử thách: ẩn pinyin';
      btn.classList.toggle('on', !showPinyin);
      setFilter(currentFilter);
      alert('Đã khôi phục tiến trình thành công!');
    } catch (err) {
      alert('Bản sao tiến trình không hợp lệ.');
    }
  };
  reader.readAsText(file);
  event.target.value = '';
}

function exportRadicalProgress() {
  const data = JSON.stringify({
    type: 'radicals',
    version: 1,
    progress: radicalProgress,
    showPinyin: showRadicalPinyin,
  }, null, 2);
  const blob = new Blob([data], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'hsk_radicals_progress.json';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function importRadicalProgress(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(loadEvent) {
    try {
      const data = JSON.parse(loadEvent.target.result);
      if (data.type !== 'radicals' || !data.progress || typeof data.progress !== 'object' || Array.isArray(data.progress)) {
        throw new Error('invalid radical backup');
      }
      if (!confirm('Khôi phục tiến trình Bộ thủ từ bản sao này? Tiến trình hiện tại có thể bị thay thế.')) return;

      const restoredProgress = {};
      Object.entries(data.progress).forEach(([key, status]) => {
        if (/^\d+$/.test(key) && Number(key) >= 1 && Number(key) <= 214 && ['known', 'unknown'].includes(status)) {
          restoredProgress[key] = status;
        }
      });
      radicalProgress = restoredProgress;
      if (typeof data.showPinyin === 'boolean') showRadicalPinyin = data.showPinyin;
      saveRadicalProgress();
      saveRadicalPrefs();

      const pinyinButton = document.getElementById('radicalPinyinToggle');
      if (pinyinButton) {
        pinyinButton.textContent = showRadicalPinyin ? '👁 Đang hiện pinyin' : '🙈 Chế độ thử thách: ẩn pinyin';
        pinyinButton.classList.toggle('on', !showRadicalPinyin);
      }
      setRadicalFilter(radicalCurrentFilter);
      if (radicalCurrentView === 'overview') renderRadicalOverview();
      alert('Đã khôi phục tiến trình Bộ thủ thành công!');
    } catch (error) {
      alert('Bản sao tiến trình Bộ thủ không hợp lệ.');
    }
  };
  reader.readAsText(file);
  event.target.value = '';
}
