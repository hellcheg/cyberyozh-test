from django.contrib.auth import get_user_model


class UserRepository:
    def exists(self, user_id: int) -> bool:
        User = get_user_model()
        return User.objects.filter(pk=user_id).exists()
