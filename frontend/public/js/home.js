// simple_tasker/frontend/public/js/search.js

let xx = `<svg xmlns="http://www.w3.org/2000/svg" width="2vw" height="2vw" viewBox="0 0 24 24"><path fill="#e11d48" d="m8 16.708l-3.246 3.246q-.14.14-.344.15t-.364-.15t-.16-.354t.16-.354L7.292 16H4.5q-.213 0-.356-.144T4 15.499t.144-.356T4.5 15h3.692q.343 0 .576.232t.232.576V19.5q0 .213-.144.356T8.499 20t-.356-.144T8 19.5zm8 0V19.5q0 .213-.144.356t-.357.144t-.356-.144T15 19.5v-3.692q0-.344.232-.576t.576-.232H19.5q.213 0 .356.144t.144.357t-.144.356T19.5 16h-2.792l3.246 3.246q.14.14.15.345q.01.203-.15.363t-.354.16t-.354-.16zM7.292 8L4.046 4.754q-.14-.14-.15-.344t.15-.364t.354-.16t.354.16L8 7.292V4.5q0-.213.144-.356T8.501 4t.356.144T9 4.5v3.692q0 .343-.232.576T8.192 9H4.5q-.213 0-.356-.144T4 8.499t.144-.356T4.5 8zm9.416 0H19.5q.213 0 .356.144t.144.357t-.144.356T19.5 9h-3.692q-.344 0-.576-.232T15 8.192V4.5q0-.213.144-.356T15.501 4t.356.144T16 4.5v2.792l3.246-3.246q.14-.14.345-.15q.203-.01.363.15t.16.354t-.16.354z"/></svg>`
let yy  = ` <svg xmlns="http://www.w3.org/2000/svg" width="2.5vw" height="2.5vw" viewBox="0 0 24 24"><path fill="#0284c7" d="M6.4 19H8q.425 0 .713.288T9 20t-.288.713T8 21H4q-.425 0-.712-.288T3 20v-4q0-.425.288-.712T4 15t.713.288T5 16v1.6l2.4-2.4q.275-.275.7-.275t.7.275t.275.7t-.275.7zm11.2 0l-2.4-2.4q-.275-.275-.275-.7t.275-.7t.7-.275t.7.275l2.4 2.4V16q0-.425.288-.712T20 15t.713.288T21 16v4q0 .425-.288.713T20 21h-4q-.425 0-.712-.288T15 20t.288-.712T16 19zM5 6.4V8q0 .425-.288.713T4 9t-.712-.288T3 8V4q0-.425.288-.712T4 3h4q.425 0 .713.288T9 4t-.288.713T8 5H6.4l2.4 2.4q.275.275.275.7t-.275.7t-.7.275t-.7-.275zm14 0l-2.4 2.4q-.275.275-.7.275t-.7-.275t-.275-.7t.275-.7L17.6 5H16q-.425 0-.712-.287T15 4t.288-.712T16 3h4q.425 0 .713.288T21 4v4q0 .425-.288.713T20 9t-.712-.288T19 8z"/></svg>`
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
            button.innerHTML = xx

            this.addEventListener("click", ()=>{
                this.innerHTML = xx
            })

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
                this.addEventListener("click", ()=>{
                    this.innerHTML = yy
                })

                closeButton.addEventListener("click",()=>{
                    this.innerHTML = yy
                    this.addEventListener("click", ()=>{
                        this.innerHTML = xx
                    })
                })
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
