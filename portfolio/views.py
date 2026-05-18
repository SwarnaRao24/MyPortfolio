from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Experience, Project, Service, ContactMessage


def home_view(request):
    # This renders your detailed biography landing page
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

        # Capture all checked values from the 'services_requested' checkbox group
        services_list = request.POST.getlist('services_requested')
        # Convert list array into a single clean text string: "Tax Filing, Resume Strategy"
        services_string = ", ".join(services_list) if services_list else "None Selected"

        # Inject straight into your database
        ContactMessage.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            selected_services=services_string,
            message=message_text
        )

        messages.success(request,
                         "Your booking request has logged onto the grid! I'll contact you manually over email shortly.")
        return redirect('contact')

    return render(request, 'portfolio/contact.html')