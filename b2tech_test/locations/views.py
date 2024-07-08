from rest_framework             import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .models                    import Location
from .serializers               import LocationSerializer
from groups.models              import SharedGroup

class LocationCreateView(generics.CreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LocationListView(generics.ListAPIView):
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Location.objects.filter(user=self.request.user)

class GroupLocationListView(generics.ListAPIView):
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        return Location.objects.filter(shared_group_id=group_id)