from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class WelcomeView(APIView):
    def get(self, request):
        return Response({
            "message": (
                "Welcome Jasurbek to our API section. "
                "By doing slash after URL (/swagger), "
                "you can see all endpoints."
            )
        }, status=status.HTTP_200_OK)
