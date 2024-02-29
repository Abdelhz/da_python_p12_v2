from django.utils import timezone
from CustomUser.models import CustomToken
from pathlib import Path
import json

KEY_FILE = Path.home() / '.my_app_key.json'


def verify_token(token):
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
        
        if not created and not verify_token(token):
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


def get_signature_status(options, CONTRACT_DESCRIPTIONS):
    while True:
        signature_status_str = (options['signature_status'] or input(CONTRACT_DESCRIPTIONS['signature_status'])).lower()
        if signature_status_str in ['true', '1', 'yes']:
            return True
        elif signature_status_str in ['false', '0', 'no']:
            return False
        else:
            print("Invalid input. Please enter either : 'true', '1', 'yes' for True or : 'false', '0', 'no' for False.")

def get_total_amount(options, CONTRACT_DESCRIPTIONS):
    while True:
        try:
            return float(options['total_amount'] or input(CONTRACT_DESCRIPTIONS['total_amount']))
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_remaining_amount(options, CONTRACT_DESCRIPTIONS):
    while True:
        try:
            return float(options['remaining_amount'] or input(CONTRACT_DESCRIPTIONS['remaining_amount']))
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_attendees(options, EVENT_DESCRIPTIONS):
    while True:
        try:
            return int(options['attendees'] or input(EVENT_DESCRIPTIONS['attendees']))
        except ValueError:
            print("Invalid input. Please enter a number.")