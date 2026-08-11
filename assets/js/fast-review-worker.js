// Fast-review worker: fetches multiple level word lists in parallel off the main thread.
self.onmessage = async function (e) {
  const { levels, dataUrls } = e.data;
  try {
    const results = await Promise.all(dataUrls.map(url => fetch(url).then(res => {
      if (!res.ok) throw new Error('fetch failed: ' + url);
      return res.json();
    })));
    const words = [];
    for (let i = 0; i < results.length; i++) {
      const level = levels[i];
      for (const word of results[i]) {
        words.push({ ...word, _level: level });
      }
    }
    self.postMessage({ ok: true, words });
  } catch (err) {
    self.postMessage({ ok: false, error: String(err && err.message || err) });
  }
};
