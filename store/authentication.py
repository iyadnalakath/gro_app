from rest_framework.authentication import TokenAuthentication

class CustomTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        if request.method == 'GET':
            return None
        return super().authenticate(request)
