from rest_framework             import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .models                    import Location
from .serializers               import LocationSerializer
from groups.models              import SharedGroup
from notifications.models       import Boundary, Notification

class LocationCreateView(generics.CreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        location = serializer.save(user=self.request.user)
        self.check_boundaries(location)

    def check_boundaries(self, location):
        boundaries = Boundary.objects.all()
        for boundary in boundaries:
            if self.is_within_boundary(location, boundary):
                Notification.objects.create(
                    user=location.user,
                    boundary=boundary,
                    message=f"You have entered the restricted area: {boundary.name}"
                )

    def is_within_boundary(self, location, boundary):
        from shapely.geometry import Point, Polygon
        point = Point(float(location.latitude), float(location.longitude))
        polygon = Polygon(boundary.points)
        return polygon.contains(point)

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
