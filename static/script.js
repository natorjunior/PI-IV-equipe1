document.addEventListener('DOMContentLoaded', () => {
    const feed = document.querySelector('.feed');
    const postButton = document.querySelector('.btn-post');
    const postTextarea = document.querySelector('.criar-post textarea'); 
    
    const userAvatarUrl = "https://via.placeholder.com/40/FF00FF/ffffff?text=L"; 
    const currentUsername = "Usuário Logado"; 

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
            const response = await fetch('/api/posts');
            const posts = await response.json();
            
            feed.querySelector('h2').textContent = 'Feed de Postagens';
            
            feed.querySelectorAll('.postagem').forEach(p => p.remove());

            posts.forEach(post => {
                feed.appendChild(createPostElement(post));
            });

        } catch (error) {
            console.error('Erro ao carregar o feed:', error);
            feed.innerHTML = `<h2>Erro ao carregar o feed.</h2>`;
        }
    }

    if (postButton) {
        postButton.addEventListener('click', async () => {
            const content = postTextarea.value.trim();

            if (content.length > 0) {
                try {
                    const response = await fetch('/api/posts', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ content: content })
                    });

                    if (response.ok) {
                        const newPost = await response.json();
                        postTextarea.value = '';
                        
                        const newPostElement = createPostElement(newPost);
                        feed.insertBefore(newPostElement, feed.children[1]); 
                    } else {
                        alert('Erro ao postar. Tente novamente.');
                    }
                } catch (error) {
                    console.error('Erro de conexão:', error);
                    alert('Não foi possível conectar ao servidor.');
                }
            } else {
                alert('O conteúdo da postagem não pode estar vazio.');
            }
        });
    }

    if (feed) {
        feed.addEventListener('click', async (event) => {
            
            const likeButton = event.target.closest('.btn-acao.curtir');
            const deleteButton = event.target.closest('.btn-excluir');
            
            const post = event.target.closest('.postagem');
            if (!post) return;

            if (deleteButton) {
                const isConfirmed = confirm('Tem certeza que deseja excluir esta postagem? Esta ação é permanente.');
                
                if (isConfirmed) {
                    const postId = post.getAttribute('data-id');
                    
                    if (!postId) {
                        console.error("ID da postagem não encontrado.");
                        return;
                    }

                    try {
                        const response = await fetch(`/api/posts/${postId}`, {
                            method: 'DELETE'
                        });

                        if (response.status === 204) {
                            post.remove(); 
                            console.log(`Postagem ${postId} excluída com sucesso!`);
                        } else {
                            alert('Erro ao excluir a postagem. O servidor não permitiu.');
                        }
                    } catch (error) {
                        console.error('Erro de conexão ao tentar excluir:', error);
                        alert('Não foi possível conectar ao servidor para excluir a postagem.');
                    }
                }
            }


            if (likeButton) {
                
                likeButton.classList.toggle('curtido'); 
                let currentLikes = parseInt(likeButton.textContent.match(/\d+/) || 0);
                
                if (likeButton.classList.contains('curtido')) {
                    currentLikes++;
                    likeButton.innerHTML = `<i class="fas fa-heart"></i> ${currentLikes} Curtidas`;
                } else {
                    currentLikes = Math.max(0, currentLikes - 1);
                    
                    if (currentLikes > 0) {
                        likeButton.innerHTML = `<i class="fas fa-heart"></i> ${currentLikes} Curtidas`;
                    } else {
                        likeButton.innerHTML = `<i class="fas fa-heart"></i> Curtir`;
                    }
                }
            }
        });
    }

    loadFeed();
});