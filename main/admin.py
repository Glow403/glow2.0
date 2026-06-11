from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db import transaction
from .models import UserProfile, ServiceOrder


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = '欢乐豆'


class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ('username', 'email', 'joy_dots', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')
    actions = ['recharge_joy_dots', 'deduct_joy_dots']

    def joy_dots(self, obj):
        return obj.profile.joy_dots
    joy_dots.short_description = '欢乐豆'

    @admin.action(description='为选中的用户充值欢乐豆')
    def recharge_joy_dots(self, request, queryset):
        with transaction.atomic():
            for user in queryset:
                try:
                    amount = int(request.POST.get('recharge_amount', 0))
                    if amount > 0:
                        user.profile.joy_dots += amount
                        user.profile.save(update_fields=['joy_dots'])
                except (ValueError, TypeError):
                    pass
            self.message_user(request, f'成功为 {queryset.count()} 个用户充值欢乐豆')

    recharge_joy_dots.short_description = '批量充值欢乐豆'

    @admin.action(description='为选中的用户扣除欢乐豆')
    def deduct_joy_dots(self, request, queryset):
        with transaction.atomic():
            for user in queryset:
                try:
                    amount = int(request.POST.get('deduct_amount', 0))
                    if amount > 0 and user.profile.joy_dots >= amount:
                        user.profile.joy_dots -= amount
                        user.profile.save(update_fields=['joy_dots'])
                    elif amount > user.profile.joy_dots:
                        self.message_user(request, f'用户 {user.username} 欢乐豆不足，无法扣除 {amount}', level=admin.messages.ERROR)
                except (ValueError, TypeError):
                    pass
            self.message_user(request, f'成功为部分用户扣除欢乐豆')

    deduct_joy_dots.short_description = '批量扣除欢乐豆'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_type', 'username', 'course_name', 'cost', 'created_at')
    list_filter = ('service_type', 'created_at')
    search_fields = ('username', 'user__username')
    readonly_fields = ('user', 'service_type', 'username', 'password', 'course_name',
                       'times', 'distance', 'remark', 'cost', 'created_at')
    list_per_page = 20


admin.site.register(ServiceOrder, ServiceOrderAdmin)
