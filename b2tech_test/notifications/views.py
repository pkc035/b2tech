from rest_framework import generics, permissions
from .models        import Boundary, Notification
from .serializers   import BoundarySerializer, NotificationSerializer

class BoundaryCreateView(generics.CreateAPIView):
    queryset = Boundary.objects.all()
    serializer_class = BoundarySerializer
    permission_classes = [permissions.IsAdminUser]

class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
