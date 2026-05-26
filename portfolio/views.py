import resend
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import Experience, Project, Service, ContactMessage


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


def contact_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        message_text = request.POST.get('message')

        services_list = request.POST.getlist('services_requested')
        services_string = ", ".join(services_list) if services_list else "None Selected"

        # Save to database
        ContactMessage.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            selected_services=services_string,
            message=message_text
        )

        # Configure Resend API key
        resend.api_key = settings.RESEND_API_KEY

        # --- Email 1: Notify admin ---
        try:
            resend.Emails.send({
                "from": "The Swarna Rao Group <no-reply@no-reply.theswarnaraogroup.com>",
                "to": [settings.ADMIN_EMAIL],
                "subject": f"New Booking Request — {first_name} {last_name}",
                "html": f"""
                    <div style="font-family:monospace;background:#0a0a0a;color:#e5e5e5;padding:32px;border-radius:8px;max-width:600px;">
                        <h2 style="color:#06b6d4;letter-spacing:0.1em;text-transform:uppercase;">New Booking Request</h2>
                        <hr style="border-color:#262626;margin:16px 0;">
                        <p><strong style="color:#a3a3a3;">Name:</strong> {first_name} {last_name}</p>
                        <p><strong style="color:#a3a3a3;">Email:</strong> {email}</p>
                        <p><strong style="color:#a3a3a3;">Phone:</strong> {phone_number}</p>
                        <p><strong style="color:#a3a3a3;">Services Requested:</strong> {services_string}</p>
                        <p><strong style="color:#a3a3a3;">Message:</strong> {message_text or "None provided"}</p>
                        <hr style="border-color:#262626;margin:16px 0;">
                        <a href="https://www.theswarnaraogroup.com/admin/portfolio/contactmessage/"
                           style="background:#06b6d4;color:#000;padding:10px 20px;font-weight:900;
                           text-decoration:none;text-transform:uppercase;letter-spacing:0.1em;font-size:12px;">
                            View in Admin Panel
                        </a>
                    </div>
                """
            })
        except Exception:
            pass

        # --- Email 2: Confirmation to user ---
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
                        <p>Thank you for reaching out! Your booking request has been received and I will get back to you shortly.</p>
                        <hr style="border-color:#262626;margin:16px 0;">
                        <p><strong style="color:#a3a3a3;">Services Requested:</strong> {services_string}</p>
                        <p><strong style="color:#a3a3a3;">Your Message:</strong> {message_text or "None provided"}</p>
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

        messages.success(request,
                         "Your booking request has logged onto the grid! I'll contact you manually over email shortly.")
        return redirect('contact')

    return render(request, 'portfolio/contact.html')