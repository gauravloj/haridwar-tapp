from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
import json
# import razorpay

from .models import PujaService, Booking, Payment, SiteConfig, Pandit
from .forms import BookingForm


def get_site_config():
    """Helper to get site configuration"""
    return SiteConfig.objects.first()


def home(request):
    """Home page with featured services"""
    featured_services = PujaService.objects.filter(featured=True, is_active=True)[:6]
    all_services = PujaService.objects.filter(is_active=True).count()
    site_config = get_site_config()

    context = {
        'featured_services': featured_services,
        'total_services': all_services,
        'site_config': site_config,
    }
    return render(request, 'services/home.html', context)


def service_list(request):
    """List all puja services with filtering"""
    services = PujaService.objects.filter(is_active=True)
    category = request.GET.get('category')
    site_config = get_site_config()

    if category:
        services = services.filter(category=category)

    categories = PujaService.CATEGORY_CHOICES

    context = {
        'services': services,
        'categories': categories,
        'selected_category': category,
        'site_config': site_config,
    }
    return render(request, 'services/service_list.html', context)


def service_detail(request, pk):
    """Detailed view of a single service"""
    service = get_object_or_404(PujaService, pk=pk, is_active=True)
    site_config = get_site_config()

    context = {
        'service': service,
        'site_config': site_config,
    }
    return render(request, 'services/service_detail.html', context)


def booking(request, service_id):
    """Handle service booking"""
    service = get_object_or_404(PujaService, pk=service_id, is_active=True)
    site_config = get_site_config()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_obj = form.save(commit=False)
            booking_obj.service = service
            booking_obj.total_amount = service.price
            booking_obj.save()

            # Redirect to payment
            return redirect('payment', booking_id=booking_obj.id)
    else:
        form = BookingForm()

    context = {
        'form': form,
        'service': service,
        'site_config': site_config,
    }
    return render(request, 'services/booking.html', context)


def payment(request, booking_id):
    """Initiate Razorpay payment"""
    booking = get_object_or_404(Booking, pk=booking_id)
    site_config = get_site_config()

    if not site_config or not site_config.razorpay_key_id:
        messages.error(request, 'Payment gateway not configured')
        return redirect('service_detail', pk=booking.service.id)

    messages.error(request, f'Error initiating payment: No payment service installed')
    return redirect('service_detail', pk=booking.service.id)
    # Create Razorpay client
    # client = razorpay.Client(auth=(site_config.razorpay_key_id, site_config.razorpay_key_secret))

    try:
        # Create Payment in database
        payment_obj, created = Payment.objects.get_or_create(
            booking=booking,
            defaults={'amount': booking.total_amount, 'status': 'initiated'}
        )

        if created:
            # Create Razorpay order
            razorpay_order = client.order.create(
                data={
                    'amount': int(float(booking.total_amount) * 100),  # Convert to paise
                    'currency': 'INR',
                    'receipt': f'booking_{booking.id}',
                    'payment_capture': 1
                }
            )

            payment_obj.razorpay_order_id = razorpay_order['id']
            payment_obj.save()
        else:
            razorpay_order = {'id': payment_obj.razorpay_order_id}

        context = {
            'booking': booking,
            'payment': payment_obj,
            'razorpay_key': site_config.razorpay_key_id,
            'razorpay_order_id': razorpay_order['id'],
            'amount': int(float(booking.total_amount) * 100),
            'site_config': site_config,
        }
        return render(request, 'services/payment.html', context)

    except Exception as e:
        messages.error(request, f'Error initiating payment: {str(e)}')
        return redirect('service_detail', pk=booking.service.id)


@csrf_exempt
@require_http_methods(['POST'])
def payment_callback(request):
    """Handle Razorpay payment callback"""
    try:
        data = json.loads(request.body)
        payment_id = data.get('razorpay_payment_id')
        order_id = data.get('razorpay_order_id')
        signature = data.get('razorpay_signature')

        # Get payment object
        payment = Payment.objects.get(razorpay_order_id=order_id)
        site_config = get_site_config()

        if not site_config:
            return JsonResponse({'status': 'error', 'message': 'Configuration not found'}, status=400)

        return JsonResponse({'status': 'success', 'booking_id': "1234"})

        # Verify signature
        # client = razorpay.Client(auth=(site_config.razorpay_key_id, site_config.razorpay_key_secret))

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            # Update payment status
            with transaction.atomic():
                payment.razorpay_payment_id = payment_id
                payment.razorpay_signature = signature
                payment.status = 'captured'
                payment.save()

                # Update booking status
                booking = payment.booking
                booking.status = 'confirmed'
                booking.save()

                # Send confirmation email
                send_booking_confirmation_email(booking)

            return JsonResponse({'status': 'success', 'booking_id': booking.id})

        except razorpay.BadSignatureError:
            payment.status = 'failed'
            payment.save()
            return JsonResponse({'status': 'error', 'message': 'Invalid signature'}, status=400)

    except Payment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Payment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def payment_success(request, booking_id):
    """Payment success page"""
    booking = get_object_or_404(Booking, pk=booking_id)
    site_config = get_site_config()

    context = {
        'booking': booking,
        'site_config': site_config,
    }
    return render(request, 'services/payment_success.html', context)


def payment_failed(request, booking_id):
    """Payment failed page"""
    booking = get_object_or_404(Booking, pk=booking_id)
    site_config = get_site_config()

    context = {
        'booking': booking,
        'site_config': site_config,
    }
    return render(request, 'services/payment_failed.html', context)


def send_booking_confirmation_email(booking):
    """Send booking confirmation email to customer"""
    try:
        subject = f'Booking Confirmation - {booking.service.name}'
        message = f"""
        Dear {booking.customer_name},

        Thank you for booking {booking.service.name} with us.

        Booking Details:
        - Service: {booking.service.name}
        - Date: {booking.preferred_date}
        - Total Amount: ₹{booking.total_amount}
        - Status: {booking.get_status_display()}

        We will contact you soon with more details.

        Best regards,
        Haridwar Puja Team
        """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [booking.customer_email])
    except Exception as e:
        print(f"Error sending email: {str(e)}")


def about(request):
    """About page"""
    site_config = get_site_config()
    context = {'site_config': site_config}
    return render(request, 'services/about.html', context)


def contact(request):
    """Contact page"""
    site_config = get_site_config()
    context = {'site_config': site_config}
    return render(request, 'services/contact.html', context)
