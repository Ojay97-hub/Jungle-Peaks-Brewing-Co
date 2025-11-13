from django.contrib import admin
from .models import NewsletterSubscriber


# Register your models here.
@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    # Shows email, date, and interests
    list_display = ('email', 'subscribed_at', 'interests')
    search_fields = ('email',)
    ordering = ('-subscribed_at',)

# --- Social/Auth visibility in admin ---
try:
    from allauth.socialaccount.models import SocialAccount, SocialToken
    from allauth.account.models import EmailAddress
    from django.contrib.auth import get_user_model
    from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

    @admin.register(SocialAccount)
    class SocialAccountAdmin(admin.ModelAdmin):
        list_display = ('user', 'provider', 'uid')
        search_fields = ('user__username', 'user__email', 'uid')
        list_filter = ('provider',)
        ordering = ('-id',)

    @admin.register(EmailAddress)
    class EmailAddressAdmin(admin.ModelAdmin):
        list_display = ('email', 'user', 'verified', 'primary')
        search_fields = ('email', 'user__username')
        list_filter = ('verified', 'primary')
        ordering = ('-id',)

    class SocialAccountInline(admin.TabularInline):
        model = SocialAccount
        extra = 0
        readonly_fields = ('provider', 'uid')
        can_delete = False

    User = get_user_model()

    class UserAdmin(BaseUserAdmin):
        inlines = [SocialAccountInline]

    # Re-register User admin with SocialAccount inline
    try:
        admin.site.unregister(User)
    except admin.sites.NotRegistered:
        pass
    admin.site.register(User, UserAdmin)

except Exception:
    # If allauth is not installed/migrated yet, avoid admin import errors
    pass