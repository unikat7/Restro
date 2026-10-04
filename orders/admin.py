from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['menu_item']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'order_type', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'order_type', 'created_at')
    list_editable = ('status',)
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    inlines = [OrderItemInline]
