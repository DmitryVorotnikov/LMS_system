from django.contrib import admin

from education.models import Course, Lesson, Subscription


@admin.register(Course)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('name', 'preview', 'description', 'creator',)
    list_filter = ('creator',)
    search_fields = ('name', 'description',)


@admin.register(Lesson)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('course', 'name', 'description', 'preview', 'link_to_video',)
    list_filter = ('course',)
    search_fields = ('name', 'description',)


@admin.register(Subscription)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'subscription_date',)
    list_filter = ('course', 'user',)
    search_fields = ('course',)
