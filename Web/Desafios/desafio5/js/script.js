// Inicialização do array de tarefas
let tasks = [];

// Função para renderizar a lista de tarefas na tabela
function renderTasks(filteredTasks = tasks) {
    const taskList = document.getElementById('tasks');
    taskList.innerHTML = ''; // Limpa a tabela antes de renderizar

    filteredTasks.forEach((task, index) => {
        const taskRow = document.createElement('tr');
        taskRow.innerHTML = `
            <td>${task.title}</td>
            <td>${task.description}</td>
            <td>
                <button class="edit-btn" onclick="editTask(${index})">Editar</button>
                <button class="delete-btn" onclick="deleteTask(${index})">Excluir</button>
            </td>
        `;
        taskList.appendChild(taskRow);
    });
}

// Função para adicionar uma nova tarefa
function addTask() {
    const title = document.getElementById('task-title').value.trim();
    const description = document.getElementById('task-desc').value.trim();

    if (title && description) {
        tasks.push({ title, description });
        renderTasks();
        document.getElementById('task-title').value = '';
        document.getElementById('task-desc').value = '';
    } else {
        alert('Por favor, preencha todos os campos!');
    }
}

// Função para editar uma tarefa existente
function editTask(index) {
    const newTitle = prompt('Novo título da tarefa:', tasks[index].title);
    const newDescription = prompt('Nova descrição da tarefa:', tasks[index].description);

    if (newTitle && newDescription) {
        tasks[index].title = newTitle;
        tasks[index].description = newDescription;
        renderTasks();
    }
}

// Função para excluir uma tarefa
function deleteTask(index) {
    tasks.splice(index, 1);
    renderTasks();
}

// Função para filtrar tarefas
function filterTasks() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const filteredTasks = tasks.filter(task => 
        task.title.toLowerCase().includes(searchTerm) || 
        task.description.toLowerCase().includes(searchTerm)
    );
    renderTasks(filteredTasks);
}

// Event listener para o botão de adicionar tarefa
document.getElementById('add-task-btn').addEventListener('click', addTask);

// Event listener para o campo de busca
document.getElementById('search-input').addEventListener('input', filterTasks);
