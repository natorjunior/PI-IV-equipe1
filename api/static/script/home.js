document.addEventListener('DOMContentLoaded', () => {
    const feed = document.querySelector('.feed');
    const postButton = document.querySelector('.btn-post');
    const postTextarea = document.querySelector('.criar-post textarea');
    
    // URL BASE da API (Confirme se no app.py o prefixo é /api/posts)
    const API_URL = '/api/posts'; 

    function createPostElement(postData) {
        const post = document.createElement('article');
        post.classList.add('postagem'); 
        post.setAttribute('data-id', postData.id); 

        post.innerHTML = `
            <div class="cabecalho-post">
                <img src="${postData.avatar}" alt="Foto do Usuário" class="avatar">
                <div class="info-usuario">
                    <strong>${postData.username}</strong>
                    <span class="tempo">${postData.timestamp}</span>
                </div>
                ${postData.can_delete ? `<button class="btn-excluir" title="Excluir Post"><i class="fas fa-trash-alt"></i></button>` : ''}
            </div>
            <div class="conteudo-post">
                <p>${postData.content}</p>
            </div>
            <div class="acoes-post">
                <button class="btn-acao curtir ${postData.curtido ? 'curtido' : ''}">
                    <i class="fas fa-heart"></i> ${postData.likes > 0 ? `${postData.likes} Curtidas` : 'Curtir'}
                </button>
            </div>
        `;
        return post;
    }

    async function loadFeed() {
        try {
            // O fetch chama a rota definida no post_routes.py
            const response = await fetch(API_URL);
            const posts = await response.json();
            
            const title = feed.querySelector('h2');
            feed.innerHTML = ''; 
            if(title) feed.appendChild(title);

            posts.forEach(post => {
                feed.appendChild(createPostElement(post));
            });
        } catch (error) {
            console.error('Erro:', error);
        }
    }

    if (postButton) {
        postButton.addEventListener('click', async () => {
            const content = postTextarea.value.trim();
            if (content.length > 0) {
                try {
                    const response = await fetch(API_URL, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ content: content })
                    });

                    if (response.ok) {
                        const newPost = await response.json();
                        postTextarea.value = '';
                        const newEl = createPostElement(newPost);
                        // Insere logo após o título H2
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
            }
        });
    }

    if (feed) {
        feed.addEventListener('click', async (event) => {
            const deleteButton = event.target.closest('.btn-excluir');
            const likeButton = event.target.closest('.btn-acao.curtir');
            const post = event.target.closest('.postagem');
            if (!post) return;

            if (deleteButton) {
                if (confirm('Excluir postagem?')) {
                    const postId = post.getAttribute('data-id');
                    try {
                        const res = await fetch(`${API_URL}/${postId}`, { method: 'DELETE' });
                        if (res.status === 204) post.remove();
                    } catch (e) { console.error(e); }
                }
            }
            
            if (likeButton) {
                likeButton.classList.toggle('curtido');
                // Lógica visual de like (igual ao anterior)
            }
        });
    }

    loadFeed();
});