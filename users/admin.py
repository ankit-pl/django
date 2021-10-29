from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.http.response import HttpResponseRedirect
from .models import User, WalletInformation, Card, Transaction
from django.urls import path


admin.site.site_header = "API Admin Panel"


class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency', 'balance', 'last_transaction_date')
    list_filter = ('user', 'currency', 'last_transaction_date')
    search_fields = ('user',)


class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'last_transaction_date')
    list_filter = ('user', 'last_transaction_date')
    search_fields = ('user',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'type', 'status')
    list_filter = ('type', 'status')


class UserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'is_staff', 'is_active')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    change_list_template = "admin/user_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [path('change-active-status', self.change_active_status)]
        return urls + custom_urls

    def change_active_status(self, request):
        emails = request.POST['emails'].split(",")
        status = True if request.POST['status'] == "active" else False
        for email in emails:
            user = self.model.objects.filter(email=email.strip()).first()
            if user:
                user.is_active = status
                user.save()
        self.message_user(request, "Status updated")
        return HttpResponseRedirect("../user")


admin.site.register(User, UserAdmin)
admin.site.register(WalletInformation, WalletAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.unregister(Group)
