from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from payments.models import Payment
from payments.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    # Поле payments с историей платежей по пользователю
    def get_payments(self, instance):
        return PaymentSerializer(Payment.objects.filter(user=instance), many=True).data
