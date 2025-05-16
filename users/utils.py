from django.contrib.auth import get_user_model

User = get_user_model()

def generate_unique_username(base_username):
    
    username = base_username
    count = 1

    while User.objects.filter(username=username).exists():
        username = f"{base_username}{count}"
        count += 1
    
    return username