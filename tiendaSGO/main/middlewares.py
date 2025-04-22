from .models import Cliente


class ClienteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                cliente, created = Cliente.objects.get_or_create(user=request.user)
                request.saldo = cliente.saldo
                request.carrito = request.session.setdefault("carrito", {})
            except Exception as e:
                print(e)
                pass
        response = self.get_response(request)

        return response
