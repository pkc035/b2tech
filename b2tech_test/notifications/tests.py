from django.urls                        import reverse
from django.contrib.auth                import get_user_model
from rest_framework                     import status
from rest_framework.test                import APITestCase
from rest_framework_simplejwt.tokens    import RefreshToken
from .models                            import Boundary, Notification

User = get_user_model()

class BoundaryTests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(phone_number='+12345678901', password='adminpassword')
        self.refresh_token = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh_token.access_token}')
        self.boundary1 = Boundary.objects.create(name='Boundary 1', points=[[0,0], [0,1], [1,1], [1,0]])
        self.boundary2 = Boundary.objects.create(name='Boundary 2', points=[[1,1], [1,2], [2,2], [2,1]])

    def test_list_boundaries(self):
        url = reverse('boundary-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Check if both boundaries are listed

    def test_create_boundary_as_admin(self):
        url = reverse('boundary-list')
        data = {'name': 'New Boundary', 'points': [[2,2], [2,3], [3,3], [3,2]]}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Boundary.objects.count(), 3)

    def test_retrieve_boundary(self):
        url = reverse('boundary-detail', kwargs={'pk': self.boundary1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.boundary1.name)

    def test_update_boundary(self):
        url = reverse('boundary-detail', kwargs={'pk': self.boundary1.id})
        data = {'name': 'Updated Boundary', 'points': self.boundary1.points}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Boundary.objects.get(id=self.boundary1.id).name, 'Updated Boundary')

    def test_delete_boundary(self):
        url = reverse('boundary-detail', kwargs={'pk': self.boundary1.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Boundary.objects.count(), 1)
    
    def tearDown(self):
        Boundary.objects.all().delete()
        User.objects.all().delete()

class NotificationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone_number='+12345678901', password='userpassword')
        self.refresh_token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh_token.access_token}')
        self.boundary = Boundary.objects.create(name='Test Boundary', points=[[0,0], [0,1], [1,1], [1,0]])

    def test_list_notifications(self):
        Notification.objects.create(user=self.user, boundary=self.boundary, message='Test Notification 1')
        Notification.objects.create(user=self.user, boundary=self.boundary, message='Test Notification 2')
        
        url = reverse('notification-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_notification(self):
        url = reverse('notification-list')
        data = {'user': self.user.id, 'boundary': self.boundary.id, 'message': 'New Test Notification'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(Notification.objects.get().message, 'New Test Notification')
        self.assertEqual(Notification.objects.get().user, self.user)

    def test_retrieve_notification(self):
        notification = Notification.objects.create(user=self.user, boundary=self.boundary, message='Test Notification')
        url = reverse('notification-detail', kwargs={'pk': notification.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Test Notification')

    def test_delete_notification(self):
        notification = Notification.objects.create(user=self.user, boundary=self.boundary, message='Test Notification')
        url = reverse('notification-detail', kwargs={'pk': notification.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Notification.objects.count(), 0)

    def tearDown(self):
        Notification.objects.all().delete()
        Boundary.objects.all().delete()
        User.objects.all().delete()