document.addEventListener('DOMContentLoaded', async () => {
    const feed = document.querySelector('.feed');
    const postButton = document.querySelector('.btn-post');
    const postTextarea = document.querySelector('.criar-post textarea');
    const imageInput = document.getElementById('image-input');
    const imagePreview = document.getElementById('image-preview');
    
    // --- 1. SEGURANÇA E LOGIN ---
    // Verifica autenticação no servidor
    try {
        const authResponse = await fetch('/check-auth', {
            credentials: 'include' // Importante para enviar cookies
        });
        const authData = await authResponse.json();
        
        if (!authData.authenticated) {
            alert("Você precisa fazer login primeiro!");
            window.location.href = "/";    
            return; 
        }
        
        // Exibir nome do usuário na navbar
        const nomeDisplay = document.querySelector(".nome-usuario-display");
        if (nomeDisplay && authData.nome_usuario) {
            nomeDisplay.textContent = authData.nome_usuario;
        }
    } catch (error) {
        console.error("Erro ao verificar autenticação:", error);
        alert("Erro ao verificar sessão. Faça login novamente.");
        window.location.href = "/";
        return;
    }
    
    // Preview da imagem
    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.innerHTML = `
                    <div style="position: relative; display: inline-block; max-width: 100%;">
                        <img src="${e.target.result}" style="max-width: 100%; max-height: 300px; border-radius: 8px; display: block;">
                        <button onclick="document.getElementById('image-input').value=''; document.getElementById('image-preview').innerHTML='';" 
                                style="position: absolute; top: 8px; right: 8px; background: rgba(220, 53, 69, 0.9); color: white; border: none; border-radius: 50%; width: 30px; height: 30px; cursor: pointer; font-size: 18px; line-height: 1;">×</button>
                    </div>
                `;
            };
            reader.readAsDataURL(file);
        }
    });

    // --- 2. TEMA (DARK MODE) ---
    const temaSalvo = localStorage.getItem("theme");
    if (temaSalvo === "dark") {
        document.body.classList.add("dark-mode");
    }

    const API_URL = '/api/posts'; 

    // --- 3. FUNÇÃO PARA CRIAR O HTML DO POST ---
    function createPostElement(postData, currentUserName) {
        const post = document.createElement('article');
        post.classList.add('postagem'); 
        post.setAttribute('data-id', postData.id); 

        const avatarSrc = postData.avatar && postData.avatar.trim() !== "" 
            ? postData.avatar 
            : `https://ui-avatars.com/api/?name=${postData.username}&background=random&color=fff&size=128`;

        const jaCurti = postData.liked_by && postData.liked_by.includes(currentUserName);
        
        const imageHtml = postData.image_url 
            ? `<img src="${postData.image_url}" alt="Imagem do post" loading="lazy">` 
            : '';

        post.innerHTML = `
            <div class="cabecalho-post">
                <img src="${avatarSrc}" alt="Foto" class="avatar">
                <div class="info-usuario">
                    <strong>${postData.username}</strong>
                    <span class="tempo">${postData.timestamp}</span>
                </div>
                ${postData.can_delete ? `<button class="btn-excluir" title="Excluir Post"><i class="fas fa-trash-alt"></i></button>` : ''}
            </div>
            <div class="conteudo-post">
                <p>${postData.content}</p>
                ${imageHtml}
            </div>
            <div class="acoes-post">
                <button class="btn-acao curtir ${jaCurti ? 'curtido' : ''}">
                    <i class="fas fa-heart"></i> ${postData.likes} Curtidas
                </button>
            </div>
        `;
        return post;
    }

    // --- 4. CARREGAR O FEED ---
    async function loadFeed() {
        try {
            const response = await fetch(API_URL, {
                credentials: 'include' // Envia cookies de sessão
            });
            
            if (!response.ok) {
                if (response.status === 401) {
                    alert("Sessão expirada. Faça login novamente.");
                    window.location.href = "/";
                    return;
                }
                throw new Error('Erro ao carregar feed');
            }
            
            const posts = await response.json();
            
            // Pega o nome do usuário atual
            const authResponse = await fetch('/check-auth', { credentials: 'include' });
            const authData = await authResponse.json();
            const currentUserName = authData.nome_usuario;
            
            // Limpa o feed mas mantém o título H2
            const title = feed.querySelector('h2');
            feed.innerHTML = ''; 
            if(title) feed.appendChild(title);

            posts.forEach(post => {
                feed.appendChild(createPostElement(post, currentUserName));
            });
        } catch (error) {
            console.error('Erro ao carregar feed:', error);
        }
    }

    // --- 5. BOTÃO POSTAR ---
    if (postButton) {
        postButton.addEventListener('click', async () => {
            const content = postTextarea.value.trim();
            const imageFile = imageInput.files[0];

            if (!content && !imageFile) {
                alert("Escreva algo ou adicione uma imagem!");
                return;
            }

            try {
                const formData = new FormData();
                formData.append('content', content || ' ');
                if (imageFile) {
                    formData.append('image', imageFile);
                }

                const response = await fetch(API_URL, {
                    method: 'POST',
                    credentials: 'include',
                    body: formData
                });

                if (response.status === 401) {
                    alert("Sessão expirada. Faça login novamente.");
                    window.location.href = "/";
                    return;
                }

                if (response.ok) {
                    const newPost = await response.json();
                    postTextarea.value = '';
                    imageInput.value = '';
                    imagePreview.innerHTML = '';
                    
                    const authResponse = await fetch('/check-auth', { credentials: 'include' });
                    const authData = await authResponse.json();
                    
                    const newEl = createPostElement(newPost, authData.nome_usuario);
                    const title = feed.querySelector('h2');
                    if (title && title.nextSibling) {
                        feed.insertBefore(newEl, title.nextSibling);
                    } else {
                        feed.appendChild(newEl);
                    }
                }
            } catch (error) {
                console.error('Erro ao postar:', error);
            }
        });
    }

    // --- 6. CLIQUES NO FEED (EXCLUIR E CURTIR) ---
    if (feed) {
        feed.addEventListener('click', async (event) => {
            const deleteButton = event.target.closest('.btn-excluir');
            const likeButton = event.target.closest('.btn-acao.curtir');
            const post = event.target.closest('.postagem');
            
            if (!post) return;

            // Excluir
            if (deleteButton) {
                if (confirm('Excluir postagem?')) {
                    const postId = post.getAttribute('data-id');
                    try {
                        const res = await fetch(`${API_URL}/${postId}`, { 
                            method: 'DELETE',
                            credentials: 'include'
                        });
                        if (res.status === 204) post.remove();
                        else if (res.status === 401) {
                            alert("Sessão expirada. Faça login novamente.");
                            window.location.href = "/";
                        } else if (res.status === 403) {
                            alert("Você não tem permissão para excluir este post.");
                        }
                    } catch (e) { console.error(e); }
                }
            }
            
            // Curtir
            if (likeButton) {
                const postId = post.getAttribute('data-id');

                try {
                    const res = await fetch(`${API_URL}/${postId}/like`, { 
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        credentials: 'include'
                    });
                    
                    if (res.status === 401) {
                        alert("Sessão expirada. Faça login novamente.");
                        window.location.href = "/";
                        return;
                    }
                    
                    if (res.ok) {
                        const data = await res.json();
                        
                        if (data.action === 'liked') {
                            likeButton.classList.add('curtido');
                        } else {
                            likeButton.classList.remove('curtido');
                        }
                        likeButton.innerHTML = `<i class="fas fa-heart"></i> ${data.likes} Curtidas`;
                    }
                } catch (error) {
                    console.error("Erro ao curtir:", error);
                }
            }
        });
    }

    // Inicia carregando os posts
    loadFeed();
});

// --- FUNÇÕES GLOBAIS (FORA DO DOMContentLoaded) ---
async function logout() {
    try {
        const response = await fetch('/logout', {
            method: 'POST',
            credentials: 'include'
        });
        
        if (response.ok) {
            // Limpa qualquer dado local que possa existir
            localStorage.clear();
            window.location.href = "/";
        }
    } catch (error) {
        console.error("Erro ao fazer logout:", error);
        // Mesmo com erro, redireciona para a página inicial
        localStorage.clear();
        window.location.href = "/";
    }
}

function toggleTheme() {
    document.body.classList.toggle("dark-mode");
    const isDark = document.body.classList.contains("dark-mode");
    localStorage.setItem("theme", isDark ? "dark" : "light");
}