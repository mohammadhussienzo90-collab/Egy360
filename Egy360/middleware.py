from django.http import JsonResponse

class HealthCheckMiddleware:
    """Handle health check before any other middleware"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/health/' or request.path == '/health':
            return JsonResponse({'status': 'ok'})
        return self.get_response(request)
