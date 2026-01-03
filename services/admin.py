from django.contrib import admin
from .models import Pandit, PujaService, Booking, Payment, SiteConfig


@admin.register(Pandit)
class PanditAdmin(admin.ModelAdmin):
    list_display = ('name', 'experience_years', 'phone', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'email', 'phone')
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Professional Details', {
            'fields': ('experience_years', 'bio', 'image')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(PujaService)
class PujaServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'number_of_pandits', 'is_active', 'featured')
    list_filter = ('category', 'is_active', 'featured', 'created_at')
    search_fields = ('name', 'description')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description', 'detailed_description')
        }),
        ('Service Details', {
            'fields': ('price', 'number_of_pandits', 'duration_days')
        }),
        ('Content', {
            'fields': ('benefits', 'includes', 'image')
        }),
        ('Status', {
            'fields': ('is_active', 'featured')
        }),
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'service', 'preferred_date', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at', 'service')
    search_fields = ('customer_name', 'customer_email', 'customer_phone')
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone', 'customer_address')
        }),
        ('Booking Details', {
            'fields': ('service', 'preferred_date', 'assigned_pandits', 'special_requests')
        }),
        ('Payment & Status', {
            'fields': ('status', 'total_amount')
        }),
    )
    filter_horizontal = ('assigned_pandits',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'status', 'razorpay_order_id', 'created_at')
    list_filter = ('status', 'created_at', 'payment_method')
    search_fields = ('booking__customer_name', 'razorpay_order_id', 'razorpay_payment_id')
    readonly_fields = ('razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'created_at', 'updated_at')
    fieldsets = (
        ('Booking Information', {
            'fields': ('booking', 'amount')
        }),
        ('Razorpay Details', {
            'fields': ('razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature')
        }),
        ('Payment Status', {
            'fields': ('status', 'payment_method')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'tagline', 'description')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email', 'whatsapp_number')
        }),
        ('Location', {
            'fields': ('address', 'city', 'state', 'country', 'latitude', 'longitude')
        }),
        ('Razorpay Settings', {
            'fields': ('razorpay_key_id', 'razorpay_key_secret'),
            'classes': ('collapse',)
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'youtube_url')
        }),
    )

    def has_add_permission(self, request):
        return not SiteConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
