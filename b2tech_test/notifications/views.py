from rest_framework     import generics, permissions
from .models            import Boundary, Notification
from .serializers       import BoundarySerializer, NotificationSerializer

class BoundaryListCreateView(generics.ListCreateAPIView):
    queryset = Boundary.objects.all()
    serializer_class = BoundarySerializer
    permission_classes = [permissions.IsAdminUser]

class BoundaryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Boundary.objects.all()
    serializer_class = BoundarySerializer
    permission_classes = [permissions.IsAdminUser]

class NotificationListView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

class NotificationDetailView(generics.RetrieveDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
