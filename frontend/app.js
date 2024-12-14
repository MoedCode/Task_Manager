const express = require("express");
const axios = require("axios");
const bodyParser = require("body-parser");
const path = require("path");
const cookieParser = require("cookie-parser");
const morgan = require("morgan"); // HTTP request logger
const fs = require("fs"); // File system module for logging
const { error } = require("console");

/*                                                  GLOBALS                                                         */

function DEBUG(input = "", linChar = "") {
    // Get the stack trace
    const stack = new Error().stack;
    const stackLines = stack.split("\n");

    // Extract the caller's line (stack[2] gives the caller information)
    const callerInfo = stackLines[2].trim();

    // Parse the file name and line number
    const match = callerInfo.match(/at (.+):(\d+):(\d+)/);
    let fileInfo = "Unknown location";
    if (match) {
        const fileName = match[1].split('/').pop(); // Get the file name
        const lineNumber = match[2]; // Get the line number
        fileInfo = `${fileName}, line ${lineNumber}`;
    }

    // Handle input
    let formattedInput;
    if (typeof input === "object") {
        const seen = new WeakSet(); // To track circular references
        try {
            formattedInput = JSON.stringify(input, (key, value) => {
                if (typeof value === "object" && value !== null) {
                    if (seen.has(value)) {
                        return "[Circular]"; // Mark circular references
                    }
                    seen.add(value);
                }
                return value;
            }, 2);
        } catch (error) {
            formattedInput = "[Unserializable object]";
        }
    } else {
        formattedInput = input; // Use as-is for non-object types
    }

    // Log the debug message
    console.log(`${fileInfo} ::${linChar} ${formattedInput}`);
}


const app = express();
const PORT = 5001;

// Base URL for Python backend server
const PYTHON_SERVER_URL = "http://127.0.0.1:5000";

// Create a write stream for logging to a file
const accessLogStream = fs.createWriteStream(path.join(__dirname, "access.log"), {
    flags: "a", // Append mode
});

// Middleware
app.use(
    morgan("combined", {
        stream: accessLogStream, // Log requests to access.log
    })
);

app.use(bodyParser.json());
app.use(cookieParser()); // For cookie handling
app.use(express.static(path.join(__dirname, "public/css"))); // Serve static files
app.use(express.static(path.join(__dirname, 'public')));

app.set("view engine", "ejs"); // Set EJS as template engine
app.set("views", path.join(__dirname, "views")); // Set views directory
app.use('/public', express.static(path.join(__dirname, 'public')));
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
                Authorization: `Bearer ${token}`, // Pass the token in Authorization header
            },
        });

        // Check if the response contains task data
        if (response.data && Array.isArray(response.data)) {
            res.render("home", { tasks: response.data });
        } else {
            res.status(500).json({ error: "Invalid response structure from backend." });
        }
    } catch (error) {
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
        if (response.data.token) {
            res.cookie("token", response.data.token, { httpOnly: false }); // Store token in httpOnly cookie
            console.log(`/api/login/ try ${req.body}`);

        }

        res.status(response.status).json(response.data);
    } catch (error) {
        console.log(`/api/login/ catch `,req.body);
        res.status(error.response?.status || 500).json(error.response?.data || { error: "Server error" });
    }
});

// Logout User wsl.exe --updat
app.get("/logout", (req, res) => {
    res.clearCookie("token"); // Clear the token cookie
    res.redirect("/login");
});
app.delete("/delete", async (req, res) => {
    const token = req.cookies.token; // Extract user token from cookie
    const taskId = req.body.task_id;

    if (!token || !taskId) {
        return res.status(400).json({ error: "Token or Task ID missing" });
    }

    try {
        // Forward the request to the Python backend
        const response = await axios.post(
            `${PYTHON_SERVER_URL}/api/delete/`,
            { task_id: taskId },
            { headers: { Authorization: `Bearer ${token}` } }
        );

        res.status(response.status).json(response.data); // Respond with Python server response
    } catch (error) {
        res.status(error.response?.status || 500).json(error.response?.data || { error: "Delete failed" });
    }
});
app.delete("/delete/user", async (req, res) => {
    DEBUG(req.cookies.token)
    DEBUG(req.body)
    const token = req.cookies.token; // Extract user token from cookie
    const user = req.body.user;
    let msg = ""
    msg += !user ? "messing user data. " :"";
    msg += !token ? "no token provided. " :""
    if (msg) {
        DEBUG(msg)

        return res.status(400).json({ error: msg });
    }

    try {
        // Forward the request to the Python backend
        const response = await axios.post(
            `${PYTHON_SERVER_URL}/api/delete/user/`,
            { user: user },
            { headers: { Authorization: `Bearer ${token}` } }
        );

        res.status(response.status).json(response.data); // Respond with Python server response
    } catch (error) {
        DEBUG(error)
        res.status(error.response?.status || 500).json(error.response?.data || { error: "Delete failed" });
    }
});
app.put("/update", async (req, res) => {

    const token = req.cookies.token || req.headers.authorization?.split(' ')[1];
    const { lock_for, update_data,  category} = req.body;

    if (!token || !lock_for || !update_data) {
        DEBUG()
        return res.status(401).json({ error: "Unauthorized: Invalid token or request data" });
    }
    const updateData = {
        lock_for:lock_for, update_data:update_data, category:category
    }
    console.log("\n::lock_for\n", lock_for);
    try {
        const response = await axios.post(
            `${PYTHON_SERVER_URL}/api/update/`,
            updateData,
            { headers: { Authorization: `Bearer ${token}` } }

        );
        // if (response.data[0])
        res.status(response.status).json(response.data);
    } catch (error) {
        console.error('Error from Python backend:', error.response?.data || error.message);
        res.status(error.response?.status || 500).json(error.response?.data || { error: "Update failed" });
    }
});
// Add Task Endpoint (POST)
app.post("/add/task", async (req, res) => {
    const token = req.cookies.token; // Retrieve the token from the cookie
    if (!token) {
        return res.status(401).json({ error: "Unauthorized" });
    }

    try {
        const { task, kickoff, priority } = req.body;

        // Make the POST request to the Python server to add the task
        const response = await axios.post(`${PYTHON_SERVER_URL}/api/add/`, {
            task,
            kickoff,
            priority
        }, {
            headers: {
                Authorization: `Bearer ${token}`, // Pass the token in Authorization header
            }
        });

        res.status(response.status).json(response.data); // Return the response from Python server
    } catch (error) {
        console.error("Error adding task:", error);
        res.status(error.response?.status || 500).json(error.response?.data || { error: "Server error" });
    }
});
app.post("/search", async(req, res)=>{
    const token = req.cookies.token;
    if (!token){
        return res.status(401).json({error:"unauthorized"})
    }
try{
    const {category, method, query }  = req.body
    const response = await axios.post(`${PYTHON_SERVER_URL}/api/search/`,
        {category, method, query}, {headers: {Authorization: `Bearer ${token}`,} }
    )
    res.status(response.status).json(response.data)
} catch(error){
    console.log(`Error in search end point : ${error}`);
    res.status(error.response?.status || 500).json(error.response?.data || { error: "Server error" });

}
})
app.get("/search", async (req, res) => {
    const token = req.cookies.token;
    if (!token) {
        return res.redirect("/login");
    }
    try {
        const result = await auth(token);
        if (!result[0]) {
            console.error(result[1]);
            return res.redirect("/login");
        }
        const data = Array.isArray(result) ? result.slice(1) : [];
        // console.log(data);
        res.render("search", { user:data[1], searchURL:PYTHON_SERVER_URL + "/api/search/" });
    } catch (error) {
        console.error(error);
        res.status(500).send("Internal Server Error");
    }
});
app.get("/api/auth", async (req, res) => {
    const token = req.cookies.token;
    if (!token) {
        return res.status(401).json({ authorized: false, message: "Not logged in" });
    }
    try {
        const result = await auth(token);
        if (!result[0]) {
            console.error(result[1]);
            return res.status(401).json({ authorized: false, message: "Invalid token" });
        }
        DEBUG(token)
        // DEBUG(result)
        return res.status(200).json(result);

    } catch (error) {
        console.error(error);
        res.status(500).send("Internal Server Error");
    }
});

app.get("/test", (req, res)=>{
    const token = req.cookies.token;

})

// New endpoint to forward requests to Python backend
app.post("/search/forward", async (req, res) => {
    const { category, method, query } = req.body;

    if (!category || !method || !query) {
        return res.status(400).json({ error: "Missing required fields: category, method, or query" });
    }

    try {
        // Forward the search request to the Python backend
        const response = await axios.post(`${PYTHON_SERVER_URL}/api/search/`, {
            category,
            method,
            query,
        }, {
            headers: {
                Authorization: req.headers.authorization,
            },
        });

        res.status(response.status).json(response.data);
    } catch (error) {
        console.error("Error forwarding search request:", error.response?.data || error.message);
        res.status(error.response?.status || 500).json(error.response?.data || { error: "Search forward failed" });
    }
});
app.post("/update/user", async (req, res) => {
    const token = req.cookies.token;
    if (!token) {
        return res.status(401).json({ authorized: false, message: "Not logged in" });
    }
    const user =  req?.data || {}
    const password = user?.password || ""
    const userId  = user?.id || ""

    let msg = "";
    msg += !user ? "no valid user data provided, ":"";
    msg += !password ? "null user password " : "";
    msg += !userId ? "null user id " : "";
    if (msg) {
        return res.status(400).json({ error: msg });
    }

    try {
        // Forward the search request to the Python backend
        const response = await axios.post(`${PYTHON_SERVER_URL}/api/search/`, {
            category,
            method,
            query,
        }, {
            headers: {
                Authorization: req.headers.authorization,
            },
        });

        res.status(response.status).json(response.data);
    } catch (error) {
        console.error("Error forwarding search request:", error.response?.data || error.message);
        res.status(error.response?.status || 500).json(error.response?.data || { error: "Search forward failed" });
    }
});




async function auth(token = "") {
    headers =             {
        headers: {
            Authorization: "Bearer " + token,
        },
    }
    // console.log(headers);
    try {
        const response = await axios.get(
            `${PYTHON_SERVER_URL}/api/auth/`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );
        // Check if the status is not 200 (though Axios throws errors for non-2xx)
        if (response.status !== 200) {
            return [false, response.data.error || "Unexpected error occurred"];
        }

        // Return success response
        return [true, response.data];
    } catch (error) {
        // Handle network or server errors
        return [false, error.response?.data?.error || error.message];
    }
}

async function testAuth() {
    try {
        const authResult = await auth("dfc0a909623f019bfc60dee1d3d0775366f60bcd9cab3f29b117ae38116dfa14");
        // console.log(`from auth function`, authResult);
    } catch (error) {
        console.error(`Error in auth function:`, error);
    }
}

// testAuth();

// Start server
app.listen(PORT, () => {
    console.log(`Frontend server running at http://127.0.0.1:${PORT}/`); // Message in terminal
});
