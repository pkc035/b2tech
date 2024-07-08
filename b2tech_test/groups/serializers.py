from rest_framework import serializers
from .models        import SharedGroup, GroupInvitation

class SharedGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedGroup
        fields = ['id', 'name', 'members']
        read_only_fields = ['members']

class GroupInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupInvitation
        fields = ['id', 'group', 'invitee', 'inviter', 'created_at', 'accepted', 'rejected']
        read_only_fields = ['group', 'inviter', 'created_at', 'accepted', 'rejected']