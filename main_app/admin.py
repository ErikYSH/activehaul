from atexit import register
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, OrderItem, Orders, Product

# Register your models here.

class AccountAdmin (UserAdmin):
    list_display = ('email', 'username', 'bio', 'created_at','last_login', 'is_admin','is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'created_at', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets =()


admin.site.register(Account, AccountAdmin)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Orders)

