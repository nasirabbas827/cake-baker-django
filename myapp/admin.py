import csv
from django.http import HttpResponse
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Profile, Cake, CakeCategory, Order, OrderItem, Cart, CustomizationRequest
from django import forms
from django.utils import timezone


class DateRangeFilter(admin.SimpleListFilter):
    title = _('Order Date')
    parameter_name = 'order_date'

    def lookups(self, request, model_admin):
        return (
            ('today', _('Today')),
            ('past_week', _('Past week')),
            ('past_month', _('Past month')),
            ('past_year', _('Past year')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'today':
            return queryset.filter(order_date__date=timezone.now().date())
        elif value == 'past_week':
            return queryset.filter(order_date__gte=timezone.now() - timezone.timedelta(days=7))
        elif value == 'past_month':
            return queryset.filter(order_date__gte=timezone.now() - timezone.timedelta(days=30))
        elif value == 'past_year':
            return queryset.filter(order_date__gte=timezone.now() - timezone.timedelta(days=365))
        return queryset


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'payment_status', 'order_status', 'order_date')
    search_fields = ('user__username', 'payment_status', 'order_status')
    list_filter = (DateRangeFilter, 'order_status', 'payment_status')  # Using the custom DateRangeFilter
    actions = ['export_to_csv']

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders.csv"'

        writer = csv.writer(response)
        writer.writerow(['Order ID', 'User', 'Total Amount', 'Payment Status', 'Order Status', 'Order Date'])

        for order in queryset:
            writer.writerow([order.id, order.user.username, order.total_amount, order.payment_status, order.order_status, order.order_date])

        return response

    export_to_csv.short_description = "Export Selected Orders to CSV"


# Register models with their custom admin classes
admin.site.register(Profile)
admin.site.register(CakeCategory)
admin.site.register(Cake)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)  # Use custom OrderAdmin
admin.site.register(OrderItem)
admin.site.register(CustomizationRequest)
