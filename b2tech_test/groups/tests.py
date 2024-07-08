from django.urls                        import reverse
from django.contrib.auth                import get_user_model
from rest_framework                     import status
from rest_framework.test                import APITestCase, APIClient
from rest_framework_simplejwt.tokens    import RefreshToken
from .models                            import SharedGroup, GroupInvitation

User = get_user_model()

class GroupTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(phone_number='01012345678', password='password')
        self.refresh_token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh_token.access_token}')
        self.group = SharedGroup.objects.create(name="Test Group")

    def test_create_group(self):
        url = reverse('group-create')
        data = {'name': 'New Test Group'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_groups(self):
        url = reverse('group-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_group(self):
        url = reverse('group-detail', kwargs={'pk': self.group.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_group(self):
        url = reverse('group-detail', kwargs={'pk': self.group.pk})
        data = {'name': 'Updated Group Name'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_group(self):
        url = reverse('group-detail', kwargs={'pk': self.group.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invite_user_to_group(self):
        url = reverse('group-invite', kwargs={'pk': self.group.pk})
        invitee = User.objects.create_user(phone_number='01098765432', password='password')
        data = {'phone_number': '01098765432'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accept_group_invite(self):
        invitee = User.objects.create_user(phone_number='01098765432', password='password')
        invite = GroupInvitation.objects.create(group=self.group, invitee=invitee, inviter=self.user)
        invitee_refresh_token = RefreshToken.for_user(invitee)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {invitee_refresh_token.access_token}')
        url = reverse('group-accept-invite', kwargs={'pk': invite.pk})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reject_group_invite(self):
        invitee = User.objects.create_user(phone_number='01098765432', password='password')
        invite = GroupInvitation.objects.create(group=self.group, invitee=invitee, inviter=self.user)
        invitee_refresh_token = RefreshToken.for_user(invitee)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {invitee_refresh_token.access_token}')
        url = reverse('group-reject-invite', kwargs={'pk': invite.pk})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_leave_group(self):
        self.group.members.add(self.user)
        url = reverse('group-leave', kwargs={'pk': self.group.pk})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        SharedGroup.objects.all().delete()
        GroupInvitation.objects.all().delete()
        User.objects.all().delete()