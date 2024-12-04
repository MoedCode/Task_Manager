// simple_tasker/frontend/public/js/search.js

const defaultSearchURL = "http://127.0.0.1:5001/search/forward";

function updateAttributes() {
    const category = document.getElementById("category").value;
    const attributeSelect = document.getElementById("attribute");

    if (category === "tasks") {
        attributeSelect.innerHTML = `
            <option value="task">Task</option>
            <option value="kickoff">Kickoff</option>
        `;
    }
}

function updateInputType() {
    const attribute = document.getElementById("attribute").value;
    const inputField = document.getElementById("value");

    if (attribute === "kickoff") {
        inputField.type = "datetime-local";
        inputField.placeholder = "Select a date and time";
    } else {
        inputField.type = "text";
        inputField.placeholder = "Enter a value";
    }
}

// Function to get a specific cookie by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function performSearch() {
    const searchBody = getRequestBody();
    const headers = getRequestHeaders();
    const resultsContainer = document.getElementById("results");

    try {
        const response = await axios.post(defaultSearchURL, searchBody, { headers });

        if (response.data.results) {
            resultsContainer.innerHTML = response.data.results
                .map(result => `
                    <div>
                        <p><strong>creation time:</strong> ${result.creation_time}</p>
                        <p><strong>Task:</strong> ${result.task}</p>
                        <p><strong>Kickoff:</strong> ${result.kickoff}</p>
                        <p><strong>Priority:</strong> ${result.priority}</p>
                        <p><strong>id :</strong> ${result.id}</p>
                       <button class="delete-btn" data-id="${result.id}"> Delete Task </button>
                       <button class="update-btn"data-id="${result.id}"> updateTask </button>
                    </div>
                    <hr>
                `).join("");

        } else {
            resultsContainer.innerHTML = "<p class='error'>No matching rows found.</p>";
        }
    } catch (error) {
        resultsContainer.innerHTML = `<p class='error'>Error: ${error.response?.data?.error || "An error occurred"}</p>`;
    }
}

function getRequestBody() {
    const category = document.getElementById("category").value;
    const method = document.getElementById("method").value;
    const attribute = document.getElementById("attribute").value;
    const value = document.getElementById("value").value;

    return {
        category,
        method,
        query: {
            [attribute]: value,
            user_id: "f355aeb1-b656-4a02-927a-898b9119a4fc" // Example user_id
        }
    };
}

function getRequestHeaders() {
    const token = getCookie('token'); // Get token from cookies
    if (!token) {
        alert('Authorization token is missing!');
        throw new Error('Authorization token not found in cookies');
    }
    return {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
    };
}

// DEBUG Button Click Listener
document.getElementById('debugBtn').addEventListener('click', () => {
    const debugOutput = document.getElementById('debugOutput');
    const debugInfo = document.getElementById('debugInfo');

    // Get dynamic request data
    const requestBody = getRequestBody();
    const requestHeaders = getRequestHeaders();

    // Format the Request Details
    const requestDetails = {
        url: defaultSearchURL, // Include the URL
        headers: requestHeaders,
        body: requestBody
    };

    // Display Debug Info
    debugInfo.textContent = JSON.stringify(requestDetails, null, 2);
    debugOutput.style.display = 'block';
});
function delete_task(taskId){

    if (!taskId){
        resultsContainer.innerHTML += "<p><strong>Error: </strong> No task id </p>"
    }

}
