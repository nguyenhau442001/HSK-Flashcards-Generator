// Shared application configuration and in-memory state.
const LEVELS = {
  hsk1: {
    label: 'HSK1',
    dataUrl: 'database/vocabs/hsk1_vocabularies.json',
    audioManifestUrl: 'database/prebuilt_audio/hsk1/manifest.json',
    available: true,
    total: 150,
  },
  hsk2: {
    label: 'HSK2',
    dataUrl: 'database/vocabs/hsk2_vocabularies.json',
    audioManifestUrl: 'database/prebuilt_audio/hsk2/manifest.json',
    available: true,
    total: 150,
  },
  hsk3: { label: 'HSK3', dataUrl: 'database/vocabs/hsk3_vocabularies.json', available: true, total: 300 },
  hsk4: { label: 'HSK4', dataUrl: 'database/vocabs/hsk4_vocabularies.json', available: true, total: 600 },
  hsk5: { label: 'HSK5', dataUrl: 'database/vocabs/hsk5_vocabularies.json', available: true, total: 1300 },
  hsk6: { label: 'HSK6', dataUrl: 'database/vocabs/hsk6_vocabularies.json', available: true, total: 2500 },
};

// Topic decks: same word schema as LEVELS, browsed from the "Chủ đề" tab.
// Keys are prefixed 'topic_' and merged into LEVELS so every existing
// LEVELS[currentLevel] lookup (speech, overview, progress, backup) works unmodified.
const TOPICS = {
  topic_it: { label: 'Công nghệ thông tin', icon: '💻', dataUrl: 'database/vocabs/topics/it.json', available: true, total: 60, isTopic: true },
};
Object.assign(LEVELS, TOPICS);

function hskLevelKeys() {
  return Object.keys(LEVELS).filter(key => !TOPICS[key]);
}
const SPEECH_RATE = 0.85;
const EXAMPLE_SPEECH_SPEEDS = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2];
const DEFAULT_EXAMPLE_SPEECH_SPEED = 1;

let currentLevel = null;
let WORDS = [];
let order = [];
let filteredOrder = [];
let idx = 0;
let progress = {};
let showPinyin = true;
let currentFilter = 'all';
let transitionTimer = null;
let celebrationShown = false;
let cachedVoices = [];
let speechRequestId = 0;
let activeSpeechButton = null;
let activeSpeechAudio = null;
let prebuiltAudioManifest = null;
let exampleSpeechSpeed = DEFAULT_EXAMPLE_SPEECH_SPEED;
let currentView = 'cards';
let overviewQuery = '';
let overviewStatus = 'all';
let reviewPool = [];
let reviewIndex = 0;
let reviewLives = 3;
let reviewScore = 0;
let reviewStreak = 0;
let reviewBestStreak = 0;
let reviewTimer = null;
let reviewTimeLeft = 20;
let reviewCurrentQuestion = null;
let reviewAnswered = false;
let reviewSessionLive = false;
let reviewWordPool = [];
let reviewProgressByLevel = {};
let reviewLoadedRangeMax = 0;
let reviewWorker = null;

function formatExampleSpeechSpeed(speed) {
  const numericSpeed = Number(speed);
  return `${Number.isInteger(numericSpeed) ? numericSpeed.toFixed(1) : numericSpeed} x`;
}

function setExampleSpeechSpeed(value) {
  const nextSpeed = Number(value);
  if (!EXAMPLE_SPEECH_SPEEDS.includes(nextSpeed)) return;

  exampleSpeechSpeed = nextSpeed;
  stopSpeech();

  const currentSpeed = document.getElementById('exampleCurrentSpeed');
  if (currentSpeed) currentSpeed.textContent = formatExampleSpeechSpeed(nextSpeed);
  const speedSummary = document.querySelector('#exampleSpeedPicker summary');
  if (speedSummary) {
    speedSummary.setAttribute('aria-label', `Tốc độ đọc câu ví dụ: ${formatExampleSpeechSpeed(nextSpeed)}`);
  }
  document.querySelectorAll('.example-speed-option').forEach(option => {
    const isSelected = Number(option.dataset.speed) === nextSpeed;
    option.classList.toggle('selected', isSelected);
    option.setAttribute('aria-pressed', String(isSelected));
  });

  const speedPicker = document.getElementById('exampleSpeedPicker');
  if (speedPicker) speedPicker.open = false;
}

function pickChineseVoice() {
  if (!('speechSynthesis' in window)) return null;
  if (!cachedVoices.length) cachedVoices = speechSynthesis.getVoices();
  return cachedVoices.find(v => v.lang === 'zh-CN')
    || cachedVoices.find(v => v.lang && v.lang.toLowerCase().startsWith('zh'))
    || null;
}
if ('speechSynthesis' in window) {
  cachedVoices = speechSynthesis.getVoices();
  speechSynthesis.onvoiceschanged = () => { cachedVoices = speechSynthesis.getVoices(); };
}

let speechWarmed = false;
function warmUpSpeech() {
  if (speechWarmed || !('speechSynthesis' in window)) return;
  speechWarmed = true;
  try {
    const warmUp = new SpeechSynthesisUtterance('');
    warmUp.volume = 0;
    speechSynthesis.speak(warmUp);
  } catch (e) {}
}
document.addEventListener('touchstart', warmUpSpeech, { once: true, passive: true });
document.addEventListener('click', warmUpSpeech, { once: true });

function storageKey(suffix) {
  return 'hsk_' + currentLevel + '_' + suffix + '_v2';
}
