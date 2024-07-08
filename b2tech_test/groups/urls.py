from django.urls    import path
from .views         import (GroupListView, GroupCreateView, GroupDetailView, GroupInviteView,
                            GroupAcceptInviteView, GroupRejectInviteView, GroupLeaveView)

urlpatterns = [
    path('', GroupListView.as_view(), name='group-list'),
    path('create/', GroupCreateView.as_view(), name='group-create'),
    path('<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    path('<int:pk>/invite/', GroupInviteView.as_view(), name='group-invite'),
    path('invitations/<int:pk>/accept/', GroupAcceptInviteView.as_view(), name='group-accept-invite'),
    path('invitations/<int:pk>/reject/', GroupRejectInviteView.as_view(), name='group-reject-invite'),
    path('<int:pk>/leave/', GroupLeaveView.as_view(), name='group-leave'),
]
