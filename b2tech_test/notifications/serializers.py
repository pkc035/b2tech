from rest_framework import serializers
from .models        import Boundary, Notification

class BoundarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Boundary
        fields = ['id', 'name', 'points']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'boundary', 'message', 'created_at']
        read_only_fields = ['user', 'created_at']
