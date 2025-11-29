/**
 * Configurações e funções para detecção e preview de links
 * Abordagem sutil: apenas YouTube com preview discreto
 */

// --- CONFIGURAÇÕES ---
const LINK_CONFIG = {
    enableYouTube: true,
    enableInstagram: false,
    enableTelegram: false,
    // Se true, não mostra preview quando há imagem no post
    disableWithImage: true
};

/**
 * Extrai o ID do vídeo do YouTube de várias URLs
 */
function extractYouTubeId(url) {
    const patterns = [
        /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]+)/,
        /youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]+)/
    ];
    
    for (const pattern of patterns) {
        const match = url.match(pattern);
        if (match && match[1]) {
            return match[1];
        }
    }
    return null;
}

/**
 * Detecta se há link do YouTube no conteúdo
 */
function detectYouTubeLink(content) {
    const urlRegex = /(https?:\/\/(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/shorts\/)[^\s]+)/g;
    const match = content.match(urlRegex);
    
    if (match && match[0]) {
        const videoId = extractYouTubeId(match[0]);
        if (videoId) {
            return {
                found: true,
                url: match[0],
                videoId: videoId
            };
        }
    }
    
    return { found: false };
}

/**
 * Cria um preview do YouTube com player embutido
 */
function createYouTubePreview(videoId, url) {
    return `
        <div class="youtube-preview-subtle">
            <div class="video-container">
                <iframe 
                    src="https://www.youtube.com/embed/${videoId}" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen>
                </iframe>
            </div>
            <a href="${url}" target="_blank" rel="noopener noreferrer" class="youtube-link-subtle">
                <i class="fab fa-youtube"></i> Assistir no YouTube
            </a>
        </div>
    `;
}

/**
 * Processa o conteúdo do post para detectar e adicionar preview do YouTube
 * @param {string} content - Conteúdo do post
 * @param {boolean} hasImage - Se o post já tem uma imagem
 * @returns {object} - { text: string, preview: string }
 */
function processContentWithYouTube(content, hasImage = false) {
    // Se tem imagem e a config diz para não mostrar preview, retorna o conteúdo original
    if (hasImage && LINK_CONFIG.disableWithImage) {
        return { text: content, preview: '' };
    }
    
    // Se YouTube não está habilitado, retorna original
    if (!LINK_CONFIG.enableYouTube) {
        return { text: content, preview: '' };
    }
    
    const youtubeLink = detectYouTubeLink(content);
    
    if (!youtubeLink.found) {
        return { text: content, preview: '' };
    }
    
    // Remove o link do texto (mantém o restante)
    const textWithoutLink = content.replace(youtubeLink.url, '').trim();
    
    // Cria o preview
    const preview = createYouTubePreview(youtubeLink.videoId, youtubeLink.url);
    
    return {
        text: textWithoutLink,
        preview: preview
    };
}

/**
 * Processa links genéricos (transforma em links clicáveis sem preview)
 */
function makeLinksClickable(text) {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    return text.replace(urlRegex, '<a href="$1" target="_blank" rel="noopener noreferrer" class="text-link">$1</a>');
}
