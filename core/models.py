import uuid
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Minimal public profile, linked 1-to-1 with Django's built-in User."""
    ROLE_TAG_CHOICES = [
        ('none', 'None'),
        ('builder', 'Builder'),
        ('mentor', 'Mentor'),
        ('both', 'Builder & Mentor'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Permanent User ID')
    approved_role = models.CharField(
        max_length=10,
        choices=ROLE_TAG_CHOICES,
        default='none',
        verbose_name='Builder/Mentor Tag',
        help_text='Set automatically when an application is approved by admin.',
    )
    is_accepting_work = models.BooleanField(
        default=True, 
        verbose_name='Accepting Work',
        help_text='Builder availability toggle.'
    )

    def __str__(self):
        return f"Profile({self.user.username})"


class ApprovedBuilder(UserProfile):
    class Meta:
        proxy = True
        verbose_name = 'Builder'
        verbose_name_plural = 'Builders'


class ApprovedMentor(UserProfile):
    class Meta:
        proxy = True
        verbose_name = 'Mentor'
        verbose_name_plural = 'Mentors'


class ProjectRequest(models.Model):
    DOMAIN_CHOICES = [
        ('iot', 'IoT'),
        ('robotics', 'Robotics'),
        ('drone', 'Drone'),
        ('rover', 'Rover'),
        ('web', 'Web Development'),
        ('app', 'App Development'),
        ('embedded', 'Embedded Systems'),
        ('ai', 'AI/Automation'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewing', 'Reviewing'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    CONTACT_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('call', 'Call'),
        ('email', 'Email'),
    ]

    # Basic Info
    full_name = models.CharField(max_length=200)
    whatsapp = models.CharField(max_length=20)
    email = models.EmailField()
    college_organization = models.CharField(max_length=300)
    district_location = models.CharField(max_length=200)

    # Project Info
    project_title = models.CharField(max_length=300)
    domain = models.CharField(max_length=50, choices=DOMAIN_CHOICES)
    domain_other = models.CharField(max_length=100, blank=True)
    project_description = models.TextField()

    # Deliverables (multiple choice stored as JSON-like text)
    deliverable_working_project = models.BooleanField(default=False)
    deliverable_source_code = models.BooleanField(default=False)
    deliverable_documentation = models.BooleanField(default=False)
    deliverable_report = models.BooleanField(default=False)
    deliverable_ppt = models.BooleanField(default=False)
    deliverable_circuit_diagram = models.BooleanField(default=False)
    deliverable_mobile_app = models.BooleanField(default=False)
    deliverable_website = models.BooleanField(default=False)
    deliverable_live_demo = models.BooleanField(default=False)
    deliverable_other = models.CharField(max_length=200, blank=True)

    deadline = models.DateField(null=True, blank=True)
    reference_files = models.FileField(upload_to='project_references/', blank=True, null=True)
    contact_method = models.CharField(max_length=20, choices=CONTACT_CHOICES, default='whatsapp')
    additional_notes = models.TextField(blank=True)

    # Meta
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='project_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Project Request'
        verbose_name_plural = 'Project Requests'

    def __str__(self):
        return f"{self.project_title} — {self.full_name}"


class MentorRequest(models.Model):
    DOMAIN_CHOICES = [
        ('iot', 'IoT'),
        ('robotics', 'Robotics'),
        ('drone', 'Drone Development'),
        ('rover', 'Rover Systems'),
        ('embedded', 'Embedded Systems'),
        ('web', 'Web Development'),
        ('app', 'App Development'),
        ('ai', 'AI / Automation'),
        ('pcb', 'PCB / Electronics'),
        ('cad', 'CAD / Mechanical Design'),
        ('cybersecurity', 'Cybersecurity'),
        ('other', 'Other'),
    ]
    MENTORSHIP_TYPE_CHOICES = [
        ('workshop', 'College Workshop Mentor'),
        ('project_guidance', 'Project Guidance'),
        ('debugging', 'Debugging Help'),
        ('architecture', 'Architecture / Planning'),
        ('learning', 'Learning Support'),
        ('viva', 'Viva / Presentation Preparation'),
        ('code_review', 'Code Review'),
        ('hardware', 'Hardware Assistance'),
        ('career', 'Career Guidance'),
        ('research', 'Research Guidance'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('just_starting', 'Just Starting'),
        ('in_development', 'In Development'),
        ('nearly_complete', 'Nearly Complete'),
        ('stuck', 'Stuck on Specific Issues'),
        ('need_full', 'Need Full Guidance'),
    ]
    MODE_CHOICES = [
        ('chat', 'Chat Support'),
        ('voice', 'Voice Call'),
        ('video', 'Video Call'),
        ('live', 'Live Session'),
        ('inperson', 'In-Person'),
    ]
    CONTACT_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('call', 'Call'),
        ('email', 'Email'),
    ]

    full_name = models.CharField(max_length=200)
    whatsapp = models.CharField(max_length=20)
    email = models.EmailField()
    college_organization = models.CharField(max_length=300)
    district_location = models.CharField(max_length=200)

    domain = models.CharField(max_length=50, choices=DOMAIN_CHOICES)
    domain_other = models.CharField(max_length=100, blank=True)
    help_required = models.TextField()

    mentorship_type = models.CharField(max_length=50, choices=MENTORSHIP_TYPE_CHOICES)
    mentorship_type_other = models.CharField(max_length=100, blank=True)
    current_status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    preferred_mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    contact_method = models.CharField(max_length=20, choices=CONTACT_CHOICES, default='whatsapp')

    reference_files = models.FileField(upload_to='mentor_references/', blank=True, null=True)
    availability = models.CharField(max_length=200, blank=True)
    event_date = models.DateField(null=True, blank=True)
    additional_notes = models.TextField(blank=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='mentor_requests')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Mentor Request'
        verbose_name_plural = 'Mentor Requests'

    def __str__(self):
        return f"Mentor Request — {self.full_name} ({self.get_domain_display()})"


class BuilderMentorJoin(models.Model):
    ROLE_CHOICES = [
        ('builder', 'Builder'),
        ('mentor', 'Mentor'),
        ('both', 'Both'),
    ]
    DOMAIN_CHOICES = [
        ('iot', 'IoT'),
        ('robotics', 'Robotics'),
        ('drone', 'Drone Development'),
        ('rover', 'Rover Systems'),
        ('embedded', 'Embedded Systems'),
        ('electronics', 'Electronics'),
        ('web', 'Web Development'),
        ('app', 'App Development'),
        ('ai', 'AI / Automation'),
        ('cybersecurity', 'Cybersecurity'),
        ('cad', 'CAD / 3D Design'),
        ('pcb', 'PCB Design'),
        ('mechanical', 'Mechanical Systems'),
        ('other', 'Other'),
    ]
    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('industry', 'Industry Level'),
    ]
    AVAILABILITY_CHOICES = [
        ('occasionally', 'Occasionally'),
        ('weekends', 'Weekends'),
        ('flexible', 'Flexible'),
        ('active', 'Active Contributor'),
    ]

    full_name = models.CharField(max_length=200)
    whatsapp = models.CharField(max_length=20)
    email = models.EmailField()
    district_location = models.CharField(max_length=200)
    college_organization = models.CharField(max_length=300, blank=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    primary_domain = models.CharField(max_length=50, choices=DOMAIN_CHOICES)
    domain_other = models.CharField(max_length=100, blank=True)
    skills_experience = models.TextField()

    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    portfolio_website = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    drive_link = models.URLField(blank=True)
    other_links = models.TextField(blank=True)

    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)

    # Contribution interests
    contrib_paid_builds = models.BooleanField(default=False)
    contrib_mentorship = models.BooleanField(default=False)
    contrib_technical_guidance = models.BooleanField(default=False)
    contrib_research = models.BooleanField(default=False)
    contrib_collaboration = models.BooleanField(default=False)
    contrib_community = models.BooleanField(default=False)
    contrib_workshops = models.BooleanField(default=False)

    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES)
    resume_file = models.FileField(upload_to='builder_files/', blank=True, null=True)
    why_join = models.TextField()
    additional_notes = models.TextField(blank=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='builder_joins')
    is_approved = models.BooleanField(default=False, verbose_name='Approved')
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name='Approved At')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Builder/Mentor Application'
        verbose_name_plural = 'Builder/Mentor Applications'

    def __str__(self):
        return f"{self.get_role_display()} — {self.full_name} ({self.get_primary_domain_display()})"
