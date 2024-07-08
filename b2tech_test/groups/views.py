from django.shortcuts           import get_object_or_404
from rest_framework             import generics, permissions, status
from rest_framework.response    import Response
from .models                    import SharedGroup, GroupInvitation
from .serializers               import SharedGroupSerializer, GroupInvitationSerializer

class GroupCreateView(generics.CreateAPIView):
    queryset = SharedGroup.objects.all()
    serializer_class = SharedGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupListView(generics.ListAPIView):
    queryset = SharedGroup.objects.all()
    serializer_class = SharedGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SharedGroup.objects.all()
    serializer_class = SharedGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupInviteView(generics.GenericAPIView):
    serializer_class = GroupInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        group = get_object_or_404(SharedGroup, pk=self.kwargs['pk'])
        invitee_phone_number = request.data.get('phone_number')
        invitee = get_object_or_404(User, phone_number=invitee_phone_number)
        GroupInvitation.objects.create(group=group, invitee=invitee, inviter=request.user)
        return Response({"detail": "Invitation sent."}, status=status.HTTP_200_OK)

class GroupAcceptInviteView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        invite = get_object_or_404(GroupInvitation, pk=self.kwargs['pk'], invitee=request.user)
        invite.accepted = True
        invite.rejected = False
        invite.save()
        invite.group.members.add(request.user)
        return Response({"detail": "Invitation accepted."}, status=status.HTTP_200_OK)

class GroupRejectInviteView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        invite = get_object_or_404(GroupInvitation, pk=self.kwargs['pk'], invitee=request.user)
        invite.rejected = True
        invite.accepted = False
        invite.save()
        return Response({"detail": "Invitation rejected."}, status=status.HTTP_200_OK)

class GroupLeaveView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        group = get_object_or_404(SharedGroup, pk=self.kwargs['pk'])
        group.members.remove(request.user)
        return Response({"detail": "Left the group."}, status=status.HTTP_200_OK)