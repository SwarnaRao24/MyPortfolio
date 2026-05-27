import resend
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST
import json
from .models import Experience, Project, Service, ContactMessage, EmailOTP


def home_view(request):
    return render(request, 'portfolio/home.html')


def experience_view(request):
    experiences = Experience.objects.all().order_by('-start_date')
    return render(request, 'portfolio/experience.html', {'experiences': experiences})


def projects_view(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'portfolio/projects.html', {'projects': projects})


def services_view(request):
    services = Service.objects.filter(active=True)
    return render(request, 'portfolio/services.html', {'services': services})


@require_POST
def send_otp_view(request):
    """Sends a 6-digit OTP to the user's email address."""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
    except Exception:
        return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)

    if not email:
        return JsonResponse({'success': False, 'error': 'Email is required.'}, status=400)

    otp = EmailOTP.generate_for(email)

    resend.api_key = settings.RESEND_API_KEY
    try:
        resend.Emails.send({
            "from": "Swarna Rao Group <no-reply@no-reply.theswarnaraogroup.com>",
            "to": [email],
            "subject": "Your Verification Code",
            "html": f"""
                <div style="font-family:monospace;background:#0a0a0a;color:#e5e5e5;padding:32px;border-radius:8px;max-width:500px;">
                    <h2 style="color:#06b6d4;letter-spacing:0.1em;text-transform:uppercase;">Verification Code</h2>
                    <hr style="border-color:#262626;margin:16px 0;">
                    <p>Use the code below to verify your email and complete your booking:</p>
                    <div style="background:#111;border:1px solid #06b6d4;padding:24px;text-align:center;margin:24px 0;">
                        <span style="font-size:36px;font-weight:900;letter-spacing:0.3em;color:#06b6d4;">{otp.code}</span>
                    </div>
                    <p style="color:#737373;font-size:12px;">This code expires in 10 minutes. If you did not request this, ignore this email.</p>
                    <hr style="border-color:#262626;margin:16px 0;">
                    <p style="color:#a3a3a3;font-size:12px;">The Swarna Rao Group &mdash; theswarnaraogroup.com</p>
                </div>
            """
        })
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def contact_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        message_text = request.POST.get('message')
        otp_code = request.POST.get('otp_code', '').strip()

        services_list = request.POST.getlist('services_requested')
        services_string = ", ".join(services_list) if services_list else "None Selected"

        # Verify OTP
        try:
            otp = EmailOTP.objects.filter(email=email, code=otp_code, is_verified=False).latest('created_at')
            if otp.is_expired():
                messages.error(request, "Your verification code has expired. Please request a new one.")
                return render(request, 'portfolio/contact.html')
            otp.is_verified = True
            otp.save()
        except EmailOTP.DoesNotExist:
            messages.error(request, "Invalid verification code. Please check and try again.")
            return render(request, 'portfolio/contact.html')

        # Save to database
        ContactMessage.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            selected_services=services_string,
            message=message_text
        )

        resend.api_key = settings.RESEND_API_KEY

        # Email 1: Notify admin
        try:
            resend.Emails.send({
                "from": "Swarna Rao Group <no-reply@no-reply.theswarnaraogroup.com>",
                "to": [settings.ADMIN_EMAIL],
                "subject": f"New Booking Request — {first_name} {last_name}",
                "html": f"""
                    <div style="font-family:monospace;background:#0a0a0a;color:#e5e5e5;padding:32px;border-radius:8px;max-width:600px;">
                        <h2 style="color:#06b6d4;letter-spacing:0.1em;text-transform:uppercase;">New Booking Request</h2>
                        <hr style="border-color:#262626;margin:16px 0;">
                        <p><strong style="color:#a3a3a3;">Name:</strong> {first_name} {last_name}</p>
                        <p><strong style="color:#a3a3a3;">Email:</strong> {email}</p>
                        <p><strong style="color:#a3a3a3;">Phone:</strong> {phone_number}</p>
                        <p><strong style="color:#a3a3a3;">Services:</strong> {services_string}</p>
                        <p><strong style="color:#a3a3a3;">Message:</strong> {message_text or "None provided"}</p>
                        <hr style="border-color:#262626;margin:16px 0;">
                        <a href="https://theswarnaraogroup.com/admin/portfolio/contactmessage/"
                           style="background:#06b6d4;color:#000;padding:10px 20px;font-weight:900;
                           text-decoration:none;text-transform:uppercase;letter-spacing:0.1em;font-size:12px;">
                            View in Admin Panel
                        </a>
                    </div>
                """
            })
        except Exception:
            pass

        # Email 2: Confirmation to user
        try:
            resend.Emails.send({
                "from": "Swarna Rao Group <no-reply@no-reply.theswarnaraogroup.com>",
                "to": [email],
                "subject": "Your Booking Request Has Been Received",
                "html": f"""
                    <div style="font-family:monospace;background:#0a0a0a;color:#e5e5e5;padding:32px;border-radius:8px;max-width:600px;">
                        <h2 style="color:#06b6d4;letter-spacing:0.1em;text-transform:uppercase;">Booking Confirmed</h2>
                        <hr style="border-color:#262626;margin:16px 0;">
                        <p>Hi <strong>{first_name}</strong>,</p>
                        <p>Your booking request has been received and I will get back to you shortly.</p>
                        <hr style="border-color:#262626;margin:16px 0;">
                        <p><strong style="color:#a3a3a3;">Services:</strong> {services_string}</p>
                        <p><strong style="color:#a3a3a3;">Message:</strong> {message_text or "None provided"}</p>
                        <hr style="border-color:#262626;margin:16px 0;">
                        <p style="color:#a3a3a3;font-size:12px;">
                            The Swarna Rao Group &mdash; Mississauga, Ontario, Canada<br>
                            <a href="https://theswarnaraogroup.com" style="color:#06b6d4;">theswarnaraogroup.com</a>
                        </p>
                    </div>
                """
            })
        except Exception:
            pass

        messages.success(request, "Booking confirmed! Check your email for confirmation details.")
        return redirect('contact')

    return render(request, 'portfolio/contact.html')