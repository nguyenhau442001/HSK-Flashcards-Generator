/**
 * word-illustrations.js
 * Visual Mnemonic & Illustration Manager for HSK Flashcards.
 * Supports vector SVGs, remote URLs, and base64 images.
 */

const WORD_ILLUSTRATIONS_DB = {
  // 总结 (zǒngjié - tổng kết): Người thuyết trình bên bục và bảng tổng kết gạch đầu dòng
  '总结': {
    type: 'svg',
    svg: `<svg viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Background glow -->
      <circle cx="100" cy="100" r="82" fill="currentColor" fill-opacity="0.04" />
      <circle cx="100" cy="100" r="80" stroke="currentColor" stroke-opacity="0.12" stroke-width="2" stroke-dasharray="4 4" />
      
      <!-- Summary Board (Bảng tổng kết) -->
      <rect x="36" y="38" width="86" height="108" rx="8" fill="#1e2230" stroke="#38bdf8" stroke-width="3" />
      <!-- Clip on board -->
      <rect x="65" y="30" width="28" height="12" rx="4" fill="#38bdf8" />
      <!-- Summary Bullet Items (Gạch đầu dòng tổng kết) -->
      <circle cx="52" cy="58" r="4" fill="#38bdf8" />
      <line x1="64" y1="58" x2="104" y2="58" stroke="#f1f5f9" stroke-width="3.5" stroke-linecap="round" />
      <circle cx="52" cy="76" r="4" fill="#10b981" />
      <line x1="64" y1="76" x2="108" y2="76" stroke="#f1f5f9" stroke-width="3.5" stroke-linecap="round" />
      <circle cx="52" cy="94" r="4" fill="#f59e0b" />
      <line x1="64" y1="94" x2="96" y2="94" stroke="#f1f5f9" stroke-width="3.5" stroke-linecap="round" />
      <!-- Checkmark badge (Đã tổng kết) -->
      <circle cx="102" cy="126" r="14" fill="#10b981" />
      <path d="M96 126L100 130L108 122" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />

      <!-- Speaker / Person (Người thuyết trình) -->
      <circle cx="146" cy="62" r="16" fill="#fb923c" />
      <path d="M124 116C124 96 134 86 146 86C158 86 168 96 168 116" fill="#f97316" />
      <!-- Arm pointing to summary board -->
      <path d="M132 94L110 84" stroke="#fb923c" stroke-width="4.5" stroke-linecap="round" />
      
      <!-- Podium & Mic (Bục phát biểu & Mic) -->
      <path d="M116 112L120 162H174L178 112H116Z" fill="#334155" stroke="#64748b" stroke-width="2.5" />
      <!-- Podium accent -->
      <line x1="126" y1="124" x2="168" y2="124" stroke="#f97316" stroke-width="3" stroke-linecap="round" />
      <!-- Mic -->
      <path d="M136 112L134 100" stroke="#94a3b8" stroke-width="2.5" stroke-linecap="round" />
      <ellipse cx="133" cy="97" rx="3" ry="4" fill="#e2e8f0" />
      
      <!-- Stage floor -->
      <line x1="22" y1="168" x2="178" y2="168" stroke="currentColor" stroke-opacity="0.2" stroke-width="3" stroke-linecap="round" />
    </svg>`,
    caption: 'Thuyết trình tổng kết nội dung'
  },

  // 休 (xiū - nghỉ ngơi): Người tựa gốc cây
  '休': {
    type: 'svg',
    svg: `<svg viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="100" cy="100" r="82" fill="currentColor" fill-opacity="0.04" />
      <!-- Tree (Cây - 木) -->
      <path d="M128 165V90M128 90C128 58 100 40 135 30C165 40 160 70 128 90Z" fill="#15803d" />
      <path d="M128 165V85M128 120L108 105M128 105L145 95" stroke="#854d0e" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" />
      <path d="M110 55C125 35 155 40 165 60C170 80 150 95 128 90" fill="#22c55e" fill-opacity="0.8" />
      <!-- Person resting (Người dựa cây - 人) -->
      <circle cx="82" cy="105" r="14" fill="#fb923c" />
      <path d="M72 155C72 135 84 125 96 122L120 128" stroke="#f97316" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" />
      <path d="M72 155L60 165" stroke="#f97316" stroke-width="6" stroke-linecap="round" />
      <!-- Zzz (Nghỉ ngơi) -->
      <text x="76" y="80" fill="#38bdf8" font-size="16" font-family="sans-serif" font-weight="bold">Z</text>
      <text x="88" y="70" fill="#38bdf8" font-size="20" font-family="sans-serif" font-weight="bold">z</text>
      <!-- Ground line -->
      <line x1="30" y1="168" x2="170" y2="168" stroke="currentColor" stroke-opacity="0.2" stroke-width="3" stroke-linecap="round" />
    </svg>`,
    caption: 'Người tựa gốc cây nghỉ ngơi'
  },

  // 明 (míng - sáng sủa, thông minh): Mặt trời + Mặt trăng
  '明': {
    type: 'svg',
    svg: `<svg viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="100" cy="100" r="82" fill="currentColor" fill-opacity="0.04" />
      <!-- Sun (Nhật - 日) -->
      <circle cx="68" cy="98" r="32" fill="#f59e0b" />
      <path d="M68 54V60M68 136V142M24 98H30M106 98H112M37 67L42 72M94 124L99 129M37 129L42 124M94 72L99 67" stroke="#fbbf24" stroke-width="4" stroke-linecap="round" />
      <!-- Moon (Nguyệt - 月) -->
      <path d="M125 65C105 75 105 120 135 135C110 135 95 105 110 75C114 68 120 65 125 65Z" fill="#38bdf8" />
      <circle cx="150" cy="72" r="3" fill="#e0f2fe" />
      <circle cx="162" cy="95" r="2" fill="#e0f2fe" />
      <circle cx="142" cy="115" r="2.5" fill="#e0f2fe" />
    </svg>`,
    caption: 'Mặt trời và Mặt trăng hội tụ ánh sáng'
  }
};

/**
 * Returns illustration config for a word.
 * Fallback to generic aesthetic Hanzi seal if no specific illustration is registered.
 */
function getWordIllustration(word) {
  if (!word) return null;

  // 1. Direct word.image field (URL, base64 or inline SVG)
  if (word.image) {
    if (typeof word.image === 'string' && word.image.startsWith('<svg')) {
      return { type: 'svg', svg: word.image, caption: word.meaning || '' };
    }
    return { type: 'img', src: word.image, caption: word.meaning || '' };
  }

  // 2. Preset curated illustrations
  if (WORD_ILLUSTRATIONS_DB[word.hanzi]) {
    return WORD_ILLUSTRATIONS_DB[word.hanzi];
  }

  // 3. Fallback: Elegant Minimalist Character Motif
  return generateAestheticFallback(word);
}

/**
 * Generates an aesthetic, minimalist vector motif for words without custom art.
 */
function generateAestheticFallback(word) {
  const char = (word.hanzi && word.hanzi[0]) || '字';
  return {
    type: 'svg',
    isPlaceholder: true,
    svg: `<svg viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Outer soft disc -->
      <circle cx="100" cy="100" r="78" fill="currentColor" fill-opacity="0.04" />
      <!-- Elegant inner octagonal / diamond frame -->
      <rect x="42" y="42" width="116" height="116" rx="14" stroke="currentColor" stroke-opacity="0.16" stroke-width="2" />
      <rect x="48" y="48" width="104" height="104" rx="10" stroke="#f97316" stroke-opacity="0.35" stroke-width="1.5" stroke-dasharray="6 4" />
      
      <!-- Chinese calligraphy seal backdrop -->
      <circle cx="100" cy="100" r="42" fill="#f97316" fill-opacity="0.12" />
      
      <!-- Central character silhouette -->
      <text x="100" y="118" text-anchor="middle" font-size="52" font-family="'Noto Serif SC', 'Songti SC', 'STSong', serif" font-weight="bold" fill="#f97316" fill-opacity="0.9">
        ${char}
      </text>

      <!-- Subtext / Visual Anchor -->
      <text x="100" y="180" text-anchor="middle" font-size="11" font-family="sans-serif" font-weight="600" fill="currentColor" fill-opacity="0.45" letter-spacing="1">
        MINH HỌA TỪ VỰNG
      </text>
    </svg>`,
    caption: word.meaning || 'Minh họa từ vựng'
  };
}

// Global exposure
if (typeof window !== 'undefined') {
  window.WORD_ILLUSTRATIONS_DB = WORD_ILLUSTRATIONS_DB;
  window.getWordIllustration = getWordIllustration;
}
