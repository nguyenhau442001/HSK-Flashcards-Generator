// FSRS boundary. Application code should use SRS instead of ts-fsrs directly.
const SRS = (function () {
  const library = window.ts_fsrs;
  if (!library || typeof library.fsrs !== 'function') {
    throw new Error('Không tải được ts-fsrs 5.4.1 (global ts_fsrs không tồn tại).');
  }

  const RATINGS = {
    again: library.Rating.Again,
    hard: library.Rating.Hard,
    good: library.Rating.Good,
    easy: library.Rating.Easy,
  };
  const RATING_NAMES = {
    [RATINGS.again]: 'again',
    [RATINGS.hard]: 'hard',
    [RATINGS.good]: 'good',
    [RATINGS.easy]: 'easy',
  };
  const DEFAULT_RETENTION = 0.9;

  function normalizeRetention(value) {
    const retention = Number(value);
    return Number.isFinite(retention)
      ? Math.min(0.97, Math.max(0.8, retention))
      : DEFAULT_RETENTION;
  }

  function scheduler(retention) {
    return library.fsrs({
      request_retention: normalizeRetention(retention),
      enable_fuzz: true,
    });
  }

  function parseDate(value) {
    if (value instanceof Date) return new Date(value.getTime());
    if (typeof value === 'string' || typeof value === 'number') {
      const date = new Date(value);
      if (Number.isFinite(date.getTime())) return date;
    }
    return null;
  }

  function deserializeCard(value) {
    if (!value || typeof value !== 'object') return null;
    const card = { ...value };
    card.due = parseDate(card.due);
    card.last_review = card.last_review == null ? undefined : parseDate(card.last_review);
    if (!card.due || (value.last_review != null && !card.last_review)) return null;
    return card;
  }

  function serializeCard(value) {
    const card = deserializeCard(value);
    if (!card) return null;
    return {
      ...card,
      due: card.due.toISOString(),
      last_review: card.last_review ? card.last_review.toISOString() : null,
    };
  }

  function createNewCard(now) {
    return serializeCard(library.createEmptyCard(parseDate(now) || new Date()));
  }

  function review(cardValue, ratingName, now, retention) {
    const card = deserializeCard(cardValue);
    const rating = RATINGS[ratingName];
    if (!card) throw new Error('Thẻ FSRS không hợp lệ.');
    if (rating === undefined) throw new Error('Mức đánh giá FSRS không hợp lệ.');
    const reviewedAt = parseDate(now) || new Date();
    const result = scheduler(retention).next(card, reviewedAt, rating);
    return {
      card: serializeCard(result.card),
      log: {
        ...result.log,
        rating: ratingName,
        state: result.log.state,
        due: result.log.due.toISOString(),
        review: result.log.review.toISOString(),
      },
      rating: ratingName,
      stateBefore: card.state,
      stateAfter: result.card.state,
      elapsedDays: card.last_review
        ? Math.max(0, (reviewedAt.getTime() - card.last_review.getTime()) / 86400000)
        : 0,
    };
  }

  function preview(cardValue, now, retention) {
    const card = deserializeCard(cardValue);
    if (!card) return {};
    const previews = scheduler(retention).repeat(card, parseDate(now) || new Date());
    const result = {};
    Object.keys(RATINGS).forEach(name => {
      const item = previews[RATINGS[name]];
      if (!item) return;
      result[name] = {
        card: serializeCard(item.card),
        due: item.card.due.toISOString(),
        intervalMs: Math.max(0, item.card.due.getTime() - (parseDate(now) || new Date()).getTime()),
        scheduledDays: item.log && Number.isFinite(item.log.scheduled_days) ? item.log.scheduled_days : null,
      };
    });
    return result;
  }

  function isDue(cardValue, now) {
    const card = deserializeCard(cardValue);
    if (!card || card.state === library.State.New) return false;
    return card.due.getTime() <= (parseDate(now) || new Date()).getTime();
  }

  function retrievability(cardValue, now, retention) {
    const card = deserializeCard(cardValue);
    if (!card || card.state === library.State.New) return 0;
    return scheduler(retention).get_retrievability(card, parseDate(now) || new Date(), false);
  }

  function ratingValue(name) {
    return RATINGS[name];
  }

  function ratingName(value) {
    return RATING_NAMES[value] || null;
  }

  return Object.freeze({
    DEFAULT_RETENTION,
    State: library.State,
    RATINGS: Object.freeze({ ...RATINGS }),
    RATING_NAMES: Object.freeze({ ...RATING_NAMES }),
    normalizeRetention,
    createNewCard,
    deserializeCard,
    serializeCard,
    review,
    preview,
    isDue,
    retrievability,
    ratingValue,
    ratingName,
  });
})();
