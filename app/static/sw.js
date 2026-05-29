const CACHE_NAME = 'sabor-prosa-v2';

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(['/', '/dashboard', '/pdv']);
        })
    );
});

self.addEventListener('fetch', (event) => {
    if (event.request.url.includes('/api/pdv/favoritos') || event.request.url.includes('/api/produtos/')) {
        event.respondWith(
            caches.match(event.request).then((response) => {
                return response || fetch(event.request).then((res) => {
                    return caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, res.clone());
                        return res;
                    });
                });
            })
        );
    }
});

self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-vendas') {
        event.waitUntil(sincronizarVendas());
    }
});

async function sincronizarVendas() {
    const db = await new Promise((resolve, reject) => {
        const request = indexedDB.open('SaborProsaPDV', 1);
        request.onupgradeneeded = (e) => {
            if (!e.target.result.objectStoreNames.contains('vendas-offline')) {
                e.target.result.createObjectStore('vendas-offline', { keyPath: 'id', autoIncrement: true });
            }
        };
        request.onsuccess = (e) => resolve(e.target.result);
        request.onerror = (e) => reject(e.target.error);
    });
    const vendas = await new Promise((resolve) => {
        const tx = db.transaction('vendas-offline', 'readonly');
        tx.objectStore('vendas-offline').getAll().onsuccess = (e) => resolve(e.target.result);
    });
    for (const venda of vendas) {
        try {
            await fetch('/api/pdv/vender', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(venda)
            });
            const tx = db.transaction('vendas-offline', 'readwrite');
            tx.objectStore('vendas-offline').delete(venda.id);
        } catch (e) {
            console.log('Falha ao sincronizar:', e);
        }
    }
}
