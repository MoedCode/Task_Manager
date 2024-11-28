```py
class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        """Set HTTP headers for the response."""
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.end_headers()
    # Class-level attributes to track the last accepted and rejected requests
    last_accepted_request = None
    last_rejected_request = None

    def serve_html(self, filepath):
        """Serve an HTML file."""
        try:
            with open(filepath, "rb") as file:
                self._set_headers(200, "text/html")
                self.wfile.write(file.read())
                # Log the current request as accepted
                self.__class__.last_accepted_request = f"GET {self.path}"  # Save the request path
                print(f"Last Accepted Request: {self.__class__.last_accepted_request}")  # Print to terminal
        except FileNotFoundError as e:
            # print(f"{DEBUG()} FileNotFoundError[{e}]")
            # raise e
            self._set_headers(404, "text/html")
            self.wfile.write(b"<h1>404 Not Found</h1>")
    # some auth function mot related to question topic
            # Log the current request as rejected due to file not found
            self.__class__.last_rejected_request = f"GET {self.path} (File Not Found)"  # Save the request path
            print(f"Last Rejected Request: {self.__class__.last_rejected_request}")  # Print to terminal

    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path


#        API INTERFACE
        # If the path matches the API endpoint, serve the HTML interface
        if path == "/api/":
            filepath = os.path.join("tasks", "templates", "api_interface.html")
            self.serve_html(filepath)
        else:
            # If the path doesn't match any endpoint, return a 404 response
            self._set_headers(404)
            self.wfile.write(b"<h1>404 Not Found</h1>")

            # Log the current request as rejected due to endpoint not found
            self.__class__.last_rejected_request = f"GET {self.path} (Endpoint Not Found)"  # Save the request path
            print(f"Last Rejected Request: {self.__class__.last_rejected_request}")  # Print to terminal


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

    # rest of endpoint
def run(server_class=HTTPServer, handler_class=RequestHandler, port=5001):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running at http://127.0.0.1:{port}/api/")
    httpd.serve_forever()


if __name__ == "__main__":
    run()

```