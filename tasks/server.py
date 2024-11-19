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

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/api/":
            # Serve the API interface HTML page
            filepath = os.path.join("tasks", "templates", "api_interface.html")
            self.serve_html(filepath)
        elif path == "/api/test/":
            auth_header = self.headers.get("Authorization", "")
            self._set_headers(200)
            self.wfile.write(json.dumps({"message": f"Authorization Header: {auth_header}"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

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
                self._set_headers(400)
                self.wfile.write(json.dumps({"Error": msg}).encode())
                return

            res = auth.authenticate(username=username, password=password)
            if not res[0]:
                self._set_headers(400)
                self.wfile.write(json.dumps({"status": "Error", "message": res[1]}).encode())
                return

            login_res = auth.login_user(res[1])
            if not login_res[0]:
                self._set_headers(400)
                self.wfile.write(json.dumps({"status": "Error", "message": login_res[1]}).encode())
                return

            # Sending the login response with the token
            self._set_headers(200)
            self.wfile.write(json.dumps({"status": "success", "token": login_res[1]}).encode())

        elif path == "/api/logout/":
            # To logout, we no longer need a global variable. Just invalidate the session using token in Authorization header.
            auth_header = self.headers.get("Authorization", "")
            if auth_header:
                # Assuming the `auth.logout_user` method can invalidate a session using the token from the header
                logout_res = auth.logout_user(auth_header)
                if logout_res:
                    self._set_headers(200)
                    self.wfile.write(json.dumps({"status": "success", "message": "Logged out"}).encode())
                else:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({"status": "Error", "message": "Invalid token"}).encode())
            else:
                self._set_headers(400)
                self.wfile.write(json.dumps({"status": "Error", "message": "Missing Authorization header"}).encode())

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
                self._set_headers(400)
                self.wfile.write(json.dumps({"Error": msg}).encode())
                print(f"from multiselection Error msg{msg}")

                return

            if select_in not in Storages_keys:
                self._set_headers(400)
                self.wfile.write(json.dumps({"Error": f"{select_in} is an invalid value"}).encode())
                return

            stor_type = Storages[select_in]
            quay = stor_type.multi_selection(select_by=select_by, val_lst=val_lst)
            if not quay[0]:
                self._set_headers(400)
                self.wfile.write(json.dumps({"Error": quay[1]}).encode())
                print(f"from multiselection {quay[1]}")
                return

            self._set_headers(200)
            self.wfile.write(json.dumps(quay[1]).encode())

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())


def run(server_class=HTTPServer, handler_class=RequestHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running at http://127.0.0.1:{port}/api/")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
