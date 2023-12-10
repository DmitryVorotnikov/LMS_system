from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from payments.models import Payment
from payments.services import check_payment_status


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PaymentListRetrieveSerializer(serializers.ModelSerializer):
    payment_status = SerializerMethodField()

    class Meta:
        model = Payment
        fields = (
            'id',
            'creator',
            'paid_course',
            'date_of_payment',
            'payment_amount',
            'payment_type',
            'payment_session_id',
            'link_for_payment',
            'payment_status',
        )

    def get_payment_status(self, instance):
        # Проверяем статус платежа с помощью id сессии.
        if instance.link_for_payment:
            payment_status = check_payment_status(payment_session_id=instance.payment_session_id)
            print(payment_status)
            if payment_status != 'open':
                return f'Оплачено'
            else:
                return f'Не оплачено'
        else:
            return f'Не оплачено'
