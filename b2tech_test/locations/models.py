from django.db              import models
from django.contrib.auth    import get_user_model
from groups.models          import SharedGroup

User = get_user_model()

class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_group = models.ForeignKey(SharedGroup, on_delete=models.CASCADE, null=True, blank=True, related_name='locations')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone_number} @ {self.timestamp}"
