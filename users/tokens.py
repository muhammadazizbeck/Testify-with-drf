from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import timedelta
def generate_jwt_tokens(user):
    refresh = RefreshToken.for_user(user)

  
    access_token = refresh.access_token
    access_token.set_exp(lifetime=timedelta(minutes=60))  

    return {
        'refresh': str(refresh),
        'access': str(access_token) 
    }