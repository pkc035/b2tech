from django.urls            import reverse
from django.contrib.auth    import get_user_model
from rest_framework         import status
from rest_framework.test    import APITestCase

User = get_user_model()

class UserTests(APITestCase):

    def test_user_signup(self):
        url = reverse('user-signup')
        data = {
            'phone_number': '+12345678901',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(phone_number=data['phone_number']).exists())

    def test_user_signup_invalid_phone(self):
        url = reverse('user-signup')
        data = {
            'phone_number': 'invalidphone',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        User.objects.all().delete()