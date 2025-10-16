let tasks = [];

function init(){
    const storedTasks = localStorage.getItem(`todoTasks`);
    if (storedTasks){
        tasks = JSON.parse(storedTasks);
    }

    renderTasks(`all`);

    setupEventListeners();
}

function saveTasks(){
    localStorage.setItem(`todoTasks`,JSON.stringify(tasks));
}

function addTask(title, description){
    const newTask = {
        id: Date.now(),
        title: title,
        description: description,
        completed: false
    };
    tasks.push(newTask);
    saveTasks();
    renderTasks(document.querySelector('#filters .active').dataset.filter);
}

// 2. Listar Tarefas & Filtrar Tarefas
function renderTasks(filterStatus) {
    const taskList = document.getElementById('task-list');
    taskList.innerHTML = ''; // Limpa a lista antes de renderizar

    // Filtragem
    let filteredTasks = tasks;
    if (filterStatus === 'pending') {
        filteredTasks = tasks.filter(task => !task.completed);
    } else if (filterStatus === 'completed') {
        filteredTasks = tasks.filter(task => task.completed);
    }

    // O loop forEach
    filteredTasks.forEach(task => {
        const listItem = document.createElement('li');
        listItem.className = `task-item ${task.completed ? 'completed' : ''}`;
        listItem.dataset.id = task.id;
        
        // (Título, Descrição, Toggle, Remover)
        listItem.innerHTML = `
            <div>
                <h3>${task.title}</h3>
                <p>${task.description}</p>
            </div>
            <div>
                <button onclick="toggleTaskCompletion(${task.id})">
                    ${task.completed ? 'Reativar' : 'Concluir'}
                </button>
                <button onclick="removeTask(${task.id})">Remover</button>
            </div>
        `;

        taskList.appendChild(listItem);
    });
}

// 3. Marcar como Concluída
function toggleTaskCompletion(id) {
    const taskIndex = tasks.findIndex(t => t.id === id);
    if (taskIndex > -1) {
        tasks[taskIndex].completed = !tasks[taskIndex].completed;
        saveTasks();
        renderTasks(document.querySelector('#filters .active').dataset.filter);
    }
}

// 4. Remover Tarefa 
function removeTask(id) {
    if (confirm('Tem certeza que deseja remover esta tarefa?')) {
        tasks = tasks.filter(task => task.id !== id);
        saveTasks();
        renderTasks(document.querySelector('#filters .active').dataset.filter);
    }
}

function setupEventListeners() {
    document.getElementById('formulario-de-tarefa').addEventListener('submit', function(e) {
        e.preventDefault();
        const title = document.getElementById('task-title').value.trim();
        const description = document.getElementById('task-description').value.trim();
        
        if (title) { // Validação
            addTask(title, description);
            // Limpa formulário
            this.reset();
        }
    });

    //Botões de Filtro
    document.getElementById('filters').addEventListener('click', function(e) {
        if (e.target.tagName === 'BUTTON') {
            document.querySelectorAll('#filters button').forEach(btn => btn.classList.remove('active'));
            e.target.classList.add('active');
            renderTasks(e.target.dataset.filter);
        }
    });
}

// Iniciar a aplicação
document.addEventListener('DOMContentLoaded', init);