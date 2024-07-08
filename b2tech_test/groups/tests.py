from django.urls            import reverse
from django.contrib.auth    import get_user_model
from rest_framework         import status
from rest_framework.test    import APITestCase


from .models import SharedGroup, GroupInvitation

User = get_user_model()

class GroupTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone_number='+12345678901', password='testpassword123')
        self.client.login(phone_number='+12345678901', password='testpassword123')

    def test_create_group(self):
        url = reverse('group-create')
        data = {'name': 'Test Group'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SharedGroup.objects.count(), 1)
        self.assertEqual(SharedGroup.objects.get().name, data['name'])

    def test_list_groups(self):
        SharedGroup.objects.create(name='Test Group')
        url = reverse('group-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_invite_to_group(self):
        group = SharedGroup.objects.create(name='Test Group')
        invitee = User.objects.create_user(phone_number='+12345678902', password='testpassword123')
        url = reverse('group-invite', kwargs={'pk': group.id})
        data = {'phone_number': invitee.phone_number}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(GroupInvitation.objects.count(), 1)
        self.assertEqual(GroupInvitation.objects.get().invitee, invitee)

    def test_accept_invitation(self):
        group = SharedGroup.objects.create(name='Test Group')
        invitee = User.objects.create_user(phone_number='+12345678902', password='testpassword123')
        invitation = GroupInvitation.objects.create(group=group, invitee=invitee, inviter=self.user)
        self.client.login(phone_number='+12345678902', password='testpassword123')
        url = reverse('group-accept-invite', kwargs={'pk': invitation.id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        invitation.refresh_from_db()
        self.assertTrue(invitation.accepted)

    def test_reject_invitation(self):
        group = SharedGroup.objects.create(name='Test Group')
        invitee = User.objects.create_user(phone_number='+12345678902', password='testpassword123')
        invitation = GroupInvitation.objects.create(group=group, invitee=invitee, inviter=self.user)
        self.client.login(phone_number='+12345678902', password='testpassword123')
        url = reverse('group-reject-invite', kwargs={'pk': invitation.id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        invitation.refresh_from_db()
        self.assertTrue(invitation.rejected)

    def test_leave_group(self):
        group = SharedGroup.objects.create(name='Test Group')
        group.members.add(self.user)
        url = reverse('group-leave', kwargs={'pk': group.id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        group.refresh_from_db()
        self.assertNotIn(self.user, group.members.all())
