/**
 * ai-image-service.js
 * Google AI Studio (Imagen 3 & Gemini Flash) Image Generator & IndexedDB Caching for HSK Flashcards.
 */

// 1. IndexedDB Persistent Binary Cache Engine
const AiImageCache = (function() {
  const DB_NAME = 'HSK_Flashcards_AIDB';
  const DB_VERSION = 1;
  const STORE_NAME = 'ai_illustrations';

  let dbPromise = null;

  function getDB() {
    if (!dbPromise) {
      dbPromise = new Promise((resolve, reject) => {
        if (typeof indexedDB === 'undefined') {
          resolve(null);
          return;
        }
        const req = indexedDB.open(DB_NAME, DB_VERSION);
        req.onupgradeneeded = (e) => {
          const db = e.target.result;
          if (!db.objectStoreNames.contains(STORE_NAME)) {
            db.createObjectStore(STORE_NAME, { keyPath: 'hanzi' });
          }
        };
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => {
          console.warn('[AiImageCache] Failed to open IndexedDB:', req.error);
          resolve(null);
        };
      });
    }
    return dbPromise;
  }

  return {
    async get(hanzi) {
      if (!hanzi) return null;
      try {
        const db = await getDB();
        if (!db) return null;
        return new Promise((resolve) => {
          const tx = db.transaction(STORE_NAME, 'readonly');
          const store = tx.objectStore(STORE_NAME);
          const req = store.get(hanzi);
          req.onsuccess = () => resolve(req.result ? req.result.payload : null);
          req.onerror = () => resolve(null);
        });
      } catch (err) {
        console.warn('[AiImageCache] Get error:', err);
        return null;
      }
    },

    async set(hanzi, payload) {
      if (!hanzi || !payload) return false;
      try {
        const db = await getDB();
        if (!db) return false;
        return new Promise((resolve) => {
          const tx = db.transaction(STORE_NAME, 'readwrite');
          const store = tx.objectStore(STORE_NAME);
          store.put({ hanzi, payload, updatedAt: Date.now() });
          tx.oncomplete = () => resolve(true);
          tx.onerror = () => resolve(false);
        });
      } catch (err) {
        console.warn('[AiImageCache] Set error:', err);
        return false;
      }
    },

    async delete(hanzi) {
      try {
        const db = await getDB();
        if (!db) return;
        const tx = db.transaction(STORE_NAME, 'readwrite');
        tx.objectStore(STORE_NAME).delete(hanzi);
      } catch (e) {}
    }
  };
})();

// 2. Optimized Prompt Engineering for Google AI Studio
function buildGoogleAiPrompt(word, pos) {
  const hanzi = (word.hanzi || '').trim();
  const meaning = (word.meaning || '').trim();
  const posName = pos?.en || 'concept';
  const posCode = pos?.code || 'noun';

  const baseStyle = "A minimalist modern 2D flat vector icon illustration, dark mode aesthetic with deep dark slate background (#0f172a), crisp geometric contours, vibrant harmonious accent colors, clean negative space, iconic language flashcard memory symbol";

  let posMetaphor = '';
  switch (posCode) {
    case 'adj':
      posMetaphor = `visual metaphor for the adjective quality or state: '${meaning}'`;
      break;
    case 'verb':
      posMetaphor = `visual metaphor symbolizing the action of: '${meaning}'`;
      break;
    case 'noun':
      posMetaphor = `iconic visual representation of: '${meaning}'`;
      break;
    default:
      posMetaphor = `conceptual visual symbol representing: '${meaning}'`;
  }

  const negativeExclusions = "STRICTLY NO text, NO letters, NO words, NO subtitles, NO typography, NO Chinese characters, NO English text, NO watermarks, NO photographic realism";

  return `${baseStyle}. Subject: ${posMetaphor}. Designed for language memory anchoring. ${negativeExclusions}.`;
}

// 3. API Communication Engine with Google AI Studio
const GoogleAiService = {
  getApiKey() {
    try {
      return (localStorage.getItem('hsk_google_ai_key') || '').trim();
    } catch (e) {
      return '';
    }
  },

  setApiKey(key) {
    try {
      localStorage.setItem('hsk_google_ai_key', (key || '').trim());
    } catch (e) {}
  },

  clearApiKey() {
    try {
      localStorage.removeItem('hsk_google_ai_key');
    } catch (e) {}
  },

  async generate(word, pos) {
    const apiKey = this.getApiKey();
    if (!apiKey) {
      throw new Error('MISSING_KEY');
    }

    const promptText = buildGoogleAiPrompt(word, pos);

    // Thử nghiệm cấp 1: Google Imagen 3 (imagen-3.0-generate-002)
    try {
      const imagenUrl = `https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key=${encodeURIComponent(apiKey)}`;
      const payload = {
        instances: [{ prompt: promptText }],
        parameters: {
          sampleCount: 1,
          aspectRatio: "1:1",
          outputOptions: { mimeType: "image/jpeg" }
        }
      };

      const res = await fetch(imagenUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        const data = await res.json();
        const base64 = data.predictions?.[0]?.bytesBase64Encoded;
        if (base64) {
          return { type: 'img', src: `data:image/jpeg;base64,${base64}` };
        }
      } else {
        const errJson = await res.json().catch(() => ({}));
        console.warn('[GoogleAiService] Imagen 3 returned status:', res.status, errJson);
      }
    } catch (imagenErr) {
      console.warn('[GoogleAiService] Imagen 3 fetch error, trying Gemini fallback:', imagenErr);
    }

    // Dự phòng cấp 2: Gemini 2.5/1.5 Flash sinh SVG thuần (Luôn miễn phí & khả dụng 100% trên mọi key Google AI Studio)
    try {
      const geminiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${encodeURIComponent(apiKey)}`;
      const geminiPrompt = `Create a clean, minimalist, modern 2D vector graphic SVG for the language concept "${word.meaning}" (part of speech: ${pos?.label || 'từ vựng'}).
Requirements:
1. Valid inline <svg viewBox="0 0 200 200" ...> with dark-mode friendly theme (navy/slate #0f172a background circle, vibrant orange/emerald/sky vector paths).
2. STRICTLY NO text, NO letters, NO words, NO Chinese characters inside the graphic.
3. Return ONLY the raw <svg>...</svg> code, without markdown backticks or explanation.`;

      const res = await fetch(geminiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: geminiPrompt }] }]
        })
      });

      if (res.ok) {
        const data = await res.json();
        const text = data.candidates?.[0]?.content?.parts?.[0]?.text || '';
        const svgMatch = text.match(/<svg[\s\S]*?<\/svg>/i);
        if (svgMatch) {
          return { type: 'svg', svg: svgMatch[0] };
        }
      }
    } catch (geminiErr) {
      console.warn('[GoogleAiService] Gemini Flash SVG fallback failed:', geminiErr);
    }

    throw new Error('Không thể kết nối đến Google AI Studio. Vui lòng kiểm tra lại API key hoặc kết nối mạng.');
  }
};

// 4. Modal & UI Interaction Logic
function openAiSettingsModal() {
  const dialog = document.getElementById('aiSettingsDialog');
  const input = document.getElementById('googleAiKeyInput');
  const statusEl = document.getElementById('aiKeyStatusText');
  if (!dialog) return;

  const currentKey = GoogleAiService.getApiKey();
  if (input) {
    input.value = currentKey;
    input.type = 'password';
  }
  if (statusEl) {
    statusEl.textContent = currentKey ? '✓ Đã lưu khóa Google AI Studio' : 'Chưa thiết lập khóa';
    statusEl.className = currentKey ? 'ai-settings-status ai-status-ok' : 'ai-settings-status';
  }
  dialog.showModal();
}

function closeAiSettingsModal() {
  const dialog = document.getElementById('aiSettingsDialog');
  if (dialog) dialog.close();
}

function saveGoogleAiKey() {
  const input = document.getElementById('googleAiKeyInput');
  const key = (input ? input.value : '').trim();
  if (!key) {
    alert('Vui lòng nhập Google AI Studio API Key (bắt đầu bằng AIzaSy...)');
    return;
  }
  GoogleAiService.setApiKey(key);
  closeAiSettingsModal();
  // Kích hoạt sinh ảnh nếu đang ở thẻ hiện tại
  if (typeof handleAiImageGenClick === 'function') {
    handleAiImageGenClick();
  }
}

function clearGoogleAiKey() {
  if (confirm('Bạn có chắc muốn xóa Google AI Studio Key khỏi trình duyệt này?')) {
    GoogleAiService.clearApiKey();
    const input = document.getElementById('googleAiKeyInput');
    if (input) input.value = '';
    const statusEl = document.getElementById('aiKeyStatusText');
    if (statusEl) {
      statusEl.textContent = 'Đã xóa khóa';
      statusEl.className = 'ai-settings-status';
    }
  }
}

function toggleAiKeyVisibility() {
  const input = document.getElementById('googleAiKeyInput');
  const btn = document.getElementById('toggleAiKeyVisBtn');
  if (!input || !btn) return;
  if (input.type === 'password') {
    input.type = 'text';
    btn.textContent = '🙈';
  } else {
    input.type = 'password';
    btn.textContent = '👁';
  }
}

// 5. Flashcard Card Action Trigger
async function handleAiImageGenClick() {
  const word = (typeof activeStudyWord !== 'undefined') ? activeStudyWord : null;
  if (!word) return;

  const apiKey = GoogleAiService.getApiKey();
  if (!apiKey) {
    openAiSettingsModal();
    return;
  }

  const pos = (typeof getWordPartOfSpeech === 'function') ? getWordPartOfSpeech(word) : null;
  const imgEl = document.getElementById('cardIllustrationImg');
  const svgEl = document.getElementById('cardIllustrationSvg');
  const skeletonEl = document.getElementById('aiSkeletonLoader');
  const genBtn = document.getElementById('aiGenTriggerBtn');

  // Bắt đầu trạng thái Loading Shimmer
  if (skeletonEl) skeletonEl.hidden = false;
  if (genBtn) genBtn.hidden = true;

  try {
    const result = await GoogleAiService.generate(word, pos);

    // Lưu vĩnh viễn vào IndexedDB cache để dùng offline & không tốn quota lần sau
    await AiImageCache.set(word.hanzi, result);

    // Hiển thị mượt mà lên thẻ Flashcard
    if (result.type === 'img') {
      imgEl.src = result.src;
      imgEl.hidden = false;
      svgEl.hidden = true;
      svgEl.innerHTML = '';
    } else if (result.type === 'svg') {
      svgEl.innerHTML = result.svg;
      svgEl.hidden = false;
      imgEl.hidden = true;
      imgEl.src = '';
    }
  } catch (err) {
    console.error('[AI Gen Error]', err);
    alert(err.message || 'Không thể tạo ảnh từ Google AI Studio.');
  } finally {
    if (skeletonEl) skeletonEl.hidden = true;
    if (genBtn) {
      genBtn.hidden = false;
      genBtn.textContent = '↻ Tạo lại';
    }
  }
}

// Global exposure
if (typeof window !== 'undefined') {
  window.AiImageCache = AiImageCache;
  window.buildGoogleAiPrompt = buildGoogleAiPrompt;
  window.GoogleAiService = GoogleAiService;
  window.openAiSettingsModal = openAiSettingsModal;
  window.closeAiSettingsModal = closeAiSettingsModal;
  window.saveGoogleAiKey = saveGoogleAiKey;
  window.clearGoogleAiKey = clearGoogleAiKey;
  window.toggleAiKeyVisibility = toggleAiKeyVisibility;
  window.handleAiImageGenClick = handleAiImageGenClick;
}
