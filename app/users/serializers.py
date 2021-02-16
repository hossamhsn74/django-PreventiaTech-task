from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser, Profile


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name',
                  'email', 'password', 'is_superuser']

    def create(self, validated_data):
        if self.validated_data['is_superuser'] == True:
            return CustomUser.objects.create_superuser(**validated_data)
        else:
            return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'first name': user.first_name,
            'last name': user.last_name,
            'email': user.email,
        }


class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            return obj.image

        return 'https://static.productionready.io/images/smiley-cyrus.jpg'
