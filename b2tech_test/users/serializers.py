from django.contrib.auth                    import get_user_model
from rest_framework                         import serializers
from rest_framework_simplejwt.serializers   import TokenObtainPairSerializer
from .validators                            import validate_phone_number


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'phone_number': {'validators': [validate_phone_number]}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['phone_number'] = user.phone_number
        return token

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if phone_number and password:
            user = User.objects.filter(phone_number=phone_number).first()
            if user and user.check_password(password):
                attrs['username'] = user.username
            else:
                raise serializers.ValidationError('No active account found with the given credentials')

        return super().validate(attrs)
