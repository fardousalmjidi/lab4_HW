import time

class CoffeeRequestLoggerMiddleware:
    """
    Middleware مخصص لمراقبة الطلبات الواردة إلى مشروع القهوة،
    حيث يسجل المسار المطلوب ويقيس وقت معالجة الطلب واستجابة السيرفر.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # يتم تنفيذ هذا الكود قبل الوصول إلى الـ View
        start_time = time.time()

        # متابعة تنفيذ الطلب
        response = self.get_response(request)

        # يتم تنفيذ هذا الكود بعد إرجاع الاستجابة
        duration = time.time() - start_time
        
        # طباعة تفاصيل الطلب في وحدة التحكم (Terminal) للاختبار
        if '/coffee/' in request.path:
            print(f"[Coffee Tracker] Path: {request.path} | Method: {request.method} | Time: {duration:.4f}s")

        return response