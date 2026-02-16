// Obtener datos del HTML
const appData = document.getElementById('app-data');
const tasksData = JSON.parse(appData.dataset.tasks || '[]');
const projectsData = JSON.parse(appData.dataset.projects || '[]');
const usersData = JSON.parse(appData.dataset.users || '[]');
const taskUpdateUrl = appData.dataset.taskUpdateUrl;
const taskAddUrl = appData.dataset.taskAddUrl;
const projectUpdateUrl = appData.dataset.projectUpdateUrl;
const projectAddUrl = appData.dataset.projectAddUrl;

// Sistema de tabs
document.querySelectorAll('.tab-button').forEach(btn => {
    btn.addEventListener('click', function() {
        const tabName = this.dataset.tab;
        document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
        document.getElementById(tabName + 'Tab').classList.add('active');
        this.classList.add('active');
    });
});

// Funciones para tareas
function selectTask(id) {
    const task = tasksData.find(t => t.id === id);
    if (!task) return;
    
    document.getElementById('taskTitle').value = task.title || '';
    document.getElementById('taskDescription').value = task.description || '';
    document.getElementById('taskStatus').value = task.status || 'Pendiente';
    document.getElementById('taskPriority').value = task.priority || 'Media';
    document.getElementById('taskProject').value = task.projectId || '';
    document.getElementById('taskAssigned').value = task.assignedTo || '';
    document.getElementById('taskDueDate').value = task.dueDate || '';
    document.getElementById('taskHours').value = task.estimatedHours || '';
    
    const form = document.getElementById('taskForm');
    form.action = taskUpdateUrl.replace('/0', '/' + id);
    form.querySelector('button[type=submit]').textContent = 'Actualizar';
}

function clearTaskForm() {
    document.getElementById('taskTitle').value = '';
    document.getElementById('taskDescription').value = '';
    document.getElementById('taskStatus').value = 'Pendiente';
    document.getElementById('taskPriority').value = 'Media';
    document.getElementById('taskProject').selectedIndex = 0;
    document.getElementById('taskAssigned').selectedIndex = 0;
    document.getElementById('taskDueDate').value = '';
    document.getElementById('taskHours').value = '';
    
    const form = document.getElementById('taskForm');
    form.action = taskAddUrl;
    form.querySelector('button[type=submit]').textContent = 'Agregar';
}

// Funciones para proyectos
function selectProject(id) {
    const p = projectsData.find(pr => pr.id === id);
    if (!p) return;
    
    document.getElementById('projectId').value = p.id;
    document.getElementById('projectName').value = p.name || '';
    document.getElementById('projectDescription').value = p.description || '';
    document.getElementById('projectUpdateBtn').style.display = 'inline';
}

function submitProjectAdd() {
    const form = document.getElementById('projectForm');
    form.action = projectAddUrl;
    form.method = 'post';
    form.submit();
}

function submitProjectUpdate() {
    const id = document.getElementById('projectId').value;
    if (!id) return;
    
    const form = document.getElementById('projectForm');
    form.action = projectUpdateUrl.replace('/0', '/' + id);
    form.method = 'post';
    form.submit();
}

// Hacer funciones accesibles globalmente (si es necesario)
window.selectTask = selectTask;
window.clearTaskForm = clearTaskForm;
window.selectProject = selectProject;
window.submitProjectAdd = submitProjectAdd;
window.submitProjectUpdate = submitProjectUpdate;

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Activar primera tab por defecto
    const firstTab = document.querySelector('.tab-button');
    if (firstTab) firstTab.click();
});