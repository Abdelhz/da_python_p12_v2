from django.utils import timezone
from CustomUser.models import CustomToken
from pathlib import Path
import json

KEY_FILE = Path.home() / '.my_app_key.json'


def verify_token(self, token):
    # Check if the token is still valid
    if timezone.now() <= token.expires_at:
        # Check if the locally stored key matches the key in the token
        with open(KEY_FILE, 'r') as f:
            data = json.load(f)
        user_token_key = next((item for item in data["user_token_keys"] if item.get("username") == token.user.username), None)
        local_key = user_token_key.get("token_key") if user_token_key else None
        return local_key == token.key
    return False


def refresh_or_create_token(user):
    try:
        token, created = CustomToken.objects.get_or_create(user=user)
        if not created:
            if not self.verify_token(token):
                token = token.refresh()
        if KEY_FILE.exists():
            with open(KEY_FILE, 'r') as f:
                data = json.load(f)
        else:
            data = {"user_token_keys": []}
        
        user_token_key = next((item for item in data["user_token_keys"] if item.get("username") == user.username), None)
        
        if user_token_key:
            user_token_key["token_key"] = token.key
        
        else:
            data["user_token_keys"].append({
            "username": user.username,
            "token_key": token.key
            })
        
        with open(KEY_FILE, 'w') as f:
            json.dump(data, f)
        
        return token
    
    except Exception as e:
        print(e)
        return None