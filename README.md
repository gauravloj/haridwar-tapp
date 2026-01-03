# Haridwar Puja - Django Website

A complete Django web application for booking authentic Vedic rituals and pujas performed by certified pandits on the banks of the Ganges River in Haridwar.

## Features

✨ **Complete Booking System**
- Service listing and detailed information pages
- Online booking form with customer details
- Secure payment integration with Razorpay
- Booking confirmation emails

🎨 **Beautiful UI with Tailwind CSS**
- Responsive design that works on all devices
- Modern, professional appearance
- Fast and lightweight

💳 **Payment Integration**
- Razorpay payment gateway integration
- Secure payment processing
- Payment success/failure handling
- Automatic booking confirmation on successful payment

🛠️ **Admin Panel**
- Manage puja services
- View and manage bookings
- Track payments
- Manage pandits/priests
- Configure site settings

## Quick Start

### 1. Environment Setup

```bash
cd /Users/mihawk/Desktop/openproj/haridwar
source venv/bin/activate  # or use: hatch shell
```

### 2. Configure Environment Variables

Edit `.env` file:
```bash
# Add your Razorpay credentials
RAZORPAY_KEY_ID=rzp_test_xxxxx
RAZORPAY_KEY_SECRET=xxxxx
```

### 3. Run Migrations (if not already done)

```bash
hatch run python manage.py migrate
```

### 4. Create Admin User (if not already done)

```bash
hatch run python manage.py createsuperuser
```

### 5. Start Development Server

```bash
hatch run python manage.py runserver
```

Visit http://127.0.0.1:8000/

### 6. Admin Panel

Go to http://127.0.0.1:8000/admin/ and create:
1. **Site Configuration** - Add your contact details
2. **Pandits** - Add priest information
3. **Puja Services** - Add service offerings

## Razorpay Setup

1. Sign up at https://razorpay.com
2. Get API Keys from Dashboard → Settings → API Keys
3. Add to `.env`:
   ```
   RAZORPAY_KEY_ID=your_key_id
   RAZORPAY_KEY_SECRET=your_key_secret
   ```
4. Use test card: 4111 1111 1111 1111

## Project Structure

- `haridwarpuja/` - Main Django project
- `services/` - Services app (models, views, forms)
- `theme/` - Tailwind CSS theme
- `templates/` - HTML templates
- `static/` - CSS, JS, images
- `.env` - Environment configuration

## Models

- **Pandit** - Priest information
- **PujaService** - Service offerings
- **Booking** - Customer bookings
- **Payment** - Payment transactions
- **SiteConfig** - Site settings

## Key Features

✅ Service listing and details
✅ Online booking form
✅ Razorpay payment integration
✅ Payment webhooks
✅ Admin management
✅ Responsive design
✅ Email notifications
✅ WhatsApp integration

## Support & Help

For detailed documentation, see the full README or Django docs at https://docs.djangoproject.com/

