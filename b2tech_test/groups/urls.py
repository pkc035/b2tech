from django.urls import path
from .views import (GroupListView, GroupCreateView, GroupDetailView, GroupInviteView,
GroupAcceptInviteView, GroupRejectInviteView, GroupLeaveView)

urlpatterns = [
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('groups/create/', GroupCreateView.as_view(), name='group-create'),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    path('groups/<int:pk>/invite/', GroupInviteView.as_view(), name='group-invite'),
    path('invitations/<int:pk>/accept/', GroupAcceptInviteView.as_view(), name='group-accept-invite'),
    path('invitations/<int:pk>/reject/', GroupRejectInviteView.as_view(), name='group-reject-invite'),
    path('groups/<int:pk>/leave/', GroupLeaveView.as_view(), name='group-leave'),
]
