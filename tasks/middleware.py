class LogRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # print("Request Headers:", request.headers)  # Logs headers to the terminal
        return self.get_response(request)
