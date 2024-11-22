```py

    def serve_html(self, filepath):
        """Serve an HTML file."""
        try:
            base_dir = os.path.dirname(__file__)
            abs_path = os.path.join(base_dir, filepath)
            print(f"{DEBUG()} >> \n base_dir[{base_dir}] \n abs_path[{abs_path}] \n filepath[{filepath}]")

            with open(abs_path, "rb") as file:
                self._set_headers(200, "text/html")
                self.wfile.write(file.read())
        except FileNotFoundError:
            self._set_headers(404, "text/html")
            self.wfile.write(b"<h1>404 Not Found</h1>")

```