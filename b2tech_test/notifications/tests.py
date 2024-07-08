from django.urls                        import reverse
from django.contrib.auth                import get_user_model
from rest_framework                     import status
from rest_framework.test                import APITestCase
from rest_framework_simplejwt.tokens    import RefreshToken
from .models                            import Boundary, Notification

User = get_user_model()

class NotificationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone_number='+12345678901', password='testpassword123')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        self.boundary = Boundary.objects.create(name='Test Boundary', points=[[0,0], [0,1], [1,1], [1,0]])

    def test_create_notification(self):
        url = reverse('notification-list')  # Assuming 'notification-list' is your endpoint name
        data = {
            'user': self.user.id,
            'boundary': self.boundary.id,
            'message': 'Test notification message',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(Notification.objects.get().message, 'Test notification message')

    def test_retrieve_notification(self):
        notification = Notification.objects.create(user=self.user, boundary=self.boundary, message='Another message')
        url = reverse('notification-detail', kwargs={'pk': notification.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Another message')

    # Add more tests as needed for update, delete, etc.
