// simple_tasker/frontend/public/js/search.js


function maximize(tasId=""){
    taskCard = document.getElementById(`${tasId}`);
    taskCard.classList.add("modal_x")
}
document.addEventListener("DOMContentLoaded", function () {
    // Select all maximize buttons
    const maximizeButtons = document.querySelectorAll(".maximize-btn");

    maximizeButtons.forEach((button) => {
        button.addEventListener("click", function () {
            const cardId = this.getAttribute("data-id");
            const card = document.getElementById(`card-${cardId}`);

            // Check if card is already maximized
            if (card.classList.contains("card-popup")) {
                // Minimize the card
                card.classList.remove("card-popup", "highlight");
                const closeButton = card.querySelector(".close-btn");
                if (closeButton) closeButton.remove();
            } else {
                // Maximize the card
                card.classList.add("card-popup", "highlight");

                // Add a close button to the card
                const closeButton = document.createElement("button");
                closeButton.classList.add("close-btn");
                closeButton.innerHTML = "&times;";
                card.appendChild(closeButton);

                // Close popup on close button click
                closeButton.addEventListener("click", function () {
                    card.classList.remove("card-popup", "highlight");
                    closeButton.remove(); // Remove the close button
                });
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const addTaskBtn = document.getElementById('addTaskBtn');
    const addTaskModal = document.getElementById('addTaskModal');
    const cancelAddTaskBtn = document.getElementById('cancelAddTask');
    const saveAddTaskBtn = document.getElementById('saveAddTask');

    // Open Add Task Modal
    addTaskBtn.addEventListener('click', function() {
        addTaskModal.style.display = 'flex';
    });

    // Close Add Task Modal
    cancelAddTaskBtn.addEventListener('click', function() {
        addTaskModal.style.display = 'none';
    });

    // Add New Task
    saveAddTaskBtn.addEventListener('click', async function() {
        const task = document.getElementById('addTask').value;
        const kickoff = document.getElementById('addKickoff').value;
        const priority = document.getElementById('addPriority').value;

        try {
            const token = getCookie('token'); // Get token from cookies
            const response = await axios.post('/add/task', {
                task,
                kickoff,
                priority
            }, {
                headers: {
                    Authorization: `Bearer ${token}`,
                }
            });

            if (response.status === 200) {
                location.reload(); // Reload the page to display the new task
            }
        } catch (error) {
            console.error('Error adding task:', error);
        } finally {
            addTaskModal.style.display = 'none';
        }
    });

    // Utility to get a cookie value by name
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const deleteBtns = document.querySelectorAll('.delete-btn');
    const updateBtns = document.querySelectorAll('.update-btn');
    const deleteModal = document.getElementById('deleteModal');
    const updateModal = document.getElementById('updateModal');
    let taskToDelete, taskToUpdate;
    // Delete Task
    deleteBtns.forEach(button => {
        button.addEventListener('click', function() {
            taskToDelete = this.getAttribute('data-id');
            deleteModal.style.display = 'flex';
        });
    });


    document.getElementById('confirmDelete').addEventListener('click', async function() {
        try {
            const token = getCookie('token'); // Get token from cookies7

            x  = {
                headers: { Authorization: `Bearer ${token}` },
                data: { task_id: taskToDelete }
            }
            await axios.delete('/delete', {
                headers: { Authorization: `Bearer ${token}` },
                data: { task_id: taskToDelete }
            });
            location.reload();
        } catch (error) {
            console.error('Error deleting task:', error);
        } finally {
            deleteModal.style.display = 'none';
        }
    });

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
            console.log('Cookies:', document.cookie);
            console.log('Token:', token);

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
});
