from django.urls import path

from payments.apps import PaymentsConfig
from payments.views import PaymentCreateAPIView, PaymentListAPIView, PaymentRetrieveAPIView, PaymentUpdateAPIView, \
    PaymentDestroyAPIView

app_name = PaymentsConfig.name

urlpatterns = [
    path('create/', PaymentCreateAPIView.as_view(), name='payments_create'),
    path('', PaymentListAPIView.as_view(), name='payments_list'),
    path('<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payments_get'),
    # path('update/<int:pk>/', PaymentUpdateAPIView.as_view(), name='payments_update'),
    # path('delete/<int:pk>/', PaymentDestroyAPIView.as_view(), name='payments_delete'),
]
