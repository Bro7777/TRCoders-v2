import time
from django.http import JsonResponse

# Kullanıcı başına 5 saniyede 1 isteğe izin veriyoruz
REQUEST_LIMIT = 5  # saniye
user_requests = {}

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_ip = request.META.get('REMOTE_ADDR', '')

        # Kullanıcının son isteği ile şimdiki zaman farkını hesapla
        last_request_time = user_requests.get(user_ip, 0)
        time_since_last_request = time.time() - last_request_time

        if time_since_last_request < REQUEST_LIMIT:
            return JsonResponse({
                "error": "Çok fazla istek yapıyorsunuz. Lütfen bekleyin."
            }, status=429)

        # Son isteği güncelle
        user_requests[user_ip] = time.time()
        return self.get_response(request)
