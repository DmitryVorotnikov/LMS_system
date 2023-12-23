from rest_framework import serializers

from payments.serializers import PaymentSerializer
from users.models import User
from users.services import password_hashing_on_creation, password_hashing_on_update


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(source='payment_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = ('password', 'first_name', 'last_name', 'email', 'phone_number', 'city', 'avatar', 'payments',)

    def create(self, validated_data):
        password_hashing_on_creation(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password_hashing_on_update(validated_data)
        return super().update(instance, validated_data)


class UserForAdminSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(source='payment_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password_hashing_on_creation(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password_hashing_on_update(validated_data)
        return super().update(instance, validated_data)


class UserForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'email', 'phone_number', 'city', 'avatar',)
