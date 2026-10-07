// assets/js/cloud-sync.js
// Cloud synchronization module powered by Google Firebase Auth & Cloud Firestore
// Supports zero-cost session-end sync, bidirectional merge, and offline persistence.

const CloudSync = (function() {
  const CONFIG_STORAGE_KEY = 'hsk_firebase_config';
  const LAST_SYNC_KEY = 'hsk_last_sync_time';

  // Default placeholder config (can be configured via UI modal or overwritten)
  const defaultFirebaseConfig = {
    apiKey: "",
    authDomain: "",
    projectId: "",
    storageBucket: "",
    messagingSenderId: "",
    appId: ""
  };

  let auth = null;
  let db = null;
  let currentUser = null;
  let isSyncing = false;
  let syncDebounceTimer = null;

  function getStoredConfig() {
    try {
      const stored = localStorage.getItem(CONFIG_STORAGE_KEY);
      if (stored) return JSON.parse(stored);
    } catch (e) {}
    return defaultFirebaseConfig;
  }

  function isConfigValid(cfg) {
    return Boolean(cfg && cfg.apiKey && cfg.projectId && cfg.apiKey.trim() !== "");
  }

  function initFirebase() {
    const config = getStoredConfig();
    if (!isConfigValid(config)) {
      console.log('CloudSync: Firebase config not set yet. Open sync modal to configure.');
      return false;
    }

    if (typeof firebase === 'undefined') {
      console.warn('CloudSync: Firebase SDK not loaded.');
      return false;
    }

    try {
      if (!firebase.apps.length) {
        firebase.initializeApp(config);
      }
      auth = firebase.auth();
      db = firebase.firestore();

      auth.onAuthStateChanged(user => {
        currentUser = user;
        updateUI();
        if (user) {
          syncWithCloud({ silent: true });
        }
      });
      return true;
    } catch (err) {
      console.error('CloudSync: Init error', err);
      return false;
    }
  }

  // Pack all local storage data into a single consolidated snapshot
  function packLocalSnapshot() {
    const levels = {};
    const allLevelKeys = [
      'hsk1', 'hsk2', 'hsk3', 'hsk4', 'hsk5', 'hsk6', 'hsk79',
      'hsk30_1', 'hsk30_2', 'hsk30_3', 'hsk30_4', 'hsk30_5', 'hsk30_6', 'hsk30_79',
      'topic_travel', 'topic_business', 'topic_restaurant', 'topic_shopping', 'topic_daily'
    ];

    allLevelKeys.forEach(lvl => {
      const srsV3Raw = localStorage.getItem(`hsk_${lvl}_srs_v3`);
      const reviewLogRaw = localStorage.getItem(`hsk_${lvl}_review_log_v1`);
      const progressRaw = localStorage.getItem(`hsk_${lvl}_progress_v2`);
      const prefsRaw = localStorage.getItem(`hsk_${lvl}_prefs_v2`);
      if (srsV3Raw || reviewLogRaw || progressRaw || prefsRaw) {
        levels[lvl] = {
          srsV3: srsV3Raw ? JSON.parse(srsV3Raw) : null,
          reviewLog: reviewLogRaw ? JSON.parse(reviewLogRaw) : null,
          progress: progressRaw ? JSON.parse(progressRaw) : null,
          prefs: prefsRaw ? JSON.parse(prefsRaw) : null
        };
      }
    });

    let activity = null;
    try {
      const rawAct = localStorage.getItem('hsk_activity_v1');
      if (rawAct) activity = JSON.parse(rawAct);
    } catch (e) {}

    let weakWords = null;
    try {
      const rawWeak = localStorage.getItem('hsk_weak_words_v1');
      if (rawWeak) weakWords = JSON.parse(rawWeak);
    } catch (e) {}

    let radicals = null;
    try {
      const rawRad = localStorage.getItem('hsk_radicals_progress');
      if (rawRad) radicals = JSON.parse(rawRad);
    } catch (e) {}

    let srsPrefs = null;
    try {
      const rawPrefs = localStorage.getItem('hsk_srs_prefs_v1');
      if (rawPrefs) srsPrefs = JSON.parse(rawPrefs);
    } catch (e) {}

    return {
      schemaVersion: 5,
      updatedAt: Date.now(),
      levels,
      activity,
      weakWords,
      radicals,
      settings: {
        srsPrefs,
        desiredRetention: localStorage.getItem('hsk_srs_retention_target') || '0.9',
        dailyStudyGoal: localStorage.getItem('hsk_daily_study_goal') || '10',
        showHanviet: localStorage.getItem('hsk_show_hanviet') || 'true',
        theme: localStorage.getItem('hsk_theme') || 'dark',
        readingPrefs: localStorage.getItem('hsk4_reading_prefs') || null
      }
    };
  }

  // Restore remote cloud snapshot into localStorage safely
  function unpackRemoteSnapshot(data) {
    if (!data || !data.levels) return;

    Object.entries(data.levels).forEach(([lvl, lvlData]) => {
      if (lvlData.srsV3) {
        localStorage.setItem(`hsk_${lvl}_srs_v3`, JSON.stringify(lvlData.srsV3));
      } else if (lvlData.cards) {
        // Backwards compatibility if remote was v4
        localStorage.setItem(`hsk_${lvl}_srs_v3`, JSON.stringify({
          schemaVersion: 3,
          migratedFromV2: true,
          cards: lvlData.cards
        }));
      }

      if (lvlData.reviewLog) {
        localStorage.setItem(`hsk_${lvl}_review_log_v1`, JSON.stringify(lvlData.reviewLog));
      } else if (lvlData.reviews) {
        localStorage.setItem(`hsk_${lvl}_review_log_v1`, JSON.stringify(lvlData.reviews));
      }

      if (lvlData.progress) {
        localStorage.setItem(`hsk_${lvl}_progress_v2`, JSON.stringify(lvlData.progress));
      }
      if (lvlData.prefs) {
        localStorage.setItem(`hsk_${lvl}_prefs_v2`, JSON.stringify(lvlData.prefs));
      }
    });

    if (data.activity) {
      localStorage.setItem('hsk_activity_v1', JSON.stringify(data.activity));
    }
    if (data.weakWords) {
      localStorage.setItem('hsk_weak_words_v1', JSON.stringify(data.weakWords));
    }
    if (data.radicals) {
      localStorage.setItem('hsk_radicals_progress', JSON.stringify(data.radicals));
    }
    if (data.settings) {
      if (data.settings.srsPrefs) {
        localStorage.setItem('hsk_srs_prefs_v1', JSON.stringify(data.settings.srsPrefs));
      }
      if (data.settings.desiredRetention) localStorage.setItem('hsk_srs_retention_target', data.settings.desiredRetention);
      if (data.settings.dailyStudyGoal) localStorage.setItem('hsk_daily_study_goal', data.settings.dailyStudyGoal);
      if (data.settings.showHanviet) localStorage.setItem('hsk_show_hanviet', data.settings.showHanviet);
      if (data.settings.theme) localStorage.setItem('hsk_theme', data.settings.theme);
      if (data.settings.readingPrefs) localStorage.setItem('hsk4_reading_prefs', data.settings.readingPrefs);
    }

    // Refresh active study UI if open
    if (typeof currentLevel !== 'undefined' && currentLevel) {
      if (typeof loadState === 'function') loadState();
      if (typeof updateProgress === 'function') updateProgress();
      if (typeof updateStats === 'function') updateStats();
      if (typeof render === 'function') render();
    }
    if (typeof renderLearningDashboard === 'function') {
      renderLearningDashboard();
    }
  }

  // Main Bidirectional Sync logic
  async function syncWithCloud(options = {}) {
    if (!currentUser || !db || isSyncing) return;
    if (!navigator.onLine) {
      setStatus('offline', 'Mất kết nối mạng');
      return;
    }

    isSyncing = true;
    setStatus('syncing', 'Đang đồng bộ...');
    const syncBtn = document.getElementById('headerSyncBtn');
    if (syncBtn) syncBtn.classList.add('is-syncing');

    try {
      const docRef = db.collection('users').doc(currentUser.uid).collection('hsk_data').doc('sync_progress');
      const docSnap = await docRef.get();
      const localData = packLocalSnapshot();

      if (!docSnap.exists) {
        // First-time sync: Upload local to Cloud
        await docRef.set(localData);
        setStatus('ok', 'Đã sao lưu lên đám mây');
      } else {
        const cloudData = docSnap.data();
        const cloudTime = cloudData.updatedAt || 0;
        const lastSyncTime = parseInt(localStorage.getItem(LAST_SYNC_KEY) || '0', 10);

        if (cloudTime > lastSyncTime) {
          // Cloud has newer data -> pull down
          unpackRemoteSnapshot(cloudData);
          setStatus('ok', 'Đã cập nhật từ đám mây');
        } else {
          // Local has newer changes -> push up
          await docRef.set(localData, { merge: true });
          setStatus('ok', 'Đã đồng bộ');
        }
      }

      const now = Date.now();
      localStorage.setItem(LAST_SYNC_KEY, String(now));
      updateLastSyncedTime(now);

      if (!options.silent) {
        alert('Đồng bộ dữ liệu đám mây thành công!');
      }
    } catch (err) {
      console.error('CloudSync error:', err);
      setStatus('error', 'Lỗi đồng bộ');
      if (!options.silent) {
        alert('Đồng bộ thất bại: ' + (err.message || 'Lỗi mạng hoặc phân quyền'));
      }
    } finally {
      isSyncing = false;
      if (syncBtn) syncBtn.classList.remove('is-syncing');
    }
  }

  function setStatus(state, msg) {
    const badge = document.getElementById('syncStatusBadge');
    if (badge) {
      badge.textContent = msg;
      badge.className = `sync-badge sync-badge-${state}`;
    }
    const headerBtn = document.getElementById('headerSyncBtn');
    if (headerBtn) {
      headerBtn.title = `Đồng bộ: ${msg}`;
    }
  }

  function updateLastSyncedTime(timestamp) {
    const el = document.getElementById('lastSyncedTime');
    if (!el || !timestamp) return;
    const date = new Date(timestamp);
    const timeStr = `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
    const dateStr = `${String(date.getDate()).padStart(2, '0')}/${String(date.getMonth() + 1).padStart(2, '0')}/${date.getFullYear()}`;
    el.textContent = `${timeStr} · ${dateStr}`;
  }

  function updateUI() {
    const loggedOutView = document.getElementById('syncLoggedOutView');
    const loggedInView = document.getElementById('syncLoggedInView');
    const configSection = document.getElementById('syncConfigSection');
    const hasConfig = isConfigValid(getStoredConfig());

    if (configSection) {
      configSection.style.display = hasConfig ? 'none' : 'block';
    }

    if (currentUser) {
      if (loggedOutView) loggedOutView.style.display = 'none';
      if (loggedInView) loggedInView.style.display = 'block';

      const nameEl = document.getElementById('userName');
      if (nameEl) nameEl.textContent = currentUser.displayName || 'Học viên HSK';
      const emailEl = document.getElementById('userEmail');
      if (emailEl) emailEl.textContent = currentUser.email || '';
      const avatarEl = document.getElementById('userAvatar');
      if (avatarEl && currentUser.photoURL) avatarEl.src = currentUser.photoURL;

      const last = localStorage.getItem(LAST_SYNC_KEY);
      if (last) updateLastSyncedTime(parseInt(last, 10));
      setStatus('ok', 'Đã kết nối tài khoản');
    } else {
      if (loggedOutView) loggedOutView.style.display = 'block';
      if (loggedInView) loggedInView.style.display = 'none';
      setStatus('offline', 'Chưa kết nối');
    }
  }

  function loginWithGoogle() {
    if (!auth) {
      if (!initFirebase()) {
        alert('Vui lòng nhập mã cấu hình Firebase trước khi đăng nhập (Bấm "⚙️ Cài đặt cấu hình Firebase" bên dưới).');
        return;
      }
    }
    const provider = new firebase.auth.GoogleAuthProvider();
    auth.signInWithPopup(provider).catch(err => {
      console.error('Google Sign-in failed:', err);
      alert('Đăng nhập Google thất bại: ' + err.message);
    });
  }

  function logoutGoogle() {
    if (auth && confirm('Bạn có chắc chắn muốn đăng xuất tài khoản đồng bộ?')) {
      auth.signOut().then(() => {
        currentUser = null;
        updateUI();
      });
    }
  }

  function saveCustomFirebaseConfig(configJsonStr) {
    try {
      let cleaned = configJsonStr.trim();
      if (cleaned.startsWith('const firebaseConfig =')) {
        cleaned = cleaned.replace(/^const firebaseConfig =\s*/, '').replace(/;\s*$/, '');
      }
      const parsed = JSON.parse(cleaned);
      if (!parsed.apiKey || !parsed.projectId) {
        throw new Error('Cấu hình thiếu apiKey hoặc projectId');
      }
      localStorage.setItem(CONFIG_STORAGE_KEY, JSON.stringify(parsed));
      alert('Đã lưu cấu hình Firebase thành công! Đang kết nối...');
      initFirebase();
      updateUI();
    } catch (e) {
      alert('Cấu hình JSON không hợp lệ: ' + e.message);
    }
  }

  // Debounced auto-sync after learning activity
  function requestDebouncedSync() {
    if (!currentUser) return;
    if (syncDebounceTimer) clearTimeout(syncDebounceTimer);
    syncDebounceTimer = setTimeout(() => {
      syncWithCloud({ silent: true });
    }, 45000); // 45 seconds after last activity
  }

  function openSyncModal() {
    const modal = document.getElementById('syncModal');
    if (!modal) return;
    modal.classList.add('is-open');
    const input = document.getElementById('firebaseConfigInput');
    if (input && !input.value) {
      const stored = getStoredConfig();
      if (isConfigValid(stored)) {
        input.value = JSON.stringify(stored, null, 2);
      }
    }
    updateUI();
  }

  function closeSyncModal() {
    const modal = document.getElementById('syncModal');
    if (!modal) return;
    modal.classList.remove('is-open');
  }

  // Network & Session lifecycle listeners
  window.addEventListener('online', () => {
    if (currentUser) syncWithCloud({ silent: true });
  });

  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden' && currentUser) {
      syncWithCloud({ silent: true });
    }
  });

  // Auto-init on DOM ready
  document.addEventListener('DOMContentLoaded', () => {
    initFirebase();
    const modal = document.getElementById('syncModal');
    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) closeSyncModal();
      });
    }
  });

  return {
    init: initFirebase,
    sync: syncWithCloud,
    login: loginWithGoogle,
    logout: logoutGoogle,
    openModal: openSyncModal,
    closeModal: closeSyncModal,
    saveConfig: saveCustomFirebaseConfig,
    requestDebouncedSync,
    getUser: () => currentUser
  };
})();

window.CloudSync = CloudSync;
