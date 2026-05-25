from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
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

        # Send email notification to admin
        subject = f"🔔 New Booking Request — {first_name} {last_name}"
        body = f"""
NEW BOOKING REQUEST
===================

Name:     {first_name} {last_name}
Email:    {email}
Phone:    {phone_number}

Services Requested:
{services_string}

Additional Message:
{message_text or "None provided"}

===================
Submitted via The Swarna Rao Group website.
Review it in your admin panel: http://67.205.170.7/admin/portfolio/contactmessage/
        """.strip()

        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
        except Exception:
            # Don't crash the user's experience if email fails
            pass

        messages.success(request,
                         "Your booking request has logged onto the grid! I'll contact you manually over email shortly.")
        return redirect('contact')

    return render(request, 'portfolio/contact.html')