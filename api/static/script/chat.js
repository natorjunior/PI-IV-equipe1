document.addEventListener('DOMContentLoaded', async () => {
    const roomId = window.location.pathname.split('/').pop();
    const msgInput = document.getElementById('msg-input');
    const sendBtn = document.getElementById('btn-enviar');
    const chatBox = document.getElementById('chat-box');
    let usuarioAtual = null;

    // Verifica autenticação e obtém dados do usuário
    try {
        const authResponse = await fetch('/check-auth', {
            credentials: 'include'
        });
        const authData = await authResponse.json();
        
        if (!authData.authenticated) {
            alert("Você precisa fazer login primeiro!");
            window.location.href = "/";    
            return; 
        }
        
        // Obtém nome do usuário da resposta de autenticação
        usuarioAtual = authData.nome_usuario;
    } catch (error) {
        console.error("✗ Erro ao verificar autenticação:", error);
        alert("Erro ao verificar sessão. Faça login novamente.");
        window.location.href = "/";
        return;
    }

    // Função para gerar as iniciais do nome
    function getInitials(name) {
        if (!name) return "U";
        const parts = name.trim().split(' ');
        if (parts.length >= 2) {
            return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
        }
        return name.substring(0, 2).toUpperCase();
    }

    // Função para gerar cor baseada no nome
    function getColorFromName(name) {
        const colors = [
            '#7C8E99', '#6B9DB5', '#8B6BA3', '#A0846D', '#7B9A8F',
            '#9B8B7E', '#8B9FA0', '#9B8BA0', '#8BA09F', '#A08B8B'
        ];
        let hash = 0;
        for (let i = 0; i < name.length; i++) {
            hash = name.charCodeAt(i) + ((hash << 5) - hash);
        }
        return colors[Math.abs(hash) % colors.length];
    }

    async function sendMessage() {
        const text = msgInput.value.trim();

        if (!text) return;

        try {
            const response = await fetch(`/api/chat/${roomId}/messages`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                credentials: 'include', // Envia cookies de sessão
                body: JSON.stringify({ text: text })
            });
            
            if (response.status === 401) {
                alert("Sessão expirada. Faça login novamente.");
                window.location.href = "/";
                return;
            }
            
            msgInput.value = ''; 
            loadMessages(); 
        } catch (error) {
            console.error('Erro ao enviar:', error);
        }
    }

    // Função para BUSCAR mensagens (Sem piscar)
    async function loadMessages() {
        try {
            const res = await fetch(`/api/chat/${roomId}/messages`, {
                credentials: 'include'
            });
            
            if (res.status === 401) {
                alert("Sessão expirada. Faça login novamente.");
                window.location.href = "/";
                return;
            }
            
            const messages = await res.json();

            // Truque: Só atualiza se o número de mensagens mudou
            // (Para evitar que o chat fique piscando ou rolando sozinho se não tem nada novo)
            if (messages.length === chatBox.children.length) {
                return; 
            }

            chatBox.innerHTML = ''; // Limpa

            messages.forEach(msg => {
                const div = document.createElement('div');
                const isOwnMessage = msg.user.trim() === usuarioAtual.trim();
                
                // Aplicar classe baseada se é mensagem do usuário ou de outro
                if (isOwnMessage) {
                    div.classList.add('msg-bubble', 'own-message');
                } else {
                    div.classList.add('msg-bubble', 'other-message');
                }
                
                const initials = getInitials(msg.user);
                const avatarColor = getColorFromName(msg.user);
                
                div.innerHTML = `
                    <div class="msg-header">
                        <div class="msg-avatar" style="background-color: ${avatarColor};">${initials}</div>
                        <div class="msg-user">${msg.user}</div>
                    </div>
                    <div class="msg-content">${msg.text}</div>
                    <div class="msg-time">${msg.time}</div>
                `;
                
                chatBox.appendChild(div);
            });

            // Rola para baixo suavemente
            chatBox.scrollTop = chatBox.scrollHeight;
        } catch (error) {
            console.error('Erro ao carregar:', error);
        }
    }

    if (sendBtn) sendBtn.addEventListener('click', sendMessage);
    
    if (msgInput) {
        msgInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    }

    setInterval(loadMessages, 2000);
    loadMessages();
});