


const toggleSidebarButton = document.getElementById("toggle-sidebar");
const sidebar = document.getElementById("sidebar");
const overlay = document.getElementById("overlay");

// Toggle sidebar and overlay
toggleSidebarButton.addEventListener("click", () => {
    sidebar.classList.toggle("active");
    overlay.classList.toggle("active");
});

// Close sidebar when clicking on overlay
overlay.addEventListener("click", () => {
    sidebar.classList.remove("active");
    overlay.classList.remove("active");
});

// user Profile
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
function getRequestHeaders() {
    const token = getCookie('token'); // Get token from cookies
    if (!token) {
        //alert('Authorization token is missing!');
        return  [false, 'Authorization token not found in cookies']
    }
    return {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
    };
}
token = getCookie('token')
const reqHeaders =  {
    headers: { Authorization: `Bearer ${token}` },
    withCredentials: true // Ensure cookies are sent

}
async function profile() {
        /* user modal */
        let user_obj = {}
        const userModal = document.getElementById('userModal');
        const userModal_h3 = document.getElementById("userModal-h3");
        const  userUpdate = document.getElementById('user-update');
        const  userModUpdate = document.getElementById("modal-body-update");
        const  userModView = document.getElementById("user-modal-view");
            // sub element
        const usernameView  = document.getElementById("username-view")
        const emailView = document.getElementById("email-view")
        const usernameUpdate = document.getElementById("update-username")
        const emailUpdate = document.getElementById("update-email")
        const passwordCheck = document.getElementById("check-password")
        const passwordUpdate = document.getElementById("update-password")
        const passwordUpdate2 = document.getElementById("update-password2")
        const useUpdateErr = document.getElementById("user-update-err")
                //user delete
        const userModDelete =  document.getElementById("user-modal-delete")
        const userDelBtn = document.getElementById("user-delete-btn")
        const userDel_h3 = document.getElementById("delete-user-h3")
        const userDel_err = document.getElementById("delete-user-error")
        const userDelCancel = document.getElementById("user-delete-cancel")
        const userDelConf = document.getElementById("user-delete-conf")
        const userDelPWD = document.getElementById("user-delete-password")
        const useless = document.getElementById("useless-btn")
    try {
        const response = await fetch('/api/auth', {
            method: 'GET',
            credentials: 'include', // Include cookies in the request
        });

        if (!response.ok) {
            throw new Error('Not authorized');
        }
        const result = await response.json();

        const profBtn = document.getElementById("user-btn");
        if (!result[0]) {
            profBtn.innerHTML = "Not authorized";
            setTimeout(() => {
                profBtn.innerHTML = "Profile";
            }, 3000);
            return
        }
        let user =  result[1][1]
        user_obj = user





        usernameUpdate.value = user.username
        emailUpdate.value = user.email
        usernameView.innerHTML = user.username
        emailView.innerHTML = user.email
        function usrUpErr (msg="", time=3000){
            useUpdateErr.innerHTML = msg
            setTimeout(() => {
            useUpdateErr.innerHTML = ""

            }, time);
        }

        document.getElementById('cancelUpdate-user').addEventListener('click', function() {
            userModal.style.display = 'none';
            return
        });
        document.getElementById('user-update').addEventListener('click', function() {
            userModUpdate.style.display = 'flex';
            userModView.style.display = 'none';
            userModal_h3.innerHTML = "Update Your Data"
        });

        document.getElementById('saveUpdate-user').addEventListener('click', async  function () {
            const token = getCookie('token');
            console.log(token);
           const  username = usernameUpdate.value.trim()
           const  email = emailUpdate.value.trim()
            const PWD = passwordCheck.value
            const PWD1 = passwordUpdate.value
            const PWD2 = passwordUpdate2.value
            if ( (PWD1  ||  PWD2) && PWD1 !== PWD2){
                usrUpErr(`password not match `)
                return
            }


            const userUpdateObj = {
                username:username,
                email:email,


            }
            if ( (PWD1  && PWD2) && ( PWD1 == PWD2) ){
                userUpdateObj.password = PWD1
            }
            const lock_for  = {
                username:user.username, password:PWD
            }
            usrUpErr(JSON.stringify(userUpdateObj), 500000)
            reqBody = {
                    category:"users",
                    lock_for:lock_for,
                    update_data: userUpdateObj,
            }
            try{
            const response =await axios.put('/update', reqBody,reqHeaders);
            if (response.data.status == "Error")
            {
                usrUpErr(JSON.stringify(response.data), 30000)
                console.error(response.data)
                return
            }
            else {
            //
            if ("password" in userUpdateObj)
                window.location.reload()
            userModal.style.display  = 'none';
            profile()

        }
        } catch(error){
            console.log("axios Error", error);
        }





        });


        userModal.style.display = 'flex';
        userModView.style.display = 'flex'
        userModUpdate.style.display = 'none';
        userModal_h3.innerHTML = "view Your Data";

    } catch (error) {
        console.error('Error fetching profile:', error);
        const profBtn = document.getElementById("user-btn");
        profBtn.innerHTML = "Not authorized";
        setTimeout(() => {
            profBtn.innerHTML = "Profile";
        }, 3000);
    }
    userDelCancel.addEventListener("click", ()=> userModDelete.style.display="none")
    userDelBtn.addEventListener('click', function () {
        userModDelete.style.display = "flex";
        useless.style.display = "none";
        userDelPWD.value = "";
        hiddenElement = document.getElementById("hiddenElement")
        hiddenElement.addEventListener('mouseover', () => {
            useless.style.display = 'block';
        });

        hiddenElement.addEventListener('mouseout', () => {
            useless.style.display = 'none';
        });


});

userDelConf.addEventListener("click", async function () {

    try{
        userData = {
        username : user_obj.username,
        password : userDelPWD.value
        }
        res = await axios.delete("/delete/user", {
            headers: { Authorization: `Bearer ${token}` },
            data: { user:userData}
        })
        if (res.data.status == "Error"){
            userDel_err.innerHTML = res.data.message
            setTimeout(() => {
                userDel_err.innerHTML = ""
            }, 5000);
            return
        }
        window.location.reload()
    }catch(error){
        console.error(error)
        userDel_err.innerHTML = res.data
    }

});
useless.addEventListener("click", function  useless() {

    // Create a new paragraph element
    const x = document.createElement("p");
    x.innerHTML = `${userDel_h3.children.length + 1}🐥`; // Add numbering for clarity

    // Append the element to the userDel_h3 container
    userDel_h3.append(x);

    // Remove the element after 3 seconds
    setTimeout(() => {
        y =  userDel_h3.children.length + 1
        if (y > 14 )
            window.document.body .innerHTML = `<h1>you   get ${y}🐥 before flying away   congratulation  winning  useless game  </h1>`
        x.remove(); // Safely remove the DOM element
    }, 3000);
});

}
