from django.urls    import path
from .views         import (LocationListView, LocationCreateView, GroupLocationListView)

urlpatterns = [
    path('locations/', LocationListView.as_view(), name='location-list'),
    path('locations/create/', LocationCreateView.as_view(), name='location-create'),
    path('groups/<int:group_id>/locations/', GroupLocationListView.as_view(), name='group-location-list'),
]
