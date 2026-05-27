from django.db import models
from django.utils import timezone
import random


class Experience(models.Model):
    company_name = models.CharField(max_length=150)
    location = models.CharField(max_length=100, help_text="e.g., Toronto, ON or Remote")
    job_title = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank if currently working here")
    is_current = models.BooleanField(default=False)
    summary = models.TextField(help_text="Core team responsibilities, data architectures, and high-level achievements")

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.CharField(max_length=200, help_text="e.g., Python, PySpark, Databricks, AWS, Django")
    github_url = models.URLField(blank=True, null=True)
    live_demo_url = models.URLField(blank=True, null=True)
    associated_experience = models.ForeignKey(
        Experience,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='projects',
        help_text="Link this project to a specific employer, or leave blank if independent"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Service(models.Model):
    SERVICE_TYPES = [
        ('WEBSITE', 'Personal/Business Web Services'),
        ('GRAPHIC DESIGN', 'Graphic Design'),
        ('LOGO DESIGN', 'Logo Design'),
        ('TAX', 'Tax Filing'),
        ('RESUME', 'Resume Optimization'),
        ('LINKEDIN', 'LinkedIn Optimization')
    ]
    title = models.CharField(max_length=100)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, help_text="Price in CAD")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - ${self.price} CAD"


class EmailOTP(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=10)

    @classmethod
    def generate_for(cls, email):
        # Delete any existing OTPs for this email
        cls.objects.filter(email=email).delete()
        code = str(random.randint(100000, 999999))
        return cls.objects.create(email=email, code=code)

    def __str__(self):
        return f"OTP for {self.email} — {'verified' if self.is_verified else 'pending'}"


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    selected_services = models.TextField(help_text="Services selected by the user during booking")
    message = models.TextField(blank=True, null=True, help_text="Additional custom instructions or queries")
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        status = "✓ Read" if self.is_read else "🔔 NEW"
        return f"[{status}] Booking from {self.first_name} {self.last_name} — {self.submitted_at.strftime('%b %d, %Y')}"