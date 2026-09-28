const CACHE_NAME = 'hsk-flashcards-v20260928-layout1';
const FSRS_CDN_URL = 'https://cdn.jsdelivr.net/npm/ts-fsrs@5.4.1/dist/index.umd.js';
const APP_SHELL_URL = new URL('./flashcards.html', self.registration.scope).href;

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_NAME);
    await Promise.allSettled([
      cache.add(APP_SHELL_URL),
      cache.add(new Request(FSRS_CDN_URL, { mode: 'cors' })),
    ]);
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const names = await caches.keys();
    await Promise.all(names.filter(name => name.startsWith('hsk-flashcards-') && name !== CACHE_NAME)
      .map(name => caches.delete(name)));
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', event => {
  const request = event.request;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);

  if (url.href === FSRS_CDN_URL) {
    event.respondWith((async () => {
      const cache = await caches.open(CACHE_NAME);
      const cached = await cache.match(request);
      if (cached) return cached;
      const response = await fetch(request);
      if (response.ok || response.type === 'opaque') await cache.put(request, response.clone());
      return response;
    })());
    return;
  }

  if (url.origin !== self.location.origin) return;
  event.respondWith((async () => {
    const cache = await caches.open(CACHE_NAME);
    const cached = await cache.match(request);
    if (cached) return cached;
    const response = await fetch(request);
    if (response.ok) await cache.put(request, response.clone());
    return response;
  })());
});
