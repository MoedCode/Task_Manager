const API_BASE_URL = "http://localhost:8000/api"; // Replace with your API base URL

// Get tasks
async function fetchTasks() {
  try {
    const token = localStorage.getItem("token");
    const response = await axios.get(`${API_BASE_URL}/tasks/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data.tasks;
  } catch (error) {
    alert("Failed to fetch tasks!");
    return [];
  }
}

// Add a new task
async function addTask(taskName) {
  try {
    const token = localStorage.getItem("token");
    await axios.post(
      `${API_BASE_URL}/tasks/`,
      { name: taskName },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    alert("Task added successfully!");
  } catch (error) {
    alert("Failed to add task!");
  }
}

// Delete a task
async function deleteTask(taskId) {
  try {
    const token = localStorage.getItem("token");
    await axios.delete(`${API_BASE_URL}/tasks/${taskId}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    alert("Task deleted successfully!");
  } catch (error) {
    alert("Failed to delete task!");
  }
}

export { fetchTasks, addTask, deleteTask };
