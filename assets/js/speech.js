// Word and example pronunciation through the Web Speech API.
function speakWord() {
  if (filteredOrder.length === 0) return;

  const wIdx = filteredOrder[idx % filteredOrder.length];
  speakText(WORDS[wIdx].hanzi, document.getElementById('soundBtn'));
}

function speakExample() {
  if (filteredOrder.length === 0) return;

  const example = document.getElementById('exZh');
  const text = example ? example.textContent.trim() : '';
  if (!text) return;

  const browserRate = Math.max(0.1, exampleSpeechSpeed - EXAMPLE_SPEECH_RATE_OFFSET);
  speakText(text, document.getElementById('exampleSoundBtn'), browserRate);
}

function speakText(text, button, rate = SPEECH_RATE) {
  if (!button || !text) return;
  if (button.classList.contains('is-playing')) {
    stopSpeech();
    return;
  }

  stopSpeech();

  const hint = document.getElementById('hint');
  const prevHint = hint.textContent;

  if (!('speechSynthesis' in window) || typeof SpeechSynthesisUtterance === 'undefined') {
    hint.textContent = 'Trình duyệt này không hỗ trợ phát âm, hãy mở bằng Chrome hoặc Safari';
    setTimeout(() => { hint.textContent = prevHint; }, 2500);
    return;
  }

  const requestId = speechRequestId;
  setSpeechButtonState(button, true, text);

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
      hint.textContent = 'Không thể phát âm trên trình duyệt này';
      setTimeout(() => { hint.textContent = prevHint; }, 2500);
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
      hint.textContent = 'Không thể phát âm, hãy thử mở bằng Chrome hoặc Safari';
      setTimeout(() => { hint.textContent = prevHint; }, 2500);
    }, 800);

    if (speechSynthesis.speaking || speechSynthesis.pending) speechSynthesis.cancel();
    speechSynthesis.speak(utter);
  };

  attempt(pickChineseVoice(), false);
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
  if ('speechSynthesis' in window && (speechSynthesis.speaking || speechSynthesis.pending)) {
    speechSynthesis.cancel();
  }
  if (activeSpeechButton) setSpeechButtonState(activeSpeechButton, false);
}
