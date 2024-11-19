#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
import os

# Import your storage, authentication, and models modules
from tasks.__init__ import *
from authentication import Authentication

auth = Authentication()

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.end_headers()

    def serve_html(self, filepath):
        """Serve an HTML file."""
        try:
            with open(filepath, "rb") as file:
                self._set_headers(200, "text/html")
                self.wfile.write(file.read())
        except FileNotFoundError:
            self._set_headers(404, "text/html")
            self.wfile.write(b"<h1>404 Not Found</h1>")

    def parse_request_data(self):
        """Parse JSON request body."""
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        return json.loads(post_data)

    def send_response_data(self, data, status=200):
        """Helper to send a JSON response."""
        self._set_headers(status)
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/api/":
            filepath = os.path.join("tasks", "templates", "api_interface.html")
            self.serve_html(filepath)
        elif path == "/api/test/":
            auth_header = self.headers.get("Authorization", "")
            self.send_response_data({"message": f"Authorization Header: {auth_header}"})
        elif path == "/api/hi/":
            data = tasks_stor.csv_read()
            self.send_response_data(data)
        else:
            self.send_response_data({"error": "Not Found"}, status=404)

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        data = self.parse_request_data()

        if path == "/api/login/":
            username = data.get("username", None)
            password = data.get("password", None)
            if not data or not username or not password:
                msg = "Missing: "
                msg += "request data, " if not data else ""
                msg += "username, " if not username else ""
                msg += "password, " if not password else ""
                self.send_response_data({"Error": msg}, status=400)
                return

            res = auth.authenticate(username=username, password=password)
            if not res[0]:
                self.send_response_data({"status": "Error", "message": res[1]}, status=400)
                return

            login_res = auth.login_user(res[1])
            if not login_res[0]:
                self.send_response_data({"status": "Error", "message": login_res[1]}, status=400)
                return

            self.send_response_data({"status": "success", "token": login_res[1]})

        elif path == "/api/logout/":
            auth_header = self.headers.get("Authorization", "")
            if auth_header:
                logout_res = auth.logout_user(auth_header)
                if logout_res:
                    self.send_response_data({"status": "success", "message": "Logged out"})
                else:
                    self.send_response_data({"status": "Error", "message": "Invalid token"}, status=400)
            else:
                self.send_response_data({"status": "Error", "message": "Missing Authorization header"}, status=400)

        elif path == "/api/selection/":
            select_by = data.get("select_by", None)
            select_in = data.get("select_in", None)
            val_lst = data.get("val_lst", None)

            if not data or not select_by or not val_lst or not select_in:
                msg = "Missing: "
                msg += "Request Data, " if not data else ""
                msg += "selection key, " if not select_by else ""
                msg += "selection area, " if not select_in else ""
                msg += "selection values, " if not val_lst else ""
                msg += "provided."
                self.send_response_data({"Error": msg}, status=400)
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
            task_data = {
                "task": data.get("task"),
                "username": data.get("username"),
                "priority": int(data.get("priority", [0])[0]),
                "kickoff": data.get("kickoff"),
            }
            task_obj = Tasks(**task_data)
            task_dict = task_obj.to_save()
            res = tasks_stor.add(task_dict)
            if not res[0]:
                self.send_response_data({"Error": res[1]}, status=400)
                return
            tasks_stor.save()
            self.send_response_data(res[1])

        elif path == "/api/register/":
            not_match = [key for key in data.keys() if key not in Users.KEYS]
            if not_match:
                msg = f"key provided {not_match} not match {Users.KEYS}"
                self.send_response_data({"Error": msg}, status=400)
                return

            username_query = users_stor.is_exist("username", data["username"])
            email_query = users_stor.is_exist("email", data["email"])
            if username_query[0] == "Exist":
                self.send_response_data({"status": "error", "message": f"user with username {data['username']} exists"}, status=400)
                return
            if email_query[0] == "Exist":
                self.send_response_data({"status": "error", "message": f"user with email {data['email']} exists"}, status=400)
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
                self.send_response_data({"Error": f"{log_res[1]}"}, status=400)
                return

            token = log_res[1]
            self.send_response_data({"success": f"Bearer {token}", "user": user_dict}, status=201)

        else:
            self.send_response_data({"error": "Endpoint not found"}, status=404)


def run(server_class=HTTPServer, handler_class=RequestHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running at http://127.0.0.1:{port}/api/")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
