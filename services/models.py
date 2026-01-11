from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone



"""
Models:

1. Services
2. Webcontent


Contents:
1. Puje list:
    - Title
    - Price
    - Number of pandit
    - number of days
    - description
    - puja purpose
2. Host details:
    - address, lat, lon
    - contact number
    - whatsapp_number
"""


class Pandit(models.Model):
    """Model for Pandits/Priests"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    experience_years = models.IntegerField(default=0)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='pandits/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class PujaService(models.Model):
    """Model for Puja Services"""
    CATEGORY_CHOICES = [
        ('ancestral', 'Ancestral Rituals'),
        ('remedial', 'Remedial Pujas'),
        ('life_event', 'Life Event Pujas'),
        ('spiritual', 'Spiritual Pujas'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='ancestral')
    description = models.TextField()
    detailed_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    number_of_pandits = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    duration_days = models.IntegerField(default=1, help_text="Duration in days")
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    benefits = models.TextField(blank=True, help_text="Key benefits of this puja")
    includes = models.TextField(blank=True, help_text="What's included in this service")
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category', 'name']


class Booking(models.Model):
    """Model for Customer Bookings"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    service = models.ForeignKey(PujaService, on_delete=models.CASCADE, related_name='bookings')
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    customer_address = models.TextField()

    # Booking details
    preferred_date = models.DateField()
    special_requests = models.TextField(blank=True)
    assigned_pandits = models.ManyToManyField(Pandit, related_name='bookings', blank=True)

    # Status and payment
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer_name} - {self.service.name}"

    class Meta:
        ordering = ['-created_at']


class Payment(models.Model):
    """Model for Payment Transactions with Razorpay Integration"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('initiated', 'Initiated'),
        ('authorized', 'Authorized'),
        ('captured', 'Captured'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Razorpay Integration
    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=500, blank=True, null=True)

    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for {self.booking.customer_name} - {self.razorpay_order_id or 'Pending'}"

    class Meta:
        ordering = ['-created_at']


class SiteConfig(models.Model):
    """Model for Site Configuration and Settings"""
    site_name = models.CharField(max_length=200, default='Haridwar Puja')
    tagline = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)

    # Contact Information
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    whatsapp_number = models.CharField(max_length=20, blank=True)

    # Location
    address = models.TextField()
    city = models.CharField(max_length=100, default='Haridwar')
    state = models.CharField(max_length=100, default='Uttarakhand')
    country = models.CharField(max_length=100, default='India')
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    # Payment Settings
    razorpay_key_id = models.CharField(max_length=500, blank=True)
    razorpay_key_secret = models.CharField(max_length=500, blank=True)

    # Social Media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = 'Site Configuration'
        verbose_name_plural = 'Site Configuration'
