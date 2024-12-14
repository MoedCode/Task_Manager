#!/usr/bin/env python3

import requests

# Define the URL and the token
url = "http://127.0.0.1:5000/home"
token = "81fce3b2695bcec9db4f0d24d946674088b64781479601a5d1fada28c7ac5daf"

# Define headers with the token
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Send a POST request to the server
response = requests.post(url, headers=headers)

# Print the response from the server
print(response.status_code)
print(response.text)




def serve_html_1(self, filepath):
    """Serve an HTML file."""

    try:
        with open(filepath, "rb") as file:
            self._set_headers(200, "text/html")
            self.wfile.write(file.read())
    except FileNotFoundError as e:
        # print(f"{DEBUG()} FileNotFoundError[{e}]")
        # raise e
        self._set_headers(404, "text/html")
        self.wfile.write(b"<h1>404 Not Found</h1>")

def serve_html_2(self, filepath, context=None):
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
    except BrokenPipeError:
        print("BrokenPipeError: Client closed the connection before the server could finish.")
    except Exception as e:
        self._set_headers(500, "text/html")
        error_message = f"<h1>500 Internal Server Error</h1><p>{e}</p>"
        self.wfile.write(error_message.encode())
