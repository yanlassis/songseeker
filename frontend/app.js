document.getElementById('search-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const query = document.getElementById('search-input').value.trim();
    if (!query) return;

    const loadingEl = document.getElementById('loading');
    const resultsEl = document.getElementById('results');
    const errorEl = document.getElementById('error-message');
    
    const seedContainer = document.getElementById('seed-track-container');
    const recsContainer = document.getElementById('recommendations-container');

    // Reset UI
    loadingEl.classList.remove('hidden');
    resultsEl.classList.add('hidden');
    errorEl.classList.add('hidden');
    seedContainer.innerHTML = '';
    recsContainer.innerHTML = '';

    try {
        // 1. Busca a música semente
        const searchRes = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        if (!searchRes.ok) throw new Error('Música não encontrada.');
        const searchData = await searchRes.json();
        const seedTrack = searchData.track;

        // Renderiza semente no iframe
        seedContainer.innerHTML = createSpotifyIframe(seedTrack.spotify_id);

        // 2. Busca recomendações baseadas na semente
        const artist = seedTrack.artist_name;
        const trackName = seedTrack.name;
        
        const recsRes = await fetch(`/api/recommendations?artist=${encodeURIComponent(artist)}&track=${encodeURIComponent(trackName)}`);
        if (!recsRes.ok) throw new Error('Erro ao buscar recomendações.');
        const recsData = await recsRes.json();

        // Renderiza recomendações
        if (recsData.recommendations.length === 0) {
            recsContainer.innerHTML = '<p style="color: var(--text-secondary)">Nenhuma recomendação encontrada para esta música.</p>';
        } else {
            recsData.recommendations.forEach(rec => {
                const wrapper = document.createElement('div');
                wrapper.className = 'iframe-container';
                wrapper.innerHTML = createSpotifyIframe(rec.spotify_id);
                recsContainer.appendChild(wrapper);
            });
        }

        loadingEl.classList.add('hidden');
        resultsEl.classList.remove('hidden');

    } catch (err) {
        loadingEl.classList.add('hidden');
        errorEl.textContent = err.message || 'Ocorreu um erro inesperado.';
        errorEl.classList.remove('hidden');
    }
});

function createSpotifyIframe(spotifyId) {
    if (!spotifyId) return '';
    return `<iframe 
        style="border-radius:12px" 
        src="https://open.spotify.com/embed/track/${spotifyId}?utm_source=generator&theme=0" 
        width="100%" 
        height="152" 
        frameBorder="0" 
        allowfullscreen="" 
        allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
        loading="lazy">
    </iframe>`;
}
