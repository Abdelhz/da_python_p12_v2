from django.utils import timezone
from CustomUser.models import CustomToken


def verify_token(self, token):
    if timezone.now() <= token.expires_at:
        return True
    return False


def refresh_or_create_token(user):
    try:
        token, created = CustomToken.objects.get_or_create(user=user)
        if not created:
            if not self.verify_token(token):
                token = token.refresh()
        return token
    except Exception as e:
        print(e)
        return None