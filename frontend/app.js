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
app.post("/logout", async (req, res) => {
    try {
        // Clear the token cookie on logout
        res.clearCookie('token');
        res.status(200).json({ message: "Logged out successfully" });
    } catch (error) {
        res.status(error.response?.status || 500).json(error.response?.data || { error: "Server error" });
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`Frontend server running at http://127.0.0.1:${PORT}/`);
});
