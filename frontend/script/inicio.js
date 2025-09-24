function abrirCadastro() {
  document.getElementById('cadastro-barra').style.right = '0';
}

function fecharCadastro() {
  document.getElementById('cadastro-barra').style.right = '-100%';
}

// LOGIN
document.querySelector('.form-acesso form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);

  try {
    const res = await fetch('http://127.0.0.1:5000/login', {
      method: 'POST',
      body: formData
    });

    const data = await res.json();
    alert(data.mensagem);

    if (res.ok) {
      window.location.href = '/home';
    }
  } catch (err) {
    alert('Erro ao conectar com a API');
  }
});

// CADASTRO
document.querySelector('#cadastro-barra form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);

  try {
    const res = await fetch('http://127.0.0.1:5000/cadastro', {
      method: 'POST',
      body: formData
    });

    const data = await res.json();
    alert(data.mensagem);

    if (res.ok) {
      fecharCadastro();
      e.target.reset();
      window.location.href = '/home';
    }
  } catch (err) {
    alert('Erro ao conectar com a API');
  }
});