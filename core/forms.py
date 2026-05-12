from django import forms
from .models import ProjectRequest, MentorRequest, BuilderMentorJoin


class ProjectRequestForm(forms.ModelForm):
    class Meta:
        model = ProjectRequest
        exclude = ['status', 'submitted_at', 'updated_at']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full name', 'class': 'dm-input'}),
            'whatsapp': forms.TextInput(attrs={'placeholder': '+91 XXXXX XXXXX', 'class': 'dm-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com', 'class': 'dm-input'}),
            'college_organization': forms.TextInput(attrs={'placeholder': 'College or organization name', 'class': 'dm-input'}),
            'district_location': forms.TextInput(attrs={'placeholder': 'City / District', 'class': 'dm-input'}),
            'project_title': forms.TextInput(attrs={'placeholder': 'e.g. Smart Agriculture IoT System', 'class': 'dm-input'}),
            'domain': forms.Select(attrs={'class': 'dm-select'}),
            'domain_other': forms.TextInput(attrs={'placeholder': 'Specify domain if Other', 'class': 'dm-input'}),
            'project_description': forms.Textarea(attrs={
                'placeholder': 'Describe the project in detail — what it should do, features, inputs/outputs, hardware, software, expected result...',
                'class': 'dm-textarea', 'rows': 6
            }),
            'deliverable_other': forms.TextInput(attrs={'placeholder': 'Other deliverables...', 'class': 'dm-input'}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'dm-input'}),
            'contact_method': forms.Select(attrs={'class': 'dm-select'}),
            'additional_notes': forms.Textarea(attrs={'placeholder': 'Any additional notes or requirements', 'class': 'dm-textarea', 'rows': 3}),
        }


class MentorRequestForm(forms.ModelForm):
    class Meta:
        model = MentorRequest
        exclude = ['submitted_at', 'updated_at']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full name', 'class': 'dm-input'}),
            'whatsapp': forms.TextInput(attrs={'placeholder': '+91 XXXXX XXXXX', 'class': 'dm-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com', 'class': 'dm-input'}),
            'college_organization': forms.TextInput(attrs={'placeholder': 'College or organization name', 'class': 'dm-input'}),
            'district_location': forms.TextInput(attrs={'placeholder': 'City / District', 'class': 'dm-input'}),
            'domain': forms.Select(attrs={'class': 'dm-select'}),
            'domain_other': forms.TextInput(attrs={'placeholder': 'Specify if Other', 'class': 'dm-input'}),
            'help_required': forms.Textarea(attrs={
                'placeholder': 'Explain your current level, what you are building/learning, problems you face, tools/platforms involved...',
                'class': 'dm-textarea', 'rows': 5
            }),
            'mentorship_type': forms.Select(attrs={'class': 'dm-select'}),
            'mentorship_type_other': forms.TextInput(attrs={'placeholder': 'Specify if Other', 'class': 'dm-input'}),
            'current_status': forms.Select(attrs={'class': 'dm-select'}),
            'preferred_mode': forms.Select(attrs={'class': 'dm-select'}),
            'contact_method': forms.Select(attrs={'class': 'dm-select'}),
            'availability': forms.TextInput(attrs={'placeholder': 'e.g. Evenings 7-9 PM', 'class': 'dm-input'}),
            'event_date': forms.DateInput(attrs={'type': 'date', 'class': 'dm-input'}),
            'additional_notes': forms.Textarea(attrs={'placeholder': 'Any other details', 'class': 'dm-textarea', 'rows': 3}),
        }


class BuilderMentorJoinForm(forms.ModelForm):
    class Meta:
        model = BuilderMentorJoin
        exclude = ['submitted_at', 'updated_at']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full name', 'class': 'dm-input'}),
            'whatsapp': forms.TextInput(attrs={'placeholder': '+91 XXXXX XXXXX', 'class': 'dm-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com', 'class': 'dm-input'}),
            'district_location': forms.TextInput(attrs={'placeholder': 'City / District', 'class': 'dm-input'}),
            'college_organization': forms.TextInput(attrs={'placeholder': 'College or organization (optional)', 'class': 'dm-input'}),
            'role': forms.Select(attrs={'class': 'dm-select'}),
            'primary_domain': forms.Select(attrs={'class': 'dm-select'}),
            'domain_other': forms.TextInput(attrs={'placeholder': 'Specify if Other', 'class': 'dm-input'}),
            'skills_experience': forms.Textarea(attrs={
                'placeholder': 'Describe your skills, tools, hardware, software, frameworks, past projects...',
                'class': 'dm-textarea', 'rows': 5
            }),
            'github': forms.URLInput(attrs={'placeholder': 'https://github.com/username', 'class': 'dm-input'}),
            'linkedin': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/username', 'class': 'dm-input'}),
            'portfolio_website': forms.URLInput(attrs={'placeholder': 'https://yourportfolio.com', 'class': 'dm-input'}),
            'youtube': forms.URLInput(attrs={'placeholder': 'https://youtube.com/@channel', 'class': 'dm-input'}),
            'drive_link': forms.URLInput(attrs={'placeholder': 'Google Drive link', 'class': 'dm-input'}),
            'other_links': forms.Textarea(attrs={'placeholder': 'Any other relevant links', 'class': 'dm-textarea', 'rows': 2}),
            'experience_level': forms.Select(attrs={'class': 'dm-select'}),
            'availability': forms.Select(attrs={'class': 'dm-select'}),
            'why_join': forms.Textarea(attrs={
                'placeholder': 'Why do you want to join DarkMatter? What will you bring to the ecosystem?',
                'class': 'dm-textarea', 'rows': 4
            }),
            'additional_notes': forms.Textarea(attrs={'placeholder': 'Any additional notes', 'class': 'dm-textarea', 'rows': 2}),
        }
