import time
import logging

logger = logging.getLogger("shop")


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        logger.info(f"➡️ Request: {request.method} {request.path}")

        response = self.get_response(request)

        duration = round(time.time() - start_time, 4)

        logger.info(
            f"⬅️ Response: {request.method} {request.path} "
            f"Status: {response.status_code} Time: {duration}s"
        )

        return response