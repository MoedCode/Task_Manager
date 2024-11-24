const API_BASE_URL = "http://localhost:8000/api"; // Replace with your API base URL

// Register a user
async function registerUser(username, password) {
  try {
    const response = await axios.post(`${API_BASE_URL}/register/`, { username, password });
    alert(response.data.message || "Registration successful!");
  } catch (error) {
    alert(error.response.data.error || "Registration failed!");
  }
}

// Login a user
async function loginUser(username, password) {
  try {
    const response = await axios.post(`${API_BASE_URL}/login/`, { username, password });
    localStorage.setItem("token", response.data.token); // Save the token
    alert("Login successful!");
    toggleSections(true); // Show the tasks section
  } catch (error) {
    alert(error.response.data.error || "Login failed!");
  }
}

// Logout a user
function logoutUser() {
  localStorage.removeItem("token");
  toggleSections(false); // Show the login section
  alert("Logged out successfully!");
}

// Toggle sections visibility
function toggleSections(isLoggedIn) {
  document.getElementById("login-section").style.display = isLoggedIn ? "none" : "block";
  document.getElementById("tasks-section").style.display = isLoggedIn ? "block" : "none";
}

export { registerUser, loginUser, logoutUser, toggleSections };
