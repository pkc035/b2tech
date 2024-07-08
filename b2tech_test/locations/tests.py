from django.urls                        import reverse
from django.contrib.auth                import get_user_model
from rest_framework                     import status
from rest_framework.test                import APITestCase
from rest_framework_simplejwt.tokens    import RefreshToken
from .models                            import Location
from groups.models                      import SharedGroup

User = get_user_model()

class LocationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone_number='+12345678901', password='testpassword123')
        self.other_user = User.objects.create_user(phone_number='+19876543210', password='otherpassword123')
        self.group = SharedGroup.objects.create(name='Test Group')
        self.group.members.add(self.user)
        self.refresh_token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh_token.access_token}')

        self.location1 = Location.objects.create(user=self.user, latitude='1.0', longitude='1.0')
        self.location2 = Location.objects.create(user=self.other_user, latitude='2.0', longitude='2.0', shared_group=self.group)

    def test_create_location(self):
        url = reverse('location-create')
        data = {'latitude': '3.0', 'longitude': '3.0'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 3)
        self.assertEqual(Location.objects.last().user, self.user)

    def test_list_user_locations(self):
        url = reverse('location-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 

    def test_list_group_locations(self):
        url = reverse('group-location-list', kwargs={'group_id': self.group.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  
    
    def tearDown(self):
        SharedGroup.objects.all().delete()
        Location.objects.all().delete()
        User.objects.all().delete()