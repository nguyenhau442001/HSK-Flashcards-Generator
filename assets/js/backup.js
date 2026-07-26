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
