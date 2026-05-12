from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html, mark_safe
from .models import ProjectRequest, MentorRequest, BuilderMentorJoin, UserProfile, ApprovedBuilder, ApprovedMentor


# ─── Inlines ───────────────────────────────────────────────────────────────────

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = 'Profile'
    verbose_name_plural = 'Profile'
    readonly_fields = ('uid', 'role_tag_display')
    fields = ('uid', 'approved_role', 'role_tag_display')

    def role_tag_display(self, obj):
        if not obj or not obj.pk:
            return '—'
        colors = {
            'builder': '#00ff88',
            'mentor': '#00ccff',
            'both': '#ffcc00',
            'none': '#555555',
        }
        color = colors.get(obj.approved_role, '#555555')
        label = obj.get_approved_role_display()
        return format_html(
            '<span style="background:{};color:#000;padding:3px 10px;border-radius:12px;'
            'font-size:12px;font-weight:bold">{}</span>',
            color, label
        )
    role_tag_display.short_description = 'Current Tag'


class ProjectRequestInline(admin.TabularInline):
    model = ProjectRequest
    extra = 0
    can_delete = False
    show_change_link = True
    readonly_fields = ('project_title', 'domain', 'status', 'submitted_at')
    fields = ('project_title', 'domain', 'status', 'submitted_at')
    verbose_name = 'Project Request'
    verbose_name_plural = 'Project Requests'

    def has_add_permission(self, request, obj=None):
        return False


class MentorRequestInline(admin.TabularInline):
    model = MentorRequest
    extra = 0
    can_delete = False
    show_change_link = True
    readonly_fields = ('domain', 'mentorship_type', 'current_status', 'submitted_at')
    fields = ('domain', 'mentorship_type', 'current_status', 'submitted_at')
    verbose_name = 'Mentor Request'
    verbose_name_plural = 'Mentor Requests'

    def has_add_permission(self, request, obj=None):
        return False


class BuilderJoinInline(admin.TabularInline):
    model = BuilderMentorJoin
    extra = 0
    can_delete = False
    show_change_link = True
    readonly_fields = ('role', 'primary_domain', 'experience_level', 'is_approved', 'submitted_at')
    fields = ('role', 'primary_domain', 'experience_level', 'is_approved', 'submitted_at')
    verbose_name = 'Builder / Mentor Application'
    verbose_name_plural = 'Builder / Mentor Applications'

    def has_add_permission(self, request, obj=None):
        return False


# ─── Extended User Admin ───────────────────────────────────────────────────────

class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, ProjectRequestInline, MentorRequestInline, BuilderJoinInline)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# ─── UserProfile Admin ─────────────────────────────────────────────────────────

# Shared badge helpers (module-level so they can be reused)
_ROLE_COLORS = {'builder': '#00ff88', 'mentor': '#00ccff', 'both': '#ffcc00', 'none': '#444444'}
_DOM_COLORS = {
    'iot': '#00ff88', 'robotics': '#00ccff', 'drone': '#ffcc00', 'web': '#ff6644',
    'app': '#cc88ff', 'embedded': '#44ffcc', 'ai': '#ff44aa', 'rover': '#88ff44',
    'pcb': '#ffaa44', 'cad': '#44aaff', 'cybersecurity': '#ff4488', 'other': '#aaaaaa',
    'electronics': '#88ccff', 'mechanical': '#ffcc88',
}
_STATUS_COLORS = {
    'pending': '#ffcc00', 'reviewing': '#00ccff', 'accepted': '#00ff88',
    'in_progress': '#ff8800', 'completed': '#44ff44', 'rejected': '#ff4444',
}

def _badge(text, color, text_color='#000'):
    return (
        f'<span style="background:{color};color:{text_color};padding:2px 9px;'
        f'border-radius:10px;font-size:11px;font-weight:bold;white-space:nowrap">{text}</span>'
    )


def _user_tag_cell(user):
    """Returns HTML showing username link + role tag for use in any admin list view."""
    if not user:
        return '<span style="color:#555">— anonymous —</span>'
    url = reverse('admin:auth_user_change', args=[user.pk])
    html = f'<a href="{url}"><strong>{user.username}</strong></a>'
    try:
        role = user.profile.approved_role
        if role and role != 'none':
            color = _ROLE_COLORS.get(role, '#444')
            html += ' ' + _badge(user.profile.get_approved_role_display(), color)
    except Exception:
        pass
    return html


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # ── List view ──────────────────────────────────────────────────────────────
    list_display = (
        'account_info',
        'role_tag_pill',
        'availability_badge',
        'project_req_badge',
        'mentor_req_badge',
        'builder_app_badge',
        'last_seen',
    )
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('approved_role', 'is_accepting_work')
    list_per_page = 30

    # ── Detail view ────────────────────────────────────────────────────────────
    readonly_fields = (
        'uid',
        'account_details_panel',
        'project_requests_panel',
        'mentor_requests_panel',
        'builder_apps_panel',
    )
    fields = (
        'uid',
        'approved_role',
        'is_accepting_work',
        'account_details_panel',
        'project_requests_panel',
        'mentor_requests_panel',
        'builder_apps_panel',
    )

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .select_related('user')
            .prefetch_related(
                'user__project_requests',
                'user__mentor_requests',
                'user__builder_joins',
            )
        )

    # ── List column: combined username + email ─────────────────────────────────
    def account_info(self, obj):
        u = obj.user
        name = f'{u.first_name} {u.last_name}'.strip() or '—'
        url = reverse('admin:auth_user_change', args=[u.pk])
        return format_html(
            '<strong><a href="{}">{}</a></strong><br>'
            '<small style="color:#aaa">{}</small><br>'
            '<small style="color:#888">{}</small>',
            url, u.username, u.email, name
        )
    account_info.short_description = 'Account'
    account_info.admin_order_field = 'user__username'

    # ── List column: role pill ─────────────────────────────────────────────────
    def role_tag_pill(self, obj):
        color = _ROLE_COLORS.get(obj.approved_role, '#444')
        return mark_safe(_badge(obj.get_approved_role_display(), color))
    role_tag_pill.short_description = '🏷 Tag'
    role_tag_pill.admin_order_field = 'approved_role'

    # ── List column: availability badge ───────────────────────────────────────
    def availability_badge(self, obj):
        if obj.approved_role in ['builder', 'both']:
            if obj.is_accepting_work:
                return mark_safe(_badge('🟢 Accepting Work', '#00ff88'))
            else:
                return mark_safe(_badge('⚪ Not Accepting Work', '#aaaaaa'))
        return mark_safe('<span style="color:#555">—</span>')
    availability_badge.short_description = 'Availability'
    availability_badge.admin_order_field = 'is_accepting_work'

    # ── List column: request count badges ─────────────────────────────────────
    def project_req_badge(self, obj):
        n = obj.user.project_requests.count()
        color = '#00ccff' if n else '#333'
        return mark_safe(_badge(f'📋 {n}', color))
    project_req_badge.short_description = 'Projects'

    def mentor_req_badge(self, obj):
        n = obj.user.mentor_requests.count()
        color = '#cc88ff' if n else '#333'
        return mark_safe(_badge(f'🎓 {n}', color))
    mentor_req_badge.short_description = 'Mentors'

    def builder_app_badge(self, obj):
        apps = obj.user.builder_joins.all()
        n = apps.count()
        approved = apps.filter(is_approved=True).count()
        if n == 0:
            return mark_safe(_badge('🛠 0', '#333'))
        color = '#00ff88' if approved else '#ffcc00'
        label = f'🛠 {n}' + (f' ✅{approved}' if approved else '')
        return mark_safe(_badge(label, color))
    builder_app_badge.short_description = 'Builder Apps'

    # ── List column: last login ────────────────────────────────────────────────
    def last_seen(self, obj):
        u = obj.user
        if u.last_login:
            return format_html(
                '<small style="color:#aaa">{}</small>',
                u.last_login.strftime('%d %b %Y %H:%M')
            )
        return format_html('<small style="color:#555">Never</small>')
    last_seen.short_description = 'Last Login'
    last_seen.admin_order_field = 'user__last_login'

    # ── Detail: full account credentials panel ────────────────────────────────
    def account_details_panel(self, obj):
        u = obj.user
        joined = u.date_joined.strftime('%d %b %Y %H:%M') if u.date_joined else '—'
        last   = u.last_login.strftime('%d %b %Y %H:%M') if u.last_login else 'Never'
        active  = '✅ Active'  if u.is_active  else '❌ Inactive'
        staff   = '🔑 Staff'   if u.is_staff   else '—'
        superuser = '👑 Superuser' if u.is_superuser else '—'
        name = f'{u.first_name} {u.last_name}'.strip() or '—'
        uid_str = str(obj.uid)
        
        availability_html = ''
        if obj.approved_role in ['builder', 'both']:
            av_status = "🟢 Accepting Work" if obj.is_accepting_work else "⚪ Not Accepting Work"
            availability_html = f'<tr style="background:#111"><td style="padding:6px 12px;color:#888">Builder Availability</td><td style="padding:6px 12px"><strong>{av_status}</strong></td></tr>'

        html = f'''
        <table style="border-collapse:collapse;width:100%;max-width:680px;font-size:13px">
          <tr style="background:#1a1a2e">
            <th colspan="2" style="padding:8px 12px;text-align:left;color:#00ccff;letter-spacing:1px">🔐 ACCOUNT &amp; LOGIN DETAILS</th>
          </tr>
          <tr><td style="padding:6px 12px;color:#888;width:160px">Username</td><td style="padding:6px 12px"><strong>{u.username}</strong></td></tr>
          <tr style="background:#111"><td style="padding:6px 12px;color:#888">Email</td><td style="padding:6px 12px">{u.email}</td></tr>
          <tr><td style="padding:6px 12px;color:#888">Full Name</td><td style="padding:6px 12px">{name}</td></tr>
          <tr style="background:#111"><td style="padding:6px 12px;color:#888">Permanent UID</td><td style="padding:6px 12px"><code style="font-size:11px;color:#888">{uid_str}</code></td></tr>
          <tr><td style="padding:6px 12px;color:#888">Date Joined</td><td style="padding:6px 12px">{joined}</td></tr>
          <tr style="background:#111"><td style="padding:6px 12px;color:#888">Last Login</td><td style="padding:6px 12px">{last}</td></tr>
          <tr><td style="padding:6px 12px;color:#888">Status</td><td style="padding:6px 12px">{active} &nbsp; {staff} &nbsp; {superuser}</td></tr>
          {availability_html}
        </table>
        '''
        return mark_safe(html)
    account_details_panel.short_description = ''


    def project_requests_panel(self, obj):
        qs = obj.user.project_requests.all().order_by('-submitted_at')
        if not qs.exists():
            return mark_safe('<p style="color:#555;font-style:italic">No project requests submitted.</p>')
        rows = ''
        for r in qs:
            url = reverse('admin:core_projectrequest_change', args=[r.pk])
            sc = _STATUS_COLORS.get(r.status, '#aaa')
            dc = _DOM_COLORS.get(r.domain, '#aaa')
            rows += (
                f'<tr>'
                f'<td style="padding:6px 10px"><a href="{url}"><strong>{r.project_title}</strong></a></td>'
                f'<td style="padding:6px 10px">{_badge(r.get_domain_display(), dc)}</td>'
                f'<td style="padding:6px 10px">{_badge(r.get_status_display(), sc)}</td>'
                f'<td style="padding:6px 10px;color:#888;font-size:12px">{r.submitted_at.strftime("%d %b %Y")}</td>'
                f'<td style="padding:6px 10px;color:#aaa;font-size:12px">{r.full_name}</td>'
                f'</tr>'
            )
        html = f'''
        <table style="border-collapse:collapse;width:100%;max-width:760px;font-size:13px">
          <tr style="background:#1a1a2e">
            <th colspan="5" style="padding:8px 12px;text-align:left;color:#00ccff;letter-spacing:1px">📋 PROJECT REQUESTS ({qs.count()})</th>
          </tr>
          <tr style="background:#111;color:#666;font-size:11px">
            <th style="padding:5px 10px;text-align:left">Title</th>
            <th style="padding:5px 10px;text-align:left">Domain</th>
            <th style="padding:5px 10px;text-align:left">Status</th>
            <th style="padding:5px 10px;text-align:left">Submitted</th>
            <th style="padding:5px 10px;text-align:left">Name on Form</th>
          </tr>
          {rows}
        </table>
        '''
        return mark_safe(html)
    project_requests_panel.short_description = ''

    # ── Detail: mentor requests table ─────────────────────────────────────────
    def mentor_requests_panel(self, obj):
        qs = obj.user.mentor_requests.all().order_by('-submitted_at')
        if not qs.exists():
            return mark_safe('<p style="color:#555;font-style:italic">No mentor requests submitted.</p>')
        rows = ''
        for r in qs:
            url = reverse('admin:core_mentorrequest_change', args=[r.pk])
            dc = _DOM_COLORS.get(r.domain, '#aaa')
            rows += (
                f'<tr>'
                f'<td style="padding:6px 10px"><a href="{url}">{r.full_name}</a></td>'
                f'<td style="padding:6px 10px">{_badge(r.get_domain_display(), dc)}</td>'
                f'<td style="padding:6px 10px;color:#ccc">{r.get_mentorship_type_display()}</td>'
                f'<td style="padding:6px 10px;color:#ccc">{r.get_preferred_mode_display()}</td>'
                f'<td style="padding:6px 10px;color:#888;font-size:12px">{r.submitted_at.strftime("%d %b %Y")}</td>'
                f'</tr>'
            )
        html = f'''
        <table style="border-collapse:collapse;width:100%;max-width:760px;font-size:13px">
          <tr style="background:#1a1a2e">
            <th colspan="5" style="padding:8px 12px;text-align:left;color:#cc88ff;letter-spacing:1px">🎓 MENTOR REQUESTS ({qs.count()})</th>
          </tr>
          <tr style="background:#111;color:#666;font-size:11px">
            <th style="padding:5px 10px;text-align:left">Name on Form</th>
            <th style="padding:5px 10px;text-align:left">Domain</th>
            <th style="padding:5px 10px;text-align:left">Type</th>
            <th style="padding:5px 10px;text-align:left">Mode</th>
            <th style="padding:5px 10px;text-align:left">Submitted</th>
          </tr>
          {rows}
        </table>
        '''
        return mark_safe(html)
    mentor_requests_panel.short_description = ''

    # ── Detail: builder / mentor applications table ────────────────────────────
    def builder_apps_panel(self, obj):
        qs = obj.user.builder_joins.all().order_by('-submitted_at')
        if not qs.exists():
            return mark_safe('<p style="color:#555;font-style:italic">No builder/mentor applications submitted.</p>')
        rows = ''
        for r in qs:
            url = reverse('admin:core_buildermentorjoin_change', args=[r.pk])
            rc = _ROLE_COLORS.get(r.role, '#aaa')
            dc = _DOM_COLORS.get(r.primary_domain, '#aaa')
            appr = _badge('✅ Approved', '#00ff88') if r.is_approved else _badge('⏳ Pending', '#ffcc00')
            rows += (
                f'<tr>'
                f'<td style="padding:6px 10px"><a href="{url}">{r.full_name}</a></td>'
                f'<td style="padding:6px 10px">{_badge(r.get_role_display(), rc)}</td>'
                f'<td style="padding:6px 10px">{_badge(r.get_primary_domain_display(), dc)}</td>'
                f'<td style="padding:6px 10px">{appr}</td>'
                f'<td style="padding:6px 10px;color:#888;font-size:12px">{r.submitted_at.strftime("%d %b %Y")}</td>'
                f'</tr>'
            )
        html = f'''
        <table style="border-collapse:collapse;width:100%;max-width:760px;font-size:13px">
          <tr style="background:#1a1a2e">
            <th colspan="5" style="padding:8px 12px;text-align:left;color:#00ff88;letter-spacing:1px">🛠 BUILDER / MENTOR APPLICATIONS ({qs.count()})</th>
          </tr>
          <tr style="background:#111;color:#666;font-size:11px">
            <th style="padding:5px 10px;text-align:left">Name on Form</th>
            <th style="padding:5px 10px;text-align:left">Role</th>
            <th style="padding:5px 10px;text-align:left">Domain</th>
            <th style="padding:5px 10px;text-align:left">Status</th>
            <th style="padding:5px 10px;text-align:left">Submitted</th>
          </tr>
          {rows}
        </table>
        '''
        return mark_safe(html)
    builder_apps_panel.short_description = ''


# ─── ApprovedBuilder & ApprovedMentor Admins ───────────────────────────────────

@admin.register(ApprovedBuilder)
class ApprovedBuilderAdmin(UserProfileAdmin):
    list_display = ('account_info', 'role_tag_pill', 'domain_info', 'skill_level_info', 'availability_badge', 'contact_info_builder')
    list_filter = ('is_accepting_work',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(approved_role__in=['builder', 'both'])

    def domain_info(self, obj):
        join = obj.user.builder_joins.filter(is_approved=True).order_by('-approved_at').first()
        if join:
            return format_html('<strong>{}</strong>', join.get_primary_domain_display())
        return '—'
    domain_info.short_description = 'Domain'

    def skill_level_info(self, obj):
        join = obj.user.builder_joins.filter(is_approved=True).order_by('-approved_at').first()
        if join:
            return join.get_experience_level_display()
        return '—'
    skill_level_info.short_description = 'Skill Level'

    def contact_info_builder(self, obj):
        join = obj.user.builder_joins.filter(is_approved=True).order_by('-approved_at').first()
        if join and join.whatsapp:
            return format_html('<a href="https://wa.me/{0}" target="_blank">📱 {0}</a>', join.whatsapp)
        return '—'
    contact_info_builder.short_description = 'Contact Number'


@admin.register(ApprovedMentor)
class ApprovedMentorAdmin(UserProfileAdmin):
    list_display = ('account_info', 'role_tag_pill', 'domain_info', 'skill_level_info', 'availability_badge', 'contact_info_mentor')
    list_filter = ('is_accepting_work',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(approved_role__in=['mentor', 'both'])

    def domain_info(self, obj):
        join = obj.user.builder_joins.filter(is_approved=True).order_by('-approved_at').first()
        if join:
            return format_html('<strong>{}</strong>', join.get_primary_domain_display())
        return '—'
    domain_info.short_description = 'Domain'

    def skill_level_info(self, obj):
        join = obj.user.builder_joins.filter(is_approved=True).order_by('-approved_at').first()
        if join:
            return join.get_experience_level_display()
        return '—'
    skill_level_info.short_description = 'Skill Level'

    def contact_info_mentor(self, obj):
        join = obj.user.builder_joins.filter(is_approved=True).order_by('-approved_at').first()
        if join and join.whatsapp:
            return format_html('<a href="https://wa.me/{0}" target="_blank">📱 {0}</a>', join.whatsapp)
        return '—'
    contact_info_mentor.short_description = 'Contact Number'


# ─── ProjectRequest Admin ──────────────────────────────────────────────────────

@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'user_account', 'full_name', 'domain_badge', 'status_badge', 'submitted_at', 'contact_info')
    list_filter = ('domain', 'status', 'submitted_at')
    search_fields = ('full_name', 'email', 'project_title', 'whatsapp')
    readonly_fields = ('submitted_at', 'updated_at')
    list_per_page = 25
    date_hierarchy = 'submitted_at'

    fieldsets = (
        ('👤 Client Information', {
            'fields': ('user', 'full_name', 'whatsapp', 'email', 'college_organization', 'district_location')
        }),
        ('🔧 Project Details', {
            'fields': ('project_title', 'domain', 'domain_other', 'project_description', 'deadline')
        }),
        ('📦 Deliverables', {
            'fields': (
                'deliverable_working_project', 'deliverable_source_code', 'deliverable_documentation',
                'deliverable_report', 'deliverable_ppt', 'deliverable_circuit_diagram',
                'deliverable_mobile_app', 'deliverable_website', 'deliverable_live_demo', 'deliverable_other'
            ),
            'classes': ('collapse',)
        }),
        ('📎 Files & Contact', {
            'fields': ('reference_files', 'contact_method', 'additional_notes')
        }),
        ('⚙️ Status & Meta', {
            'fields': ('status', 'submitted_at', 'updated_at')
        }),
    )

    def domain_badge(self, obj):
        colors = {
            'iot': '#00ff88', 'robotics': '#00ccff', 'drone': '#ffcc00',
            'web': '#ff6644', 'app': '#cc88ff', 'embedded': '#44ffcc',
            'ai': '#ff44aa', 'rover': '#88ff44', 'other': '#aaaaaa'
        }
        color = colors.get(obj.domain, '#aaaaaa')
        return format_html(
            '<span style="background:{};color:#000;padding:2px 8px;border-radius:12px;font-size:11px;font-weight:bold">{}</span>',
            color, obj.get_domain_display()
        )
    domain_badge.short_description = 'Domain'

    def status_badge(self, obj):
        colors = {
            'pending': '#ffcc00', 'reviewing': '#00ccff', 'accepted': '#00ff88',
            'in_progress': '#ff8800', 'completed': '#44ff44', 'rejected': '#ff4444'
        }
        color = colors.get(obj.status, '#aaaaaa')
        return format_html(
            '<span style="background:{};color:#000;padding:2px 8px;border-radius:12px;font-size:11px;font-weight:bold">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def contact_info(self, obj):
        return format_html('<a href="https://wa.me/{0}" target="_blank">📱 {0}</a>', obj.whatsapp)
    contact_info.short_description = 'WhatsApp'

    def user_account(self, obj):
        return mark_safe(_user_tag_cell(obj.user))
    user_account.short_description = '👤 Account'
    user_account.admin_order_field = 'user__username'


# ─── MentorRequest Admin ───────────────────────────────────────────────────────

@admin.register(MentorRequest)
class MentorRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user_account', 'domain_badge', 'mentorship_type', 'current_status', 'preferred_mode', 'submitted_at')
    list_filter = ('domain', 'mentorship_type', 'current_status', 'preferred_mode', 'submitted_at')
    search_fields = ('full_name', 'email', 'whatsapp')
    readonly_fields = ('submitted_at', 'updated_at')
    list_per_page = 25
    date_hierarchy = 'submitted_at'

    fieldsets = (
        ('👤 Personal Info', {
            'fields': ('user', 'full_name', 'whatsapp', 'email', 'college_organization', 'district_location')
        }),
        ('🎓 Mentorship Details', {
            'fields': ('domain', 'domain_other', 'help_required', 'mentorship_type',
                       'mentorship_type_other', 'current_status')
        }),
        ('📅 Scheduling', {
            'fields': ('preferred_mode', 'contact_method', 'availability', 'event_date')
        }),
        ('📎 Files & Notes', {
            'fields': ('reference_files', 'additional_notes')
        }),
        ('⚙️ Meta', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def domain_badge(self, obj):
        colors = {
            'iot': '#00ff88', 'robotics': '#00ccff', 'drone': '#ffcc00',
            'web': '#ff6644', 'app': '#cc88ff', 'embedded': '#44ffcc',
            'ai': '#ff44aa', 'rover': '#88ff44', 'other': '#aaaaaa',
            'pcb': '#ffaa44', 'cad': '#44aaff', 'cybersecurity': '#ff4488'
        }
        color = colors.get(obj.domain, '#aaaaaa')
        return format_html(
            '<span style="background:{};color:#000;padding:2px 8px;border-radius:12px;font-size:11px;font-weight:bold">{}</span>',
            color, obj.get_domain_display()
        )
    domain_badge.short_description = 'Domain'

    def user_account(self, obj):
        return mark_safe(_user_tag_cell(obj.user))
    user_account.short_description = '👤 Account'
    user_account.admin_order_field = 'user__username'


# ─── BuilderMentorJoin Admin ───────────────────────────────────────────────────

def _approve_applications(modeladmin, request, queryset):
    """
    Approve selected Builder/Mentor applications and tag the linked user's profile.
    Merges roles if a user already has a tag (e.g. builder + mentor → both).
    """
    updated = 0
    for application in queryset.filter(is_approved=False):
        application.is_approved = True
        application.approved_at = timezone.now()
        application.save(update_fields=['is_approved', 'approved_at', 'updated_at'])

        if application.user:
            profile, _ = UserProfile.objects.get_or_create(user=application.user)
            requested = application.role          # 'builder', 'mentor', or 'both'
            current   = profile.approved_role     # 'none', 'builder', 'mentor', or 'both'

            # Merge logic
            if current == 'none':
                new_role = requested
            elif current == requested:
                new_role = current
            elif {current, requested} == {'builder', 'mentor'} or 'both' in (current, requested):
                new_role = 'both'
            else:
                new_role = requested

            profile.approved_role = new_role
            profile.save(update_fields=['approved_role'])
            updated += 1

    modeladmin.message_user(
        request,
        f'{updated} application(s) approved and user tags updated successfully.'
    )

_approve_applications.short_description = '✅ Approve selected applications & tag users'


@admin.register(BuilderMentorJoin)
class BuilderMentorJoinAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'user_account', 'role_badge', 'domain_badge', 'experience_level',
        'availability', 'approval_status', 'submitted_at', 'links'
    )
    list_filter = ('role', 'is_approved', 'primary_domain', 'experience_level', 'availability', 'submitted_at')
    search_fields = ('full_name', 'email', 'whatsapp')
    readonly_fields = ('submitted_at', 'updated_at', 'approved_at', 'approval_status')
    list_per_page = 25
    date_hierarchy = 'submitted_at'
    actions = [_approve_applications]

    fieldsets = (
        ('👤 Personal Info', {
            'fields': ('user', 'full_name', 'whatsapp', 'email', 'district_location', 'college_organization')
        }),
        ('🛠 Role & Domain', {
            'fields': ('role', 'primary_domain', 'domain_other', 'experience_level', 'skills_experience')
        }),
        ('🔗 Portfolio Links', {
            'fields': ('github', 'linkedin', 'portfolio_website', 'youtube', 'drive_link', 'other_links'),
            'classes': ('collapse',)
        }),
        ('🎯 Contribution Interests', {
            'fields': (
                'contrib_paid_builds', 'contrib_mentorship', 'contrib_technical_guidance',
                'contrib_research', 'contrib_collaboration', 'contrib_community', 'contrib_workshops'
            ),
            'classes': ('collapse',)
        }),
        ('📅 Availability & Files', {
            'fields': ('availability', 'resume_file')
        }),
        ('💬 Final Notes', {
            'fields': ('why_join', 'additional_notes')
        }),
        ('✅ Approval', {
            'fields': ('is_approved', 'approved_at', 'approval_status'),
            'description': (
                'Use the "Approve selected applications" action from the list view, '
                'or tick "Approved" here and save — the user tag will update automatically on save.'
            ),
        }),
        ('⚙️ Meta', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # ── Also handle direct save (checkbox in detail view) ──────────────────────
    def save_model(self, request, obj, form, change):
        previously_approved = False
        if obj.pk:
            try:
                previously_approved = BuilderMentorJoin.objects.get(pk=obj.pk).is_approved
            except BuilderMentorJoin.DoesNotExist:
                pass

        if obj.is_approved and not previously_approved:
            obj.approved_at = timezone.now()

        super().save_model(request, obj, form, change)

        # Tag the user's profile when approved via the detail form
        if obj.is_approved and not previously_approved and obj.user:
            profile, _ = UserProfile.objects.get_or_create(user=obj.user)
            requested = obj.role
            current   = profile.approved_role

            if current == 'none':
                new_role = requested
            elif current == requested:
                new_role = current
            elif {current, requested} == {'builder', 'mentor'} or 'both' in (current, requested):
                new_role = 'both'
            else:
                new_role = requested

            profile.approved_role = new_role
            profile.save(update_fields=['approved_role'])

    # ── Display helpers ────────────────────────────────────────────────────────

    def approval_status(self, obj):
        if obj.is_approved:
            when = obj.approved_at.strftime('%d %b %Y') if obj.approved_at else ''
            return format_html(
                '<span style="background:#00ff88;color:#000;padding:2px 10px;border-radius:12px;'
                'font-size:11px;font-weight:bold">✅ Approved {}</span>', when
            )
        return format_html(
            '<span style="background:#ffcc00;color:#000;padding:2px 10px;border-radius:12px;'
            'font-size:11px;font-weight:bold">⏳ Pending</span>'
        )
    approval_status.short_description = 'Approval'

    def role_badge(self, obj):
        colors = {'builder': '#00ff88', 'mentor': '#00ccff', 'both': '#ffcc00'}
        color = colors.get(obj.role, '#aaaaaa')
        return format_html(
            '<span style="background:{};color:#000;padding:2px 8px;border-radius:12px;font-size:11px;font-weight:bold">{}</span>',
            color, obj.get_role_display()
        )
    role_badge.short_description = 'Role'

    def domain_badge(self, obj):
        return format_html('<strong>{}</strong>', obj.get_primary_domain_display())
    domain_badge.short_description = 'Domain'

    def links(self, obj):
        html = ''
        if obj.github:
            html += format_html('<a href="{}" target="_blank">GH</a> ', obj.github)
        if obj.linkedin:
            html += format_html('<a href="{}" target="_blank">LI</a> ', obj.linkedin)
        if obj.portfolio_website:
            html += format_html('<a href="{}" target="_blank">🌐</a> ', obj.portfolio_website)
        return format_html(html) if html else '—'
    links.short_description = 'Links'

    def user_account(self, obj):
        return mark_safe(_user_tag_cell(obj.user))
    user_account.short_description = '👤 Account'
    user_account.admin_order_field = 'user__username'
