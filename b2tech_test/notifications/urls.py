from django.urls    import path
from .views         import BoundaryCreateView, NotificationListView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('boundaries/', BoundaryCreateView.as_view(), name='boundary-create'),
]
