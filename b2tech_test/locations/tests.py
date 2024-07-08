from django.urls            import reverse
from django.contrib.auth    import get_user_model
from rest_framework         import status
from rest_framework.test    import APITestCase
from .models                import Location
from groups.models          import SharedGroup

User = get_user_model()

class LocationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone_number='+12345678901', password='testpassword123')
        self.group = SharedGroup.objects.create(name='Test Group')
        self.group.members.add(self.user)
        self.client.login(phone_number='+12345678901', password='testpassword123')

    def test_create_location(self):
        url = reverse('location-create')
        data = {'latitude': 37.7749, 'longitude': -122.4194}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)
        self.assertEqual(Location.objects.get().latitude, data['latitude'])

    def test_list_locations(self):
        Location.objects.create(user=self.user, latitude=37.7749, longitude=-122.4194)
        url = reverse('location-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_group_locations(self):
        Location.objects.create(user=self.user, shared_group=self.group, latitude=37.7749, longitude=-122.4194)
        url = reverse('group-location-list', kwargs={'group_id': self.group.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
