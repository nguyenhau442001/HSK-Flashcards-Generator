// Word and example pronunciation through prebuilt audio with Web Speech fallback.
async function loadPrebuiltAudioManifest(level) {
  prebuiltAudioManifest = null;
  const config = LEVELS[level];
  if (!config || !config.audioManifestUrl) return;

  try {
    const response = await fetch(config.audioManifestUrl, { cache: 'no-store' });
    if (!response.ok) return;
    const manifest = await response.json();
    if (currentLevel !== level || manifest.level !== level || !manifest.items) return;
    prebuiltAudioManifest = manifest;
  } catch (error) {
    // A missing or invalid manifest is expected while a level is being rolled
    // out. Individual speech requests continue through Web Speech below.
  }
}

function prebuiltAudioUrl(word, kind) {
  if (!word || !prebuiltAudioManifest || prebuiltAudioManifest.level !== currentLevel) return null;
  const item = prebuiltAudioManifest.items[String(word.id)];
  return item && typeof item[kind] === 'string' ? item[kind] : null;
}

function speakWord() {
  if (filteredOrder.length === 0) return;

  const wIdx = filteredOrder[idx % filteredOrder.length];
  const word = WORDS[wIdx];
  speakText(
    word.hanzi,
    document.getElementById('soundBtn'),
    SPEECH_RATE,
    prebuiltAudioUrl(word, 'word')
  );
}

function speakExample() {
  if (filteredOrder.length === 0) return;

  const wIdx = filteredOrder[idx % filteredOrder.length];
  const word = WORDS[wIdx];
  const example = document.getElementById('exZh');
  const text = example ? example.textContent.trim() : '';
  if (!text) return;

  speakText(
    text,
    document.getElementById('exampleSoundBtn'),
    exampleSpeechSpeed,
    prebuiltAudioUrl(word, 'example')
  );
}

function speakText(text, button, rate = SPEECH_RATE, audioUrl = null) {
  if (!button || !text) return;
  if (activeSpeechButton === button) {
    stopSpeech();
    return;
  }

  stopSpeech();
  const requestId = speechRequestId;
  const hint = document.getElementById('hint');
  const prevHint = hint ? hint.textContent : '';

  activeSpeechButton = button;
  if (audioUrl) {
    playPrebuiltAudio(text, button, rate, audioUrl, requestId, hint, prevHint);
    return;
  }
  speakWithWebSpeech(text, button, rate, requestId, hint, prevHint);
}

function playPrebuiltAudio(text, button, rate, audioUrl, requestId, hint, prevHint) {
  const audio = new Audio(audioUrl);
  activeSpeechAudio = audio;
  audio.preload = 'auto';
  audio.playbackRate = Math.min(2, Math.max(0.25, rate));
  if ('preservesPitch' in audio) audio.preservesPitch = true;

  let settled = false;
  const fallback = () => {
    if (settled || requestId !== speechRequestId) return;
    settled = true;
    audio.onplaying = null;
    audio.onended = null;
    audio.onerror = null;
    audio.pause();
    if (activeSpeechAudio === audio) activeSpeechAudio = null;
    speakWithWebSpeech(text, button, rate, requestId, hint, prevHint);
  };

  audio.onplaying = () => {
    if (requestId !== speechRequestId) return;
    setSpeechButtonState(button, true, text);
  };
  audio.onended = () => {
    if (settled || requestId !== speechRequestId) return;
    settled = true;
    if (activeSpeechAudio === audio) activeSpeechAudio = null;
    setSpeechButtonState(button, false);
  };
  audio.onerror = fallback;

  const playPromise = audio.play();
  if (playPromise && typeof playPromise.catch === 'function') playPromise.catch(fallback);
}

function speakWithWebSpeech(text, button, rate, requestId, hint, prevHint) {
  if (requestId !== speechRequestId) return;
  if (!('speechSynthesis' in window) || typeof SpeechSynthesisUtterance === 'undefined') {
    setSpeechButtonState(button, false);
    showSpeechHint(hint, 'Trình duyệt này không hỗ trợ phát âm, hãy mở bằng Chrome hoặc Safari', prevHint);
    return;
  }

  activeSpeechButton = button;
  const attempt = (voice, isRetry) => {
    if (requestId !== speechRequestId) return;

    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = 'zh-CN';
    utter.rate = rate;
    if (voice) utter.voice = voice;

    let spoke = false;
    let settled = false;
    let startTimer = null;

    const fail = () => {
      if (settled || requestId !== speechRequestId) return;
      settled = true;
      if (startTimer) clearTimeout(startTimer);
      if (!isRetry) { attempt(null, true); return; }
      setSpeechButtonState(button, false);
      showSpeechHint(hint, 'Không thể phát âm trên trình duyệt này', prevHint);
    };

    utter.onstart = () => {
      if (requestId !== speechRequestId) return;
      spoke = true;
      setSpeechButtonState(button, true, text);
    };
    utter.onend = () => {
      if (settled || requestId !== speechRequestId) return;
      settled = true;
      if (startTimer) clearTimeout(startTimer);
      setSpeechButtonState(button, false);
    };
    utter.onerror = fail;

    startTimer = setTimeout(() => {
      if (spoke || speechSynthesis.speaking || requestId !== speechRequestId) return;
      if (!isRetry) {
        settled = true;
        attempt(null, true);
        return;
      }
      settled = true;
      setSpeechButtonState(button, false);
      showSpeechHint(hint, 'Không thể phát âm, hãy thử mở bằng Chrome hoặc Safari', prevHint);
    }, 800);

    if (speechSynthesis.speaking || speechSynthesis.pending) speechSynthesis.cancel();
    speechSynthesis.speak(utter);
  };

  attempt(pickChineseVoice(), false);
}

function showSpeechHint(hint, message, previousMessage) {
  if (!hint) return;
  hint.textContent = message;
  setTimeout(() => {
    if (hint.textContent === message) hint.textContent = previousMessage;
  }, 2500);
}

function setSpeechButtonState(button, isPlaying, text) {
  if (!button) return;
  const isExample = button.classList.contains('example-sound-btn');

  button.classList.toggle('is-playing', isPlaying);
  button.setAttribute('aria-pressed', String(isPlaying));
  button.setAttribute(
    'aria-label',
    isPlaying
      ? (isExample ? 'Đang phát câu ví dụ' : `Đang phát âm ${text || ''}`.trim())
      : (isExample ? 'Nghe câu ví dụ' : 'Nghe phát âm')
  );
  button.title = isPlaying ? 'Bấm để dừng' : (isExample ? 'Nghe câu ví dụ' : 'Nghe phát âm');

  if (isPlaying) activeSpeechButton = button;
  else if (activeSpeechButton === button) activeSpeechButton = null;
}

function stopSpeech() {
  speechRequestId++;
  if (activeSpeechAudio) {
    const audio = activeSpeechAudio;
    activeSpeechAudio = null;
    audio.onplaying = null;
    audio.onended = null;
    audio.onerror = null;
    audio.pause();
    try { audio.currentTime = 0; } catch (error) {}
  }
  if ('speechSynthesis' in window && (speechSynthesis.speaking || speechSynthesis.pending)) {
    speechSynthesis.cancel();
  }
  if (activeSpeechButton) setSpeechButtonState(activeSpeechButton, false);
}
