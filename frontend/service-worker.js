/**
 * HEPo (Heat Encroachment Pockets) - Progressive Web App Service Worker
 * Robust Vanilla Service Worker for Offline App Shell & Tile Resilience
 * (Zero external dependencies / No Workbox required)
 */

const CACHE_NAME = 'hepo-pwa-v3';
const TILE_CACHE_NAME = 'hepo-tile-cache-v1';

const APP_SHELL_ASSETS = [
  './',
  './index.html',
  './styles.css',
  './app.js',
  './manifest.webmanifest',
  './icons/favicon.svg',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable-512.png',
  './icons/apple-touch-icon.png',
  './vendor/leaflet/leaflet.css',
  './vendor/leaflet/leaflet.js'
];

// 1. Install Event: Pre-cache core application shell
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(APP_SHELL_ASSETS))
      .then(() => self.skipWaiting())
  );
});

// 2. Activate Event: Clean up outdated cache stores
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME && key !== TILE_CACHE_NAME) {
            console.log('[HEPo SW] Evicting legacy cache:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// 3. Fetch Event: Intelligent routing for shell, tiles, and telemetry
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // A. Live AWS Telemetry & API Endpoints:
  // Strictly Network-First. Do NOT pretend AWS data is available offline.
  if (url.pathname.includes('/observations') || url.pathname.includes('/heat-pockets') || url.pathname.startsWith('/api')) {
    event.respondWith(
      fetch(event.request).catch(() => {
        return new Response(
          JSON.stringify({
            error: 'Offline: Live AWS cloud telemetry is unavailable without internet connectivity.',
            offline: true
          }),
          {
            status: 503,
            statusText: 'Service Unavailable (Offline)',
            headers: { 'Content-Type': 'application/json' }
          }
        );
      })
    );
    return;
  }

  // B. OpenStreetMap Raster Tiles:
  // Network-first with local fallback to previously cached tiles
  if (url.hostname.includes('tile.openstreetmap.org')) {
    event.respondWith(
      fetch(event.request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const clone = networkResponse.clone();
            caches.open(TILE_CACHE_NAME).then((cache) => cache.put(event.request, clone));
          }
          return networkResponse;
        })
        .catch(() => {
          return caches.match(event.request).then((cachedTile) => {
            return cachedTile || new Response('', { status: 503, statusText: 'Tile Unavailable Offline' });
          });
        })
    );
    return;
  }

  // C. Local Application Shell Assets (HTML, CSS, JS, Icons, Leaflet Vendor):
  // Cache-first with background Stale-While-Revalidate
  if (url.origin === self.location.origin) {
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        if (cachedResponse) {
          // Revalidate in background if online
          fetch(event.request)
            .then((networkResponse) => {
              if (networkResponse && networkResponse.status === 200) {
                caches.open(CACHE_NAME).then((cache) => cache.put(event.request, networkResponse));
              }
            })
            .catch(() => {
              // Harmless offline failure during background fetch
            });
          return cachedResponse;
        }

        // Cache miss: retrieve from network and save to cache
        return fetch(event.request)
          .then((networkResponse) => {
            if (networkResponse && networkResponse.status === 200) {
              const clone = networkResponse.clone();
              caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
            }
            return networkResponse;
          })
          .catch(() => {
            // Navigation fallback for SPA/PWA routing
            if (event.request.mode === 'navigate' || event.request.headers.get('accept')?.includes('text/html')) {
              return caches.match('./index.html') || caches.match('./');
            }
          });
      })
    );
    return;
  }

  // D. General Network Fallback
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});
