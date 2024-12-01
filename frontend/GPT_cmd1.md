now i face unauthorized error whhhhhhhhyyyyyyy

```console
undefined
xhr.js:195


        PUT http://127.0.0.1:5001/update 401 (Unauthorized)
(anonymous) @ xhr.js:195
xhr @ xhr.js:15
_t @ dispatchRequest.js:51
value @ Axios.js:178
(anonymous) @ Axios.js:40
p @ axios.min.js:1
(anonymous) @ axios.min.js:1
(anonymous) @ axios.min.js:1
p @ axios.min.js:1
a @ axios.min.js:1
(anonymous) @ axios.min.js:1
(anonymous) @ axios.min.js:1
(anonymous) @ Axios.js:63
(anonymous) @ Axios.js:217
(anonymous) @ bind.js:5
(anonymous) @ home:471
home:476  Error updating task: me {message: 'Request failed with status code 401', name: 'AxiosError', code: 'ERR_BAD_REQUEST', config: {…}, request: XMLHttpRequest, …}
(anonymous) @ home:476
```
update portion in script

```js

        document.getElementById('cancelDelete').addEventListener('click', function() {
            deleteModal.style.display = 'none';
        });

        // Update Task
        updateBtns.forEach(button => {
            button.addEventListener('click', function() {
                taskToUpdate = {
                    id: this.getAttribute('data-id'),
                    task: this.getAttribute('data-task'),
                    kickoff: this.getAttribute('data-kickoff'),
                    priority: this.getAttribute('data-priority')
                };
                document.getElementById('task').value = taskToUpdate.task;
                document.getElementById('kickoff').value = taskToUpdate.kickoff;
                document.getElementById('priority').value = taskToUpdate.priority;
                updateModal.style.display = 'flex';
            });
        });

        document.getElementById('saveUpdate').addEventListener('click', async function() {
            try {
                const token = getCookie('token'); // Get token from cookies
                console.log(token);
                const updatedData = {
                    lock_for: { id: taskToUpdate.id },
                    update_data: {
                        task: document.getElementById('task').value,
                        kickoff: document.getElementById('kickoff').value,
                        priority: document.getElementById('priority').value
                    }
                };
                await axios.put('/update', updatedData, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                location.reload();
            } catch (error) {
                console.error('Error updating task:', error);
            } finally {
                updateModal.style.display = 'none';
            }
        });

        document.getElementById('cancelUpdate').addEventListener('click', function() {
            updateModal.style.display = 'none';
        });

        // Utility to get a cookie value by name
        function getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        }

```
update endpoint in app.js

```
app.put("/update", async (req, res) => {
    const token = req.cookies.token; // Extract user token from cookie
    const { lock_for, update_data } = req.body;
    console.log(`token ${token} request bdy ${req.body}`);
    if (!token || !lock_for?.id || !update_data) {
        return res.status(400).json({ error: "Invalid update request data" });
    }

    try {
        // Forward the update request to the Python backend
        const response = await axios.post(
            `${PYTHON_SERVER_URL}/api/update/`,
            { lock_for, update_data },
            { headers: { Authorization: `Bearer ${token}` } }
        );

        res.status(response.status).json(response.data); // Respond with Python server response
    } catch (error) {
        res.status(error.response?.status || 500).json(error.response?.data || { error: "Update failed" });
    }
});

```