from rest_framework_simplejwt.tokens import RefreshToken

class CustomRefreshToken(RefreshToken):
    def for_user(self, user):
        """
        Override to use `user_id` instead of `id`.
        """
        self.payload['user_id'] = user.user_id  # Use `user_id` instead of `id`
        return self
