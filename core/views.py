from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ProjectRequestForm, MentorRequestForm, BuilderMentorJoinForm
from .models import UserProfile


# ─── Public pages ──────────────────────────────────────────────────────────────

def home(request):
    return render(request, 'core/home.html')


@login_required(login_url='/account/login/?next=/project-request/')
def project_request(request):
    if request.method == 'POST':
        form = ProjectRequestForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'project_request')
            return redirect('success')
    else:
        form = ProjectRequestForm()
    return render(request, 'core/project_request.html', {'form': form})


@login_required(login_url='/account/login/?next=/mentor-request/')
def mentor_request(request):
    if request.method == 'POST':
        form = MentorRequestForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'mentor_request')
            return redirect('success')
    else:
        form = MentorRequestForm()
    return render(request, 'core/mentor_request.html', {'form': form})


@login_required(login_url='/account/login/?next=/builder-join/')
def builder_join(request):
    if request.method == 'POST':
        form = BuilderMentorJoinForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'builder_join')
            return redirect('success')
    else:
        form = BuilderMentorJoinForm()
    return render(request, 'core/builder_join.html', {'form': form})


def success(request):
    form_type = None
    for msg in messages.get_messages(request):
        form_type = str(msg)
    return render(request, 'core/success.html', {'form_type': form_type})


# ─── User Account ───────────────────────────────────────────────────────────────

def user_register(request):
    if request.user.is_authenticated:
        return redirect('account_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        errors = []
        if not username:
            errors.append('Username is required.')
        elif User.objects.filter(username=username).exists():
            errors.append('That username is already taken.')
        if not email:
            errors.append('Email is required.')
        elif User.objects.filter(email=email).exists():
            errors.append('An account with that email already exists.')
        if len(password1) < 8:
            errors.append('Password must be at least 8 characters.')
        if password1 != password2:
            errors.append('Passwords do not match.')
        if errors:
            return render(request, 'core/user_register.html', {'errors': errors, 'username': username, 'email': email})
        user = User.objects.create_user(username=username, email=email, password=password1)
        UserProfile.objects.create(user=user)
        login(request, user)
        messages.success(request, 'Account created successfully! Welcome to DarkMatter.')
        return redirect('account_dashboard')
    return render(request, 'core/user_register.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('account_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'account_dashboard'))
        return render(request, 'core/user_login.html', {'error': 'Invalid username or password.', 'username': username})
    return render(request, 'core/user_login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/account/login/')
def account_dashboard(request):
    project_requests = request.user.project_requests.all().order_by('-submitted_at')
    mentor_requests = request.user.mentor_requests.all().order_by('-submitted_at')
    builder_apps = request.user.builder_joins.all().order_by('-submitted_at')
    profile = getattr(request.user, 'profile', None)
    return render(request, 'core/account_dashboard.html', {
        'project_requests': project_requests,
        'mentor_requests': mentor_requests,
        'builder_apps': builder_apps,
        'profile': profile,
    })


@login_required(login_url='/account/login/')
def account_settings(request):
    user = request.user
    errors = []
    success_msg = None
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_info':
            new_username = request.POST.get('username', '').strip()
            new_email = request.POST.get('email', '').strip()
            if not new_username:
                errors.append('Username cannot be empty.')
            elif new_username != user.username and User.objects.filter(username=new_username).exists():
                errors.append('That username is already taken.')
            if not new_email:
                errors.append('Email cannot be empty.')
            elif new_email != user.email and User.objects.filter(email=new_email).exists():
                errors.append('That email is already in use.')
            if not errors:
                user.username = new_username
                user.email = new_email
                user.save()
                success_msg = 'Profile updated successfully.'
        elif action == 'change_password':
            current = request.POST.get('current_password', '')
            new1 = request.POST.get('new_password1', '')
            new2 = request.POST.get('new_password2', '')
            if not user.check_password(current):
                errors.append('Current password is incorrect.')
            elif len(new1) < 8:
                errors.append('New password must be at least 8 characters.')
            elif new1 != new2:
                errors.append('New passwords do not match.')
            if not errors:
                user.set_password(new1)
                user.save()
                update_session_auth_hash(request, user)
                success_msg = 'Password changed successfully.'
    return render(request, 'core/account_settings.html', {
        'errors': errors,
        'success_msg': success_msg,
    })


@login_required(login_url='/account/login/')
def toggle_work_status(request):
    if request.method == 'POST':
        profile = getattr(request.user, 'profile', None)
        if profile and profile.approved_role in ['builder', 'both']:
            profile.is_accepting_work = not profile.is_accepting_work
            profile.save(update_fields=['is_accepting_work'])
            status_text = 'Accepting Work' if profile.is_accepting_work else 'Not Accepting Work'
            messages.success(request, f'Availability status updated to: {status_text}')
    return redirect('account_dashboard')
