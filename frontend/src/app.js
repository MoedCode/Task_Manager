import { registerUser, loginUser, logoutUser, toggleSections } from "./auth.js";
import { fetchTasks, addTask, deleteTask } from "./tasks.js";

document.getElementById("register-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("reg-username").value;
  const password = document.getElementById("reg-password").value;
  await registerUser(username, password);
});

document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;
  await loginUser(username, password);
});

document.getElementById("logout-button").addEventListener("click", () => {
  logoutUser();
});

document.getElementById("add-task-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const taskName = document.getElementById("task-name").value;
  await addTask(taskName);
  renderTasks();
});

async function renderTasks() {
  const tasks = await fetchTasks();
  const taskList = document.getElementById("tasks-list");
  taskList.innerHTML = "";
  tasks.forEach((task) => {
    const taskItem = document.createElement("li");
    taskItem.textContent = task.name;
    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", () => deleteTask(task.id));
    taskItem.appendChild(deleteButton);
    taskList.appendChild(taskItem);
  });
}

// Initialize the app
if (localStorage.getItem("token")) {
  toggleSections(true);
  renderTasks();
} else {
  toggleSections(false);
}
