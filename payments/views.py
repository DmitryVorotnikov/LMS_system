from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from payments.models import Payment
from payments.serializers import PaymentSerializer, PaymentListRetrieveSerializer
from payments.services import get_link_for_payment


class PaymentCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        new_payment = serializer.save()

        # Присваиваем текущего пользователя как создателя платежа.
        new_payment.creator = self.request.user

        paid_course = self.request.data.get('paid_course')
        payment_amount = self.request.data.get('payment_amount')
        # Создаем сессию платежа и сохраняем id сессии и ссылку на платеж.
        link_for_payment, payment_session_id = get_link_for_payment(paid_course=paid_course,
                                                                    payment_amount=payment_amount)

        new_payment.link_for_payment = link_for_payment
        new_payment.payment_session_id = payment_session_id

        new_payment.save()


class PaymentListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentListRetrieveSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['date_of_payment']
    filterset_fields = ('paid_course', 'payment_type',)

    def get_queryset(self):
        # Обычному пользователю в queryset указываем его платежи.
        if not self.request.user.is_staff:
            user_id = self.request.user.id
            queryset = Payment.objects.filter(creator=user_id)
        return queryset


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentListRetrieveSerializer
    queryset = Payment.objects.all()
