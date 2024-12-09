// simple_tasker/frontend/public/js/search.js

const defaultSearchURL = "http://127.0.0.1:5001/search/forward";

const resultsContainer = document.getElementById("results");
const value = document.getElementById("value").value;
const  xx = value
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
    // const resultsContainer = document.getElementById("results");

    try {
        const response = await axios.post(defaultSearchURL, searchBody, { headers });

        if (response.data.results) {
            resultsContainer.innerHTML = response.data.results
                .map(result => `
                    <div class="card ">
                        <p><strong>creation time:</strong> ${result.creation_time}</p>
                        <p><strong>Task:</strong> ${result.task}</p>
                        <p><strong>Kickoff:</strong> ${result.kickoff}</p>
                        <p><strong>Priority:</strong> ${result.priority}</p>
                        <p><strong>id :</strong> ${result.id}</p>
                        <div class="search-res-btn">
                       <button class="delete-btn " onclick="deleteTask('${result.id}')"> Delete   </button>
                       <button class="update-btn" onclick="updateTask(
                       '${result.id}',' ${result.task}', '${result.kickoff}', '${result.priority}',
                       )" > Update</button>
                       </div>
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
    const  xx = value
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
function deleteTask(taskId){

    if (!taskId){
        resultsContainer.innerHTML += "<p><strong>Error: </strong> No task id </p>"
    }
    const deleteModal = document.getElementById('deleteModal');
    deleteModal.style.display = 'flex';
    document.getElementById('cancelDelete').addEventListener('click', function() {
        deleteModal.style.display = 'none';
    });
    document.getElementById('confirmDelete').addEventListener('click', async function() {
        try {
            const token = getCookie('token'); // Get token from cookies7

            await axios.delete('/delete', {
                headers: { Authorization: `Bearer ${token}` },
                data: { task_id: taskId }
            });
            performSearch()
        } catch (error) {
            console.error('Error deleting task:', error);
        } finally {
            deleteModal.style.display = 'none';
        }
    });

}
function updateTask(id,task, kickoff, priority){
    const updateModal = document.getElementById('updateModal');
    // const updateBtns = document.querySelectorAll('.update-btn');
    let taskToUpdate;
    updateModal.style.display = 'flex';


            taskToUpdate = {
                id:id,
                task:task,
                kickoff:kickoff,
                priority:priority
            };

            document.getElementById('task').value =task.trim();
            document.getElementById('kickoff').value =kickoff
            document.getElementById('priority').value =priority
            updateModal.style.display = 'flex';
            document.getElementById('saveUpdate').addEventListener('click', async function() {
                try {
                    const token = getCookie('token'); // Get token from cookies
                    const updatedData = {
                        category: "tasks",
                        lock_for: { id: taskToUpdate.id },
                        update_data: {
                            task: document.getElementById('task').value,
                            kickoff: document.getElementById('kickoff').value,
                            priority: document.getElementById('priority').value
                        }
                    };

                    await axios.put('/update', updatedData, {
                        headers: { Authorization: `Bearer ${token}` },
                        withCredentials: true // Ensure cookies are sent
                    });
                    window.location.reload()

                } catch (error) {
                    console.error('Error updating task:', error);
                } finally {
                    updateModal.style.display = 'none';
                }
            });
    console.log(id,task, kickoff, priority, taskToUpdate);
    document.getElementById('cancelUpdate').addEventListener('click', function() {
        updateModal.style.display = 'none';
    });
    return
}
document.getElementById("value").value = xx
performSearch()
