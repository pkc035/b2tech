from django.db              import models
from django.contrib.auth    import get_user_model

User = get_user_model()

class Boundary(models.Model):
    name = models.CharField(max_length=100)
    points = models.JSONField()

    def __str__(self):
        return self.name

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    boundary = models.ForeignKey(Boundary, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.phone_number} - {self.message}"
