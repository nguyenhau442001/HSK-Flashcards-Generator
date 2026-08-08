// Application entry point — feature code lives in assets/js/.
document.querySelectorAll('.level-card').forEach(card => {
  const level = card.dataset.level;
  const cfg = LEVELS[level];
  if (!cfg.available) {
    card.classList.add('disabled');
    return;
  }
  card.addEventListener('click', () => selectLevel(level));
});

renderLevelProgress();
showWelcomeToast();
renderLearningDashboard();
startStudyHeartbeat();

loadRadicalProgress();
loadRadicalPrefs();
