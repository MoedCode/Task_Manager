# requirements
    1- i want delete button on each task ..to prevent accidental  deletion do  confirmation step  be displayed
    but do not window alert
    2- also add update button that display fields for task  task data that user concern to update
    (string) `task:`, (string)`kickoff:`  , (int)`priority:`  but kik of is date time filed sopwith specific format cant be change
    example `2025-01-30 00:28:00` so make a smart date filed input
# data you need to know
- delete endpoint url `/api/delete/`
- update url `/api/update/`
- delete request data example
```json
{"task_id":"4066176f-523e-46f5-91b3-d22e939a5f0a"}
```
- update url `/api/update/`
- update request data example
```json
{
"category": "tasks",
"lock_for": {
    "id": "ee241eb9-55ac-4e4a-9b8f-0d90257d993c"
},
"update_data": {
    "kickoff": "2025-01-30 00:28:00",
    "priority": 1,
    "task": "lose wight pro1"
}
}
```
***Note - category, must be allays tasks in case of request to update task

# front end code
app.js
```js
const express = require("express");
const axios = require("axios");
const bodyParser = require("body-parser");
const path = require("path");
const cookieParser = require("cookie-parser");

const app = express();
const PORT = 5001;

// Base URL for Python backend server
const PYTHON_SERVER_URL = "http://127.0.0.1:5000";

// Middleware
app.use(bodyParser.json());
app.use(cookieParser()); // For cookie handling
app.use(express.static(path.join(__dirname, "public/css"))); // Serve static files
app.set("view engine", "ejs"); // Set EJS as template engine
app.set("views", path.join(__dirname, "views")); // Set views directory

// Utility function to format time
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString(); // Customize as needed for desired format
}

// Routes
// Home Page (protected)
app.get("/home", async (req, res) => {
    const token = req.cookies.token; // Retrieve the token from the cookie
    if (!token) {
        return res.redirect("/login"); // Redirect to login if no token
    }

    try {
        // Make request to /api/home using the token
        const response = await axios.get(`${PYTHON_SERVER_URL}/api/home/`, {
            headers: {
                Authorization: `Bearer ${token}` // Pass the token in Authorization header
            }
        });

        // Check if the response contains task data
        if (response.data && Array.isArray(response.data)) {
            // Pass the entire task objects (no formatting needed for now)
            res.render("home", { tasks: response.data });
        } else {
            // Handle cases where the response data is missing tasks or is not an array
            res.status(500).json({ error: "Invalid response structure from backend." });
        }
    } catch (error) {
        // Redirect to login page if token is missing or invalid
        if (error.response?.status === 401) {
            console.log(`Error: ${error.response.data?.error || "Unauthorized"}`);
            return res.redirect("/login"); // Redirect to login on token error
        }

        res.status(error.response?.status || 500).json(error.response?.data || { error: "Server error" });
    }
});

// Register User
app.get("/register", (req, res) => {
    res.render("register");
});

app.post("/api/register/", async (req, res) => {
    try {
        const response = await axios.post(`${PYTHON_SERVER_URL}/api/register/`, req.body);
        res.status(response.status).json(response.data);
    } catch (error) {
        res.status(error.response?.status || 500).json(error.response?.data || { error: "Server error" });
    }
});

// Login User
app.get("/login", (req, res) => {
    res.render("login");
});

app.post("/api/login/", async (req, res) => {
    try {
        const response = await axios.post(`${PYTHON_SERVER_URL}/api/login/`, req.body);

        // Save the token in the cookie upon successful login
        if (response.data.token) {
            res.cookie('token', response.data.token, { httpOnly: true }); // Store token in httpOnly cookie
        }

        res.status(response.status).json(response.data);
    } catch (error) {
        res.status(error.response?.status || 500).json(error.response?.data || { error: "Server error" });
    }
});

// Logout User
app.get("/logout", async (req, res) => {
    try {
        // Retrieve the token from the cookie
        const token = req.cookies.token;
        if (!token) {
            return res.redirect("/login"); // Redirect to login if no token
        }

        // Make a POST request to the Python server with the token in the header
        const response = await axios.post(
            `${PYTHON_SERVER_URL}/api/logout/`,
            {}, // No body required for logout
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );

        // Clear the token cookie on successful logout
        res.clearCookie("token");
        res.redirect("/login"); // Redirect to login page
    } catch (error) {
        console.error("Error logging out:", error.response?.data || error.message);

        // Handle failure, e.g., redirect to login or show an error message
        res.clearCookie("token"); // Clear token cookie even if logout fails
        res.redirect("/login"); // Redirect to login page
    }
});


// Start server
app.listen(PORT, () => {
    console.log(`Frontend server running at http://127.0.0.1:${PORT}/`);
});

```
home.ejs

```ejs
<%- include('partials/header') %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <link rel="stylesheet" href="../public/css/style.css"> <!-- The leading slash ensures it's relative to the root of the server -->


    <title>Document</title>
</head>
<body>
 <h1>Welcome to Your Tasker</h1>
<h2>Your Tasks:</h2>

<div class="task-container">
    <% tasks.forEach(function(task) { %>
        <div class="card">
            <h3>Task:</h3>
            <% Object.keys(task).forEach(function(key) { %>
                <div class="task-detail">
                    <strong><%= key %>:</strong> <%= task[key] %>
                </div>
            <% }); %>
        </div>
    <% }); %>
</div>

<style>

    /* Ensure all cards are displayed nicely */
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    margin: 0;
    padding: 0;
}

/* Container for all the task cards */
.task-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
    padding: 20px;
}

/* Card style */
.card {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 300px;
    padding: 15px;
    margin: 10px;
    transition: transform 0.3s ease;
}

/* Hover effect for cards */
.card:hover {
    transform: scale(1.05);
}

/* Task detail style */
.task-detail {
    margin-bottom: 10px;
    font-size: 16px;
}

.task-detail strong {
    color: #333;
}

h3 {
    font-size: 24px;
    margin-bottom: 10px;
    text-align: center;
    color: #333;
}

</style>
</body>
</html>


```