from django.db              import models
from django.contrib.auth    import get_user_model

User = get_user_model()

class SharedGroup(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='shared_groups')

    def __str__(self):
        return self.name

class GroupInvitation(models.Model):
    group = models.ForeignKey(SharedGroup, on_delete=models.CASCADE, related_name='invitations')
    invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_invitations')
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    def __str__(self):
        return f"Invitation to {self.invitee.phone_number} from {self.inviter.phone_number} for {self.group.name}"
