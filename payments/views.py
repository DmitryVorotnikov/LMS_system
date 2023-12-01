from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from payments.models import Payment
from payments.serializers import PaymentSerializer


class PaymentCreateAPIView(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer


class PaymentListAPIView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['date_of_payment']
    filterset_fields = ('paid_course', 'payment_type',)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class PaymentUpdateAPIView(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class PaymentDestroyAPIView(generics.DestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
