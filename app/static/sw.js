// Service Worker - Sabor e Prosa Empório
const CACHE_NAME = 'sabor-prosa-v2';
const urlsToCache = [
    '/',
    '/dashboard',
    '/pdv',
    '/vitrine',
    '/static/manifest.json',
    '/static/icon-192.png',
    '/static/icon-512.png',
];

// Instalação
self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME).then(function(cache) {
            console.log('Cache aberto');
            return cache.addAll(urlsToCache);
        })
    );
});

// Ativação - limpa caches antigos
self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Removendo cache antigo:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Fetch - Estratégia: Network First, Cache Fallback
self.addEventListener('fetch', function(event) {
    // Para API, tenta rede primeiro
    if (event.request.url.includes('/api/')) {
        event.respondWith(
            fetch(event.request)
                .then(function(response) {
                    // Cache da resposta para uso offline
                    var responseClone = response.clone();
                    caches.open(CACHE_NAME).then(function(cache) {
                        cache.put(event.request, responseClone);
                    });
                    return response;
                })
                .catch(function() {
                    return caches.match(event.request);
                })
        );
        return;
    }
    
    // Para arquivos estáticos e páginas
    event.respondWith(
        caches.match(event.request).then(function(response) {
            return response || fetch(event.request).then(function(fetchResponse) {
                var responseClone = fetchResponse.clone();
                caches.open(CACHE_NAME).then(function(cache) {
                    cache.put(event.request, responseClone);
                });
                return fetchResponse;
            });
        })
    );
});

// Sincronização em background (vendas offline)
self.addEventListener('sync', function(event) {
    if (event.tag === 'sync-vendas') {
        event.waitUntil(sincronizarVendas());
    }
});

async function sincronizarVendas() {
    try {
        const db = await openDB();
        const vendas = await getAllFromDB(db, 'vendas-offline');
        
        for (const venda of vendas) {
            try {
                await fetch('/api/pdv/vender', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(venda)
                });
                await deleteFromDB(db, 'vendas-offline', venda.id);
            } catch(e) {
                console.log('Falha ao sincronizar venda:', e);
            }
        }
    } catch(e) {
        console.log('Erro na sincronização:', e);
    }
}

function openDB() {
    return new Promise(function(resolve, reject) {
        var request = indexedDB.open('SaborProsaPDV', 1);
        request.onupgradeneeded = function(e) {
            var db = e.target.result;
            if (!db.objectStoreNames.contains('vendas-offline')) {
                db.createObjectStore('vendas-offline', {keyPath: 'id', autoIncrement: true});
            }
        };
        request.onsuccess = function(e) { resolve(e.target.result); };
        request.onerror = function(e) { reject(e.target.error); };
    });
}

function getAllFromDB(db, storeName) {
    return new Promise(function(resolve) {
        var tx = db.transaction(storeName, 'readonly');
        var store = tx.objectStore(storeName);
        var request = store.getAll();
        request.onsuccess = function() { resolve(request.result); };
    });
}

function deleteFromDB(db, storeName, id) {
    return new Promise(function(resolve) {
        var tx = db.transaction(storeName, 'readwrite');
        tx.objectStore(storeName).delete(id);
        tx.oncomplete = function() { resolve(); };
    });
}
