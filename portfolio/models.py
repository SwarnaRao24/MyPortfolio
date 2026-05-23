from django.db import models


class Experience(models.Model):
    company_name = models.CharField(max_length=150)
    location = models.CharField(max_length=100, help_text="e.g., Toronto, ON or Remote")
    job_title = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank if currently working here")
    is_current = models.BooleanField(default=False)
    summary = models.TextField(help_text="Core team responsibilities, data architectures, and high-level achievements")

    class Meta:
        ordering = ['-start_date']  # Automatically lists your most recent role at the top

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.CharField(max_length=200, help_text="e.g., Python, PySpark, Databricks, AWS, Django")
    github_url = models.URLField(blank=True, null=True)
    live_demo_url = models.URLField(blank=True, null=True)

    # Foreign Key linking a project to an employer, while allowing independent personal projects
    associated_experience = models.ForeignKey(
        Experience,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='projects',
        help_text="Link this project to a specific employer, or leave blank if it is an independent side-project"
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


# Keep your Experience, Project, and Service models above...

class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    # Stores the selected options as a clean, comma-separated list string (e.g., "TAX, RESUME")
    selected_services = models.TextField(
        help_text="Services selected by the user during booking"
    )

    message = models.TextField(blank=True, null=True, help_text="Additional custom instructions or queries")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Booking from {self.first_name} {self.last_name}"