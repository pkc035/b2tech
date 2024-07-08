from django.urls    import path
from .views         import (BoundaryListCreateView, BoundaryRetrieveUpdateDestroyView,
                            NotificationListView, NotificationDetailView)

urlpatterns = [
    path('boundaries/', BoundaryListCreateView.as_view(), name='boundary-list'),
    path('boundaries/<int:pk>/', BoundaryRetrieveUpdateDestroyView.as_view(), name='boundary-detail'),
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
]
