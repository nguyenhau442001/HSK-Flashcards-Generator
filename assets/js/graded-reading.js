/**
 * assets/js/graded-reading.js
 * Synapse Graded Reading (HSK Reading Stories) Core Engine
 * Closed-Loop Learning: Reading -> Click-to-Inspect -> SRS Integration -> Review
 */

const GradedReading = (function() {
  let manifest = [];
  let manifestLoaded = false;
  let activeStory = null;
  let storyCache = {};
  let currentLevelFilter = 'all';
  let activePopover = null;
  let quizState = {};

  // Display Preferences
  let prefs = {
    showPinyin: true,
    showTranslation: true,
    showSrsHighlights: true
  };

  try {
    const saved = localStorage.getItem('synapse_graded_prefs_v1');
    if (saved) prefs = Object.assign(prefs, JSON.parse(saved));
  } catch (e) {}

  function savePrefs() {
    try {
      localStorage.setItem('synapse_graded_prefs_v1', JSON.stringify(prefs));
    } catch (e) {}
  }

  // Read Stories Tracking
  const READ_STORIES_STORAGE_KEY = 'synapse_graded_read_stories_v1';
  let readStories = {};

  try {
    const savedRead = localStorage.getItem(READ_STORIES_STORAGE_KEY);
    if (savedRead) readStories = JSON.parse(savedRead) || {};
  } catch (e) {
    readStories = {};
  }

  function saveReadStories() {
    try {
      localStorage.setItem(READ_STORIES_STORAGE_KEY, JSON.stringify(readStories));
    } catch (e) {}
  }

  function isStoryRead(storyId) {
    return Boolean(readStories[storyId]);
  }

  function markStoryAsRead(storyId) {
    if (!storyId) return;
    readStories[storyId] = {
      readAt: new Date().toISOString()
    };
    saveReadStories();
  }

  function unmarkStoryAsRead(storyId) {
    if (!storyId) return;
    delete readStories[storyId];
    saveReadStories();
  }

  function toggleStoryRead(storyId, event) {
    if (event) {
      if (typeof event.preventDefault === 'function') event.preventDefault();
      if (typeof event.stopPropagation === 'function') event.stopPropagation();
    }
    if (!storyId) return;
    if (isStoryRead(storyId)) {
      unmarkStoryAsRead(storyId);
    } else {
      markStoryAsRead(storyId);
    }

    if (!activeStory) {
      renderHub();
    } else {
      updateStoryReadUI();
    }
  }

  function toggleCurrentStoryRead() {
    if (!activeStory) return;
    toggleStoryRead(activeStory.id);
  }

  function updateStoryReadUI() {
    if (!activeStory) return;
    const isRead = isStoryRead(activeStory.id);

    const navBtn = document.getElementById('toggleReadStoryBtn');
    if (navBtn) {
      navBtn.classList.toggle('active', isRead);
      navBtn.classList.toggle('read-active', isRead);
      navBtn.innerHTML = isRead
        ? `<span>✓ Đã đọc</span>`
        : `<span>○ Đánh dấu đã đọc</span>`;
      navBtn.title = isRead ? 'Đã đọc (Bấm để hủy đánh dấu)' : 'Đánh dấu đã đọc bài này';
    }

    const compCard = document.getElementById('storyCompletionCard');
    if (compCard) {
      compCard.classList.toggle('completed', isRead);
      const icon = compCard.querySelector('.completion-icon-box');
      if (icon) icon.textContent = isRead ? '🎉' : '📖';
      const heading = compCard.querySelector('.completion-heading');
      if (heading) heading.textContent = isRead ? 'Đã hoàn thành bài đọc!' : 'Hoàn thành bài đọc này?';
      const sub = compCard.querySelector('.completion-sub');
      if (sub) sub.textContent = isRead ? 'Bài viết đã được lưu vào danh sách Đã đọc của bạn.' : 'Đánh dấu đã đọc để lưu tiến trình và theo dõi lộ trình học tập.';
      const ctaBtn = compCard.querySelector('.graded-completion-btn');
      if (ctaBtn) {
        ctaBtn.classList.toggle('active', isRead);
        ctaBtn.textContent = isRead ? '✓ Đã hoàn thành (Bấm để hủy)' : '✓ Đánh dấu đã đọc';
      }
    }
  }

  /**
   * Determine user's SRS memory state for a given token
   * Returns: 'mastered' | 'learning' | 'new'
   */
  function getTokenSrsStatus(token) {
    if (!token || !token.word_id) return 'none';
    const match = token.word_id.match(/^hsk(\d+)_(\d+)$/i);
    if (!match) return 'none';
    const level = match[1];
    const rawId = match[2];

    try {
      if (typeof readSrsRecord === 'function') {
        const record = readSrsRecord(level);
        if (record && record.cards) {
          const card = record.cards[String(rawId)];
          if (card) {
            if (card.state === 2 || card.status === 'known' || (card.reps && card.reps >= 2)) {
              return 'mastered';
            }
            if (card.state === 1 || card.state === 3 || (card.reps && card.reps > 0)) {
              return 'learning';
            }
          }
        }
      }
    } catch (e) {
      console.warn('SRS lookup error:', e);
    }
    return 'new';
  }

  /**
   * Add a token word directly into the user's FSRS queue for today
   */
  function addTokenToSrs(token) {
    if (!token || !token.word_id) return false;
    const match = token.word_id.match(/^hsk(\d+)_(\d+)$/i);
    if (!match) return false;
    const level = match[1];
    const rawId = match[2];

    try {
      if (typeof readSrsRecord === 'function' && typeof saveSrsRecord === 'function') {
        const record = readSrsRecord(level) || { schemaVersion: 3, cards: {} };
        if (!record.cards) record.cards = {};
        
        let card = record.cards[String(rawId)];
        if (!card) {
          card = (typeof SRS !== 'undefined' && SRS.createNewCard) ? SRS.createNewCard() : { state: 0, reps: 0 };
        }
        card.state = 1; // Learning state
        card.status = 'unknown';
        card.due = new Date().toISOString();
        card.last_rating = 'again';
        
        record.cards[String(rawId)] = card;
        saveSrsRecord(level, record.cards, false);

        // Update active in-memory SRS cache if matching current selected level
        if (typeof currentLevel !== 'undefined' && String(currentLevel) === String(level)) {
          if (typeof srsCards !== 'undefined' && srsCards) {
            srsCards[String(rawId)] = card;
          }
        }

        // Live update all matching tokens on screen to learning status
        document.querySelectorAll(`[data-word-id="${token.word_id}"]`).forEach(el => {
          el.classList.remove('token-new');
          el.classList.add('token-learning');
        });

        return true;
      }
    } catch (e) {
      console.error('Failed to add token to SRS:', e);
    }
    return false;
  }

  /**
   * Load manifest of all available stories
   */
  async function ensureManifestLoaded() {
    if (manifestLoaded && manifest.length) return manifest;
    try {
      const res = await fetch('database/readings/manifest.json?v=' + Date.now());
      if (!res.ok) throw new Error('Không thể tải danh sách bài đọc.');
      manifest = await res.json();
      manifestLoaded = true;
      return manifest;
    } catch (e) {
      console.error('GradedReading manifest error:', e);
      return [];
    }
  }

  /**
   * Load single story data
   */
  async function loadStory(storyId) {
    if (storyCache[storyId]) return storyCache[storyId];
    const item = manifest.find(m => m.id === storyId);
    if (!item) throw new Error('Không tìm thấy bài đọc: ' + storyId);
    const storyUrl = item.file || item.path || `database/readings/${(item.level || '').toLowerCase()}/${item.id}.json`;
    const res = await fetch(storyUrl);
    if (!res.ok) throw new Error('Không thể tải nội dung bài: ' + storyUrl);
    const data = await res.json();
    storyCache[storyId] = data;
    return data;
  }

  let escapeListenerBound = false;

  /**
   * Main entry point
   */
  async function init() {
    const mount = document.getElementById('screenGradedReading');
    if (!mount) return;
    document.body.classList.add('graded-reading-active');

    if (!escapeListenerBound) {
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          if (activePopover) {
            closePopover();
          } else if (activeStory) {
            goBackToHub();
          }
        }
      });
      escapeListenerBound = true;
    }

    // Check URL parameter for direct story link
    const params = new URLSearchParams(window.location.search);
    const storyParam = params.get('story');

    await ensureManifestLoaded();

    if (storyParam) {
      await openStory(storyParam, false);
    } else {
      renderHub();
    }
  }

  /**
   * Return back to reading hub and sync URL
   */
  function goBackToHub() {
    activeStory = null;
    closePopover();
    document.body.classList.remove('graded-story-active');
    if (typeof SpaRouter !== 'undefined') {
      SpaRouter.pushView({ view: 'tab', tab: 'gradedReading' }, `${window.location.pathname}?tab=gradedReading`);
    } else {
      window.history.pushState({}, '', `${window.location.pathname}?tab=gradedReading`);
    }
    renderHub();
  }

  /**
   * Render Reading Hub
   */
  function renderHub() {
    activeStory = null;
    closePopover();
    document.body.classList.remove('graded-story-active');
    const mount = document.getElementById('screenGradedReading');
    if (!mount) return;

    // Apply preference classes
    document.body.classList.remove('graded-pinyin-hidden', 'graded-translation-hidden');

    const readCount = manifest.filter(m => isStoryRead(m.id)).length;
    const progressPercent = manifest.length ? Math.round((readCount / manifest.length) * 100) : 0;

    let filtered = manifest;
    if (currentLevelFilter === 'read') {
      filtered = manifest.filter(m => isStoryRead(m.id));
    } else if (currentLevelFilter !== 'all') {
      filtered = manifest.filter(m => m.level.toLowerCase() === currentLevelFilter.toLowerCase());
    }

    const levels = ['HSK1', 'HSK2', 'HSK3', 'HSK4', 'HSK5', 'HSK6', 'HSK7', 'HSK8', 'HSK9'];
    const levelCounts = {};
    levels.forEach(lvl => {
      levelCounts[lvl] = manifest.filter(m => m.level.toUpperCase() === lvl).length;
    });

    mount.innerHTML = `
      <div class="graded-reading-container">
        <!-- Back to Vocab Hub Bar -->
        <div style="display: flex; align-items: center; justify-content: flex-start; margin-bottom: 16px;">
          <button type="button" class="graded-back-btn" onclick="setPrimaryTab('vocab')" title="Quay lại Hub Từ vựng">
            ← Quay lại Hub Từ vựng
          </button>
        </div>

        <!-- Hero Header -->
        <header class="graded-hub-hero">
          <div class="graded-hub-badge">📚 Graded Reading</div>
          <h1 class="graded-hub-title">Synapse Graded Reading</h1>
          <p class="graded-hub-subtitle">
            Luyện đọc hiểu phân cấp theo ngữ cảnh thực tế · Vòng lặp học từ khép kín · Nhận diện vốn từ SRS cá nhân
          </p>
          <div class="graded-hub-progress-wrap">
            <div class="graded-hub-progress-bar">
              <div class="graded-hub-progress-fill" style="width: ${progressPercent}%;"></div>
            </div>
            <div class="graded-hub-progress-meta">
              <span>Tiến độ đọc: <strong>${readCount}/${manifest.length}</strong> bài (${progressPercent}%)</span>
            </div>
          </div>
        </header>

        <!-- Filter Pills -->
        <nav class="graded-hub-filters" aria-label="Bộ lọc cấp độ HSK">
          <button type="button" class="graded-filter-pill ${currentLevelFilter === 'all' ? 'active' : ''}" onclick="GradedReading.setLevelFilter('all')">
            Tất cả (${manifest.length})
          </button>
          <button type="button" class="graded-filter-pill ${currentLevelFilter === 'read' ? 'active' : ''} ${readCount === 0 ? 'disabled' : ''}" onclick="GradedReading.setLevelFilter('read')" title="Xem bài đã đọc">
            ✓ Đã đọc (${readCount})
          </button>
          ${levels.map(lvl => {
            const count = levelCounts[lvl] || 0;
            const lvlDisplay = lvl.replace('HSK', 'HSK ');
            const lvlReadCount = manifest.filter(m => m.level.toUpperCase() === lvl && isStoryRead(m.id)).length;
            if (count > 0) {
              const readTag = lvlReadCount > 0 ? ` · ${lvlReadCount}✓` : '';
              return `
                <button type="button" class="graded-filter-pill ${currentLevelFilter === lvl ? 'active' : ''}" onclick="GradedReading.setLevelFilter('${lvl}')">
                  ${lvlDisplay} (${count} bài${readTag})
                </button>
              `;
            } else {
              return `
                <button type="button" class="graded-filter-pill disabled" title="Đang cập nhật thêm bài đọc">
                  ${lvlDisplay} (Sắp có)
                </button>
              `;
            }
          }).join('')}
        </nav>

        <!-- Stories Grid -->
        <div class="graded-stories-grid">
          ${filtered.length === 0 ? `
            <div class="graded-empty-state">
              <span style="font-size: 2.2rem;">📖</span>
              <div style="font-weight: 700; font-size: 1.05rem; margin-top: 10px; color: var(--graded-text-primary);">
                ${currentLevelFilter === 'read' ? 'Bạn chưa đánh dấu bài đọc nào' : 'Không có bài đọc nào phù hợp'}
              </div>
              <p style="color: var(--graded-text-secondary); font-size: 0.88rem; max-width: 480px; margin: 6px auto 16px;">
                ${currentLevelFilter === 'read' ? 'Hãy mở một bài đọc và bấm "Đánh dấu đã đọc" sau khi đọc xong, hoặc bấm nút tích trên thẻ bài đọc.' : 'Vui lòng chọn cấp độ khác.'}
              </p>
              <button type="button" class="graded-filter-pill active" onclick="GradedReading.setLevelFilter('all')">Xem tất cả bài đọc</button>
            </div>
          ` : filtered.map(story => {
            const isRead = isStoryRead(story.id);
            return `
            <article class="graded-story-card ${isRead ? 'is-read' : ''}" onclick="GradedReading.openStory('${story.id}')" tabindex="0" role="button" aria-label="Đọc bài ${story.title.vi}">
              <div>
                <div class="graded-card-header">
                  <div style="display: flex; align-items: center; gap: 6px;">
                    <span class="graded-card-level-badge">${story.level}</span>
                    ${isRead ? `
                      <span class="graded-card-read-badge" title="Đã hoàn thành bài đọc">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        Đã đọc
                      </span>
                    ` : ''}
                  </div>
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <span class="graded-card-topic">${story.topic_vi}</span>
                    <span class="graded-card-time">⏱️ ${story.estimatedMinutes}m</span>
                    <button type="button" class="graded-card-mark-toggle ${isRead ? 'read' : ''}" onclick="GradedReading.toggleStoryRead('${story.id}', event)" title="${isRead ? 'Bỏ đánh dấu đã đọc' : 'Đánh dấu đã đọc'}" aria-label="${isRead ? 'Bỏ đánh dấu đã đọc' : 'Đánh dấu đã đọc'}">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="${isRead ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                    </button>
                  </div>
                </div>
                <div class="graded-card-body">
                  <h2 class="graded-card-zh-title">
                    <span>${story.icon || '📖'}</span>
                    <span>${story.title.zh}</span>
                  </h2>
                  <div class="graded-card-vi-title">${story.title.vi}</div>
                  <p class="graded-card-desc">${story.description_vi}</p>
                </div>
              </div>
              <footer class="graded-card-footer">
                <span class="graded-card-meta-text">${story.sentence_count ?? story.sentences_count ?? 5} câu · ${story.spotlight_count ?? 10} từ</span>
                <span class="graded-card-read-btn ${isRead ? 'read' : ''}">
                  ${isRead ? 'Đọc lại →' : 'Đọc ngay →'}
                </span>
              </footer>
            </article>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }

  /**
   * Open and render interactive story reader
   */
  async function openStory(storyId, updateUrl = true) {
    const mount = document.getElementById('screenGradedReading');
    if (!mount) return;

    mount.innerHTML = `
      <div class="graded-reading-container" style="text-align: center; padding: 60px 0;">
        <div style="font-size: 1.5rem; margin-bottom: 12px;">📖</div>
        <div style="color: var(--text-secondary);">Đang tải bài đọc...</div>
      </div>
    `;

    try {
      const story = await loadStory(storyId);
      activeStory = story;
      quizState = {};

      if (updateUrl && typeof SpaRouter !== 'undefined') {
        SpaRouter.pushView({ view: 'tab', tab: 'gradedReading', story: storyId }, `${window.location.pathname}?tab=gradedReading&story=${storyId}`);
      }

      renderStoryView(story);
    } catch (e) {
      mount.innerHTML = `
        <div class="graded-reading-container" style="text-align: center; padding: 60px 0;">
          <div style="color: #ef4444; font-weight: 700; margin-bottom: 12px;">Đã xảy ra lỗi</div>
          <p style="color: var(--text-secondary);">${e.message}</p>
          <button type="button" class="graded-back-btn" style="margin: 16px auto;" onclick="GradedReading.goBackToHub()">← Trở về danh sách</button>
        </div>
      `;
    }
  }

  /**
   * Render Interactive Story Reader View
   */
  function renderStoryView(story) {
    const mount = document.getElementById('screenGradedReading');
    if (!mount) return;

    document.body.classList.add('graded-story-active');

    // Apply initial toggle preference classes
    document.body.classList.toggle('graded-pinyin-hidden', !prefs.showPinyin);
    document.body.classList.toggle('graded-translation-hidden', !prefs.showTranslation);

    const storyLvlNum = parseInt(story.level.replace(/\D/g, '') || '1', 10);
    const isRead = isStoryRead(story.id);

    mount.innerHTML = `
      <div class="graded-reading-container graded-reader-shell">
        <!-- Navigation & Toggles Bar -->
        <header class="graded-reader-nav">
          <button type="button" class="graded-back-btn" onclick="GradedReading.goBackToHub()" title="Trở về danh sách bài đọc (Esc)">
            ← Hub bài đọc
          </button>

          <div class="graded-reader-title-group">
            <h1 class="graded-reader-zh-title">
              <span>${story.title.zh}</span>
              <span class="graded-card-level-badge">${story.level}</span>
            </h1>
            <div class="graded-reader-vi-title">${story.title.vi} · ⏱️ ${story.estimatedMinutes} phút</div>
          </div>

          <div class="graded-reader-actions">
            <button type="button" id="toggleReadStoryBtn" class="graded-toggle-btn ${isRead ? 'active read-active' : ''}" onclick="GradedReading.toggleCurrentStoryRead()" title="${isRead ? 'Đã đọc (Bấm để hủy đánh dấu)' : 'Đánh dấu đã đọc bài này'}">
              ${isRead ? '<span>✓ Đã đọc</span>' : '<span>○ Đánh dấu đã đọc</span>'}
            </button>
            <button type="button" id="togglePinyinBtn" class="graded-toggle-btn ${prefs.showPinyin ? 'active' : ''}" onclick="GradedReading.togglePinyin()" title="Bật/Tắt phiên âm Pinyin">
              拼 Pinyin
            </button>
            <button type="button" id="toggleTransBtn" class="graded-toggle-btn ${prefs.showTranslation ? 'active' : ''}" onclick="GradedReading.toggleTranslation()" title="Bật/Tắt bản dịch tiếng Việt">
              🇻🇳 Dịch
            </button>
          </div>
        </header>

        <!-- SRS Highlighting Legend Bar -->
        <div class="graded-srs-legend-bar" aria-label="Chú giải trạng thái từ vựng">
          <span style="font-weight: 700; color: var(--text-secondary);">Vốn từ cá nhân:</span>
          <div class="graded-legend-item">
            <span class="legend-swatch mastered"></span>
            <span>Đã thuộc</span>
          </div>
          <div class="graded-legend-item">
            <span class="legend-swatch learning"></span>
            <span>Đang học (SRS)</span>
          </div>
          <div class="graded-legend-item">
            <span class="legend-swatch new"></span>
            <span>Từ mới</span>
          </div>
          <div class="graded-legend-item">
            <span class="legend-swatch overlevel"></span>
            <span>Vượt cấp (+1)</span>
          </div>
        </div>

        <!-- Main Story Reader Card -->
        <main class="graded-passage-card">
          <div class="graded-sentence-stream">
            ${story.sentences.map((sentence, sidx) => `
              <div class="graded-sentence-block" id="sent-${sentence.id}">
                <div class="graded-sentence-zh">
                  ${sentence.tokens.map((token, tidx) => renderTokenHtml(token, sidx, tidx, storyLvlNum)).join('')}
                </div>
                <div class="graded-sentence-vi">${sentence.vi}</div>
              </div>
            `).join('')}
          </div>
        </main>

        <!-- Vocabulary Spotlight Section -->
        <section class="graded-section-card">
          <h2 class="graded-section-title">
            <span>⭐</span>
            <span>Từ vựng trọng tâm trong bài (${story.vocabulary_spotlight.length} từ)</span>
          </h2>
          <div class="graded-spotlight-grid">
            ${renderSpotlightItems(story)}
          </div>
        </section>

        <!-- Comprehension Quiz Section -->
        <section class="graded-section-card">
          <h2 class="graded-section-title">
            <span>📝</span>
            <span>Kiểm tra đọc hiểu (${story.quiz.length} câu)</span>
          </h2>
          <div class="graded-quiz-container">
            ${story.quiz.map((q, qidx) => `
              <div class="graded-quiz-item" id="quiz-${q.id}">
                <div class="graded-quiz-question">Câu ${qidx + 1}: ${q.question_vi}</div>
                <div class="graded-quiz-options">
                  ${q.options_vi.map((opt, oidx) => `
                    <button type="button" class="graded-quiz-opt-btn" onclick="GradedReading.answerQuiz('${q.id}', ${oidx})">
                      <span style="font-weight: 700; color: var(--text-secondary);">${String.fromCharCode(65 + oidx)}.</span>
                      <span>${opt}</span>
                    </button>
                  `).join('')}
                </div>
                <div class="graded-quiz-explanation" id="quiz-exp-${q.id}" style="display:none;"></div>
              </div>
            `).join('')}
          </div>
        </section>

        <!-- Story Completion Section -->
        <section class="graded-completion-card ${isRead ? 'completed' : ''}" id="storyCompletionCard">
          <div class="completion-icon-box">${isRead ? '🎉' : '📖'}</div>
          <div class="completion-content">
            <h3 class="completion-heading">${isRead ? 'Đã hoàn thành bài đọc!' : 'Hoàn thành bài đọc này?'}</h3>
            <p class="completion-sub">${isRead ? 'Bài viết đã được lưu vào danh sách Đã đọc của bạn.' : 'Đánh dấu đã đọc để lưu tiến trình và theo dõi lộ trình học tập.'}</p>
          </div>
          <button type="button" class="graded-completion-btn ${isRead ? 'active' : ''}" onclick="GradedReading.toggleCurrentStoryRead()">
            ${isRead ? '✓ Đã hoàn thành (Bấm để hủy)' : '✓ Đánh dấu đã đọc'}
          </button>
        </section>
      </div>
    `;
  }

  /**
   * Render individual token inside sentence
   */
  function renderTokenHtml(token, sidx, tidx, storyLvlNum) {
    const isPunct = /^[，。？！、：；“”‘’（）…—《》\s]+$/.test(token.text);
    if (isPunct) {
      return `<span class="graded-punctuation">${token.text}</span>`;
    }

    const srsStatus = getTokenSrsStatus(token);
    const tokenLvl = token.hsk || 1;
    const isOverLevel = Boolean(token.word_id && tokenLvl > storyLvlNum);
    const overLevelBadge = isOverLevel ? `<span class="token-overlevel-badge">+${tokenLvl - storyLvlNum}</span>` : '';

    const srsClass = srsStatus !== 'none' ? `token-${srsStatus}` : '';
    const overClass = isOverLevel ? 'token-overlevel' : '';

    return `
      <span class="graded-token ${srsClass} ${overClass}"
            data-sidx="${sidx}"
            data-tidx="${tidx}"
            data-word-id="${token.word_id || ''}"
            onclick="GradedReading.handleTokenClick(event, ${sidx}, ${tidx})"
            title="Bấm để xem nghĩa & thêm vào SRS">
        <ruby>
          <rt class="token-pinyin">${token.pinyin || ''}</rt>
          <rb>${token.text}</rb>
        </ruby>${overLevelBadge}
      </span>
    `;
  }

  /**
   * Render Vocabulary Spotlight Items
   */
  function renderSpotlightItems(story) {
    const wordsById = {};
    story.sentences.forEach(s => {
      s.tokens.forEach(tok => {
        if (tok.word_id && !wordsById[tok.word_id]) {
          wordsById[tok.word_id] = tok;
        }
      });
    });

    return story.vocabulary_spotlight.map(wid => {
      const tok = wordsById[wid];
      if (!tok) return '';
      const srsStatus = getTokenSrsStatus(tok);
      const statusLabel = srsStatus === 'mastered' ? 'Đã nhớ' : (srsStatus === 'learning' ? 'Đang ôn' : 'Từ mới');
      const statusClass = srsStatus;

      return `
        <div class="graded-spotlight-item" onclick="GradedReading.inspectByWordId('${wid}', event)">
          <div class="spotlight-top">
            <span class="spotlight-hz">${tok.text}</span>
            <span class="spotlight-py">${tok.pinyin}</span>
          </div>
          <div class="spotlight-vi">${tok.meaning_vi}</div>
          <div style="margin-top: 4px;">
            <span class="popover-srs-status ${statusClass}">${statusLabel}</span>
          </div>
        </div>
      `;
    }).join('');
  }

  /**
   * Handle Click-to-Inspect Token Popover
   */
  function handleTokenClick(event, sidx, tidx) {
    event.stopPropagation();
    if (!activeStory) return;
    const sentence = activeStory.sentences[sidx];
    if (!sentence) return;
    const token = sentence.tokens[tidx];
    if (!token || (!token.word_id && !token.is_name)) return;

    showTokenPopover(token, event.currentTarget);
  }

  function inspectByWordId(wid, event) {
    if (event) event.stopPropagation();
    if (!activeStory) return;
    for (const s of activeStory.sentences) {
      for (const tok of s.tokens) {
        if (tok.word_id === wid) {
          showTokenPopover(tok, event ? event.currentTarget : null);
          return;
        }
      }
    }
  }

  /**
   * Show Token Popover
   */
  function showTokenPopover(token, targetEl) {
    closePopover();

    const popover = document.createElement('div');
    popover.id = 'gradedTokenPopover';
    popover.className = 'graded-token-popover';

    const srsStatus = getTokenSrsStatus(token);
    const statusLabel = srsStatus === 'mastered' ? '✓ Đã thuộc' : (srsStatus === 'learning' ? '⚡ Đang học' : '✨ Từ mới');
    const isAlreadyInSrs = srsStatus === 'mastered' || srsStatus === 'learning';

    popover.innerHTML = `
      <div class="popover-header">
        <div class="popover-hanzi-group">
          <div class="popover-hanzi">${token.text}</div>
          <div class="popover-pinyin">${token.pinyin || ''}</div>
        </div>
        <button type="button" class="popover-close-btn" onclick="GradedReading.closePopover()" aria-label="Đóng">✕</button>
      </div>

      <div class="popover-meta">
        ${token.hsk ? `<span class="popover-hsk-badge">HSK ${token.hsk}</span>` : ''}
        <span class="popover-srs-status ${srsStatus}" id="popoverSrsBadge">${statusLabel}</span>
      </div>

      <div class="popover-body">
        <div class="popover-row">
          <div class="popover-row-label">Nghĩa tiếng Việt</div>
          <div class="popover-meaning">${token.meaning_vi || ''}</div>
        </div>
        ${token.hanviet ? `
          <div class="popover-row">
            <div class="popover-row-label">Hán - Việt</div>
            <div class="popover-hanviet">${token.hanviet}</div>
          </div>
        ` : ''}
      </div>

      ${token.word_id ? `
        <button type="button" class="popover-action-btn ${isAlreadyInSrs ? 'added' : ''}" id="popoverAddSrsBtn" onclick="GradedReading.triggerAddSrs()">
          ${isAlreadyInSrs ? '✓ Đã có trong SRS hôm nay' : '+ Thêm vào hàng đợi SRS'}
        </button>
      ` : ''}
    `;

    document.body.appendChild(popover);
    activePopover = { el: popover, token: token };

    // Position popover near target element
    if (targetEl) {
      const rect = targetEl.getBoundingClientRect();
      const popoverWidth = 290;
      let left = rect.left + window.scrollX;
      let top = rect.bottom + window.scrollY + 8;

      if (left + popoverWidth > window.innerWidth - 16) {
        left = window.innerWidth - popoverWidth - 16;
      }
      if (left < 16) left = 16;

      popover.style.left = `${left}px`;
      popover.style.top = `${top}px`;
    } else {
      popover.style.position = 'fixed';
      popover.style.top = '50%';
      popover.style.left = '50%';
      popover.style.transform = 'translate(-50%, -50%)';
    }

    // Auto close when clicking outside
    setTimeout(() => {
      document.addEventListener('click', onDocClick);
    }, 50);
  }

  function onDocClick(e) {
    if (activePopover && activePopover.el && !activePopover.el.contains(e.target)) {
      closePopover();
    }
  }

  function closePopover() {
    if (activePopover && activePopover.el) {
      activePopover.el.remove();
      activePopover = null;
    }
    document.removeEventListener('click', onDocClick);
  }

  function triggerAddSrs() {
    if (!activePopover || !activePopover.token) return;
    const token = activePopover.token;
    const success = addTokenToSrs(token);
    if (success) {
      const btn = document.getElementById('popoverAddSrsBtn');
      const badge = document.getElementById('popoverSrsBadge');
      if (btn) {
        btn.textContent = '✓ Đã thêm vào SRS thành công!';
        btn.classList.add('added');
      }
      if (badge) {
        badge.textContent = '⚡ Đang học';
        badge.className = 'popover-srs-status learning';
      }
    }
  }

  /**
   * Interactive Quiz answering
   */
  function answerQuiz(qId, selectedIdx) {
    if (!activeStory) return;
    const q = activeStory.quiz.find(item => item.id === qId);
    if (!q) return;

    const quizItem = document.getElementById(`quiz-${qId}`);
    if (!quizItem) return;

    const isCorrect = selectedIdx === q.answer;
    quizState[qId] = { selectedIdx, isCorrect };

    const buttons = quizItem.querySelectorAll('.graded-quiz-opt-btn');
    buttons.forEach((btn, idx) => {
      btn.disabled = true;
      btn.classList.remove('correct', 'wrong');
      if (idx === q.answer) {
        btn.classList.add('correct');
      } else if (idx === selectedIdx && !isCorrect) {
        btn.classList.add('wrong');
      }
    });

    const expEl = document.getElementById(`quiz-exp-${qId}`);
    if (expEl) {
      expEl.style.display = 'block';
      expEl.innerHTML = `
        <div style="font-weight: 700; margin-bottom: 2px;">
          ${isCorrect ? '🎉 Chính xác!' : '❌ Chưa chính xác!'}
        </div>
        <div>${q.explanation_vi}</div>
      `;
    }

    // Auto-mark as read if all quiz questions are answered
    if (activeStory && activeStory.quiz) {
      const allAnswered = activeStory.quiz.every(item => quizState[item.id] !== undefined);
      if (allAnswered && !isStoryRead(activeStory.id)) {
        markStoryAsRead(activeStory.id);
        updateStoryReadUI();
      }
    }
  }

  /**
   * Toggles
   */
  function togglePinyin() {
    prefs.showPinyin = !prefs.showPinyin;
    savePrefs();
    document.body.classList.toggle('graded-pinyin-hidden', !prefs.showPinyin);
    const btn = document.getElementById('togglePinyinBtn');
    if (btn) btn.classList.toggle('active', prefs.showPinyin);
  }

  function toggleTranslation() {
    prefs.showTranslation = !prefs.showTranslation;
    savePrefs();
    document.body.classList.toggle('graded-translation-hidden', !prefs.showTranslation);
    const btn = document.getElementById('toggleTransBtn');
    if (btn) btn.classList.toggle('active', prefs.showTranslation);
  }

  function setLevelFilter(lvl) {
    currentLevelFilter = lvl;
    renderHub();
  }

  return {
    init,
    renderHub,
    openStory,
    goBackToHub,
    togglePinyin,
    toggleTranslation,
    setLevelFilter,
    handleTokenClick,
    inspectByWordId,
    triggerAddSrs,
    closePopover,
    answerQuiz,
    isStoryRead,
    markStoryAsRead,
    unmarkStoryAsRead,
    toggleStoryRead,
    toggleCurrentStoryRead
  };
})();

// Export globally for SPA integration
window.GradedReading = GradedReading;
