#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
import os
from jinja2 import Environment, FileSystemLoader
# Import your storage, authentication, and models modules
from tasks.__init__ import *
from authentication import Authentication

auth = Authentication()

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        """Set HTTP headers for the response."""
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.end_headers()

    def serve_html(self, filepath):
        """Serve an HTML file."""
        print(f"{DEBUG()} >>   filepath[{filepath}]")

        try:
            with open(filepath, "rb") as file:
                print(f"{DEBUG()} >> \n  filepath[{filepath}] \n file[{file}]")

                self._set_headers(200, "text/html")
                self.wfile.write(file.read())
        except FileNotFoundError as e:
            # print(f"{DEBUG()} FileNotFoundError[{e}]")
            # raise e
            self._set_headers(404, "text/html")
            self.wfile.write(b"<h1>404 Not Found</h1>")


    # Set up Jinja2 environment


    def serve_html(self, filepath, context=None):
        template_dir = os.path.join("tasks", "templates")  # Update to your templates folder
        env = Environment(loader=FileSystemLoader(template_dir))
        """Serve an HTML file with optional context using Jinja2."""
        try:
            # Extract template name
            template_name = os.path.relpath(filepath, template_dir)
            template = env.get_template(template_name)  # Load the template

            # Render the template with context
            html_content = template.render(context or {})

            self._set_headers(200, "text/html")
            self.wfile.write(html_content.encode())
        except Exception as e:
            self._set_headers(500, "text/html")
            error_message = f"<h1>500 Internal Server Error</h1><p>{e}</p>"
            self.wfile.write(error_message.encode())


    def parse_request_data(self):
        """Parse JSON request body."""
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        try:
            post_data = self.rfile.read(content_length)
            return json.loads(post_data)
        except json.JSONDecodeError:
            return None

    def send_response_data(self, data, status=200):
        """Helper to send a JSON response."""
        self._set_headers(status)
        self.wfile.write(json.dumps(data).encode())


    def get_token_dict(self):
        return auth.is_auth(self.headers)


    def get_user_tasks(self, user_id=""):
        if not user_id:
            query_id = self.get_token_dict()
            if not query_id[0]:
                return query_id
            user_id = query_id[1]["user_id"]
        all_tasks = tasks_stor.csv_read()
        user_tasks = []
        for task in all_tasks:
            if task["user_id"] == user_id:
                user_tasks.append(task)
        return True, user_tasks


    def get_tasks_html(self, user_id=""):
        tasks_query = self.get_user_tasks(user_id)
        if not tasks_query[0]:
            return tasks_query
        user_tasks = tasks_query[1]
        msg = "<div class='task_card'>"
        for task in user_tasks:
            msg  += f"<h3 class='task_title'>{task['task'] }</h3>"
            msg  += f"<ul class='task_list'>"
            for key, value in task.items():
                msg +=f"<li class='task_entries'><strong>{ key }:</strong> { value }</li>"
            msg += "</ul>"
        msg +="</div>"
        return True, msg


    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path


#        API INTERFACE
        if path == "/api/":
            filepath = os.path.join("tasks", "templates", "api_interface.html")
            print(f"{DEBUG()} \n {filepath}")
            self.serve_html(filepath)


# #       HOME PAGE
#         elif path == "/" or path == "":
#             res, user_id = self.get_token_dict()
#             if not  res:
#                 print(f"{DEBUG()} -- {user_id}")
#                 filepath = os.path.join("tasks", "templates", "login.html")
#                 print(f"{DEBUG()} \n {filepath}")
#                 self.serve_html(filepath)
#                 return
#             else:


#                 filepath = os.path.join("tasks", "templates", "Hi.html")
#                 rendered_tasks = self.get_tasks_html()
#                 if not rendered_tasks[0]:
#                     msg = f"<h1>sorry Something Went Wrong {rendered_tasks[1]} </h1>"
#                     self.serve_html(filepath, context={"rendered_tasks":msg})

#                 self.serve_html(filepath, context={"rendered_tasks":rendered_tasks})
#                 return

#       HOME PAGE
        elif path == "/" or path == "":
            res, token_dict = self.get_token_dict()
            if not  res:
                filepath = os.path.join("tasks", "templates", "base.html")
                cont_dict = {"status":False, "message":"not authorize"}
                self.serve_html(filepath, context={"data":cont_dict})
                return
            else:
                filepath = os.path.join("tasks", "templates", "base.html")
                cont_dict = {"status":True, "Token":token_dict["token"]}
                self.serve_html(filepath, context={"data":cont_dict})

                return



        elif path == "/api/test/":
            auth_header = self.headers.get("Authorization", "")
            self.send_response_data({"message": f"Authorization Header: {auth_header}"})


        elif path == "/api/hi/":
            res, user_id = self.get_token_dict()
            if not  res:
                print(f"{DEBUG()} -- {user_id}")
                self.send_response_data({"error": f"Not Found {user_id}"}, status=S401)
                return
            all_tasks = tasks_stor.csv_read()
            user_tasks = []
            for task in all_tasks:
                if task["user_id"] == user_id:
                    user_tasks.append(task)

            self.send_response_data(self.get_user_tasks()[1])
        else:
            self.send_response_data({"error": "Not Found"}, status=404)


    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        data = self.parse_request_data()

        if data is None:
            self.send_response_data({"Error": "Invalid JSON in request body"}, status=400)
            return

        if path == "/api/login/":
            username = data.get("username")
            password = data.get("password")
            if not username or not password:
                self.send_response_data({"Error": "Missing username or password"}, status=400)
                return

            res = auth.authenticate(username=username, password=password)
            if not res[0]:
                self.send_response_data({"Error": res[1]}, status=200)
                return

            login_res = auth.login_user(res[1])
            if not login_res[0]:
                self.send_response_data({"Error": login_res[1]}, status=200)
                return

            self.send_response_data({"status": "success", "token": login_res[1]})

        elif path == "/api/logout/":
            print(f"{path}: self.headers{self.headers}")
            if data and data.get("id"):
                user_id = data.get("id")
                x =  auth.logout(user_id=user_id)
                print(f"{path} : user_id {user_id} x{x}")
                self.send_response_data({"status": "success", "message": f"{self.headers} Logged out"})
                return
            auth_header = self.headers.get("Authorization", "")
            print(f" Error -- {path} : auth_header before : {auth_header} {type(auth_header)}")
            if not auth_header:


                self.send_response_data({"Error": "Missing Authorization header"}, status=400)
                return
            parsed_token = auth_header.split(" ")[1]
            logout_res = auth.delete_token(parsed_token)
            print(f" Error -- {path} : parsed_token : {parsed_token}")
            if logout_res[0]:
                self.send_response_data({"status": "success", "message": "Logged out"})
            else:
                self.send_response_data({"Error": f"Invalid token {logout_res[1]}"}, status=400)

        elif path == "/api/selection/":
            select_by = data.get("select_by")
            select_in = data.get("select_in")
            val_lst = data.get("val_lst")

            if not select_by or not val_lst or not select_in:
                self.send_response_data(
                    {"Error": "Missing selection key, selection area, or selection values"},
                    status=400,
                )
                return

            if select_in not in Storages_keys:
                self.send_response_data({"Error": f"{select_in} is an invalid value"}, status=400)
                return

            stor_type = Storages[select_in]
            quay = stor_type.multi_selection(select_by=select_by, val_lst=val_lst)
            if not quay[0]:
                self.send_response_data({"Error": quay[1]}, status=400)
                return

            self.send_response_data(quay[1])

        elif path == "/api/add/":
            res, token_dict = self.get_token_dict()
            if not  res:
                self.send_response_data({"error": f"Not Found {token_dict}"}, status=401)
            try:
                task_data = {
                    "task": data.get("task"),
                    "user_id": token_dict["user_id"],
                    "priority": int(data.get("priority", 0)),
                    "kickoff": data.get("kickoff"),
                }
                task_obj = Tasks(**task_data)
                task_dict = task_obj.to_save()
                res = tasks_stor.add(task_dict)
                if not res[0]:
                    self.send_response_data({"Error": res[1]}, status=200)
                    return
                tasks_stor.save()
                self.send_response_data(res[1])
            except Exception as e:
                self.send_response_data({"Error": str(e)}, status=200)

            #UPDATE
        elif path == "/api/update/":
            res, token_dict = self.get_token_dict()
            if not  res:
                self.send_response_data({"error": f"Not Found {token_dict}"}, status=401)
            category = data.get("category", "")
            lock_for= data.get("lock_for", "")
            update_data= data.get("update_data","")
            if not category or not update_data or not lock_for:
                msg = f"No:{' -category' if not category else ''}" \
                    f"{', key value to lock for' if not lock_for else ''}" \
                    f"{', data to update' if not update_data else ''}   provided"

                self.send_response_data({"status":"Error", "message":msg}, status=200)
                return

            cat = category + 's' if category[-1] != 's' else category
            if cat.lower() == "users":
                result = auth.update_user(user=lock_for, data=update_data)
                if result[0]:
                    self.send_response_data({"status":"success", "message":result[1]}, status=200)
                    return
                self.send_response_data({"status":"Error", "message":result[1]}, status=200)
                return

            storage = None
            for name ,stor_type in Storages.items():
                if cat.lower() == name.lower():
                    storage = stor_type
            if not storage:
                self.send_response_data({"status":"Error", "message":f"category {category} not found"}, status=200)
                return
            print(f"{DEBUG()} {lock_for}")
            key=list(lock_for.keys())[0]
            value = lock_for[key]
            print(f"{DEBUG()}  {key}:{value}")
            result = storage.update(key=key,value=value,  data=update_data)
            if not result[0]:
                self.send_response_data({"status":"Error", "message":f"{result[1]}"}, status=200)
                return
            self.send_response_data({"success":"Error", "data":result[1]}, status=200)
            return


        elif path == "/api/delete/":
            print(f"{DEBUG()}")
            res, token_dict = self.get_token_dict()
            if not  res:
                self.send_response_data({"error": f"Not Found {token_dict}"}, status=401)
            task_id = data.get("task_id", "")
            if not task_id:
                self.send_response_data({"Error":"No task id provided"}, status=200)
                return
            task_q = tasks_stor.get_by("id", task_id)
            if not task_q[0]:
                self.send_response_data({"status":"Error", "message":f"{task_q[1]}"}, status=200)
                return
            if task_q[1]["user_id"] != token_dict["user_id"]:
                self.send_response_data({"status":"Error", "message":f"task id{task_q[1]['user_id']} \n  {user_id}"}, status=200)
                return
            del_res = tasks_stor.delete("id", task_id)
            self.send_response_data({"status":"success", "message":f"task deleted successfully"}, status=200)

        elif path == "/api/register/":
            not_match = [key for key in data.keys() if key not in Users.KEYS]
            if not_match:
                self.send_response_data(
                    {"Error": f"Invalid keys provided: {not_match}"}, status=200
                )
                return

            username_query = users_stor.is_exist("username", data["username"])
            email_query = users_stor.is_exist("email", data["email"])
            if username_query[0] == "Exist":
                self.send_response_data(
                    {"Error": f"User with username {data['username']} already exists"},
                    status=200,
                )
                return
            if email_query[0] == "Exist":
                self.send_response_data(
                    {"Error": f"User with email {data['email']} already exists"},
                    status=200,
                )
                return

            result = Users.create(**data)
            if not result[0]:
                self.send_response_data({"Error": result[1]}, status=422)
                return

            user_dict = result[1].to_save()
            users_stor.add(user_dict)
            users_stor.save()
            log_res = auth.login_user(user_dict)
            if not log_res[0]:
                self.send_response_data({"Error": log_res[1]}, status=400)
                return

            token = log_res[1]
            self.send_response_data(
                {"success": "User registered successfully", "token": token, "user": user_dict},
                status=201,
            )

        else:
            self.send_response_data({"Error": "Endpoint not found"}, status=404)


def run(server_class=HTTPServer, handler_class=RequestHandler, port=5000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running at http://127.0.0.1:{port}/api/")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
