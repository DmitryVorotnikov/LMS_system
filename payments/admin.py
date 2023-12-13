from django.contrib import admin

from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('paid_course', 'date_of_payment', 'payment_amount', 'payment_session_id', 'link_for_payment', 'payment_status', 'creator',)
    list_filter = ('payment_status',)
    search_fields = ('payment_amount',)
