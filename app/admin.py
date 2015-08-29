from django.contrib import admin
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.db import models
from ckeditor.widgets import CKEditorWidget
from django.template.defaultfilters import truncatewords_html
from app.forms import StakeholderForm
from app.models import (
    Assessment, Finding, Reference, Attachment, Stakeholder, Comment)


class AttachmentInline(admin.StackedInline):
    model = Attachment
    classes = ('grp-collapse grp-closed',)
    inline_classes = ('grp-collapse grp-open',)
    extra = 1


class AssessmentInline(admin.TabularInline):
    model = Assessment.stakeholders.through
    extra = 1


class CommentInline(admin.StackedInline):
    model = Comment
    classes = ('grp-collapse grp-closed',)
    inline_classes = ('grp-collapse grp-open',)
    extra = 1


class FindingInline(admin.StackedInline):
    filter_horizontal = ('references', )
    model = Finding
    fieldsets = (
        (None, {
            'fields': (
                ('assessment', )
            ),
        }),
        ('Vulnerability', {
            'classes': ('grp-collapse grp-open',),
            'fields': (
                'title', 'overview',
                ('is_fixed', 'fixed_by', 'fix_date'), 'is_published')
        }),
        ('Risk', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('risk', 'cvssv2', 'impact')
        }),
        ('Infected instances', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('instance', 'url')
        }),
        ('Recommendations', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('references', 'recommendation')
        }),
        ('More options', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('conditions', )
        }),
    )
    max_num = 5
    classes = ('grp-collapse grp-open',)


class ReferenceInline(admin.StackedInline):
    model = Reference


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):

    def make_published(self, request, queryset):
        rows_updated = 0
        for q in queryset:
            q.is_published = True
            q.save()
            rows_updated += 1
        # rows_updated = queryset.update(is_published=True)
        if rows_updated == 1:
            message_bit = "1 finding was"
        else:
            message_bit = "%s findings were" % rows_updated
        self.message_user(
            request, "%s successfully marked as published." % message_bit)

    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},
    }
    # define the raw_id_fields
    raw_id_fields = ['stakeholders', ]
    # define the autocomplete_lookup_fields
    autocomplete_lookup_fields = {
        'm2m': ['stakeholders'],
    }
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'slug'), 'introduction', ('created_at', 'ends_at'),
                ('status', 'is_published', 'publish_date'), 'stakeholders')
        }),
        ('More options', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('summary', 'scope', 'methodology', 'caveats')
        }),
    )

    list_display = (
        'name', 'get_short_introduction', 'get_stakeholders',
        'number_of_findings',
        'status', 'created_at', 'ends_at',  'publish_date', 'is_published'
    )

    list_filter = (
        'status', 'created_at', 'is_published', 'stakeholders__username')
    # inlines = [
    #     FindingInline,
    # ]

    search_fields = ['name', ]

    def get_stakeholders(self, obj):
        holders = []
        for p in obj.stakeholders.all():
            url = reverse('admin:app_stakeholder_change', args=(p.id,))
            holders.append(
                format_html("<a href=%s>%s</a>" % (url, p.username))
            )
        return ", ".join(holders)
    get_stakeholders.short_description = 'Stakeholders'
    get_stakeholders.allow_tags = True

    def get_queryset(self, request):
        qs = super(AssessmentAdmin, self).get_queryset(request)
        qs = qs.annotate(Count('finding'))
        return qs

    def number_of_findings(self, obj):
        return obj.finding__count

    number_of_findings.short_description = "Findings count"
    number_of_findings.admin_order_field = "finding__count"
    make_published.short_description = "Mark selected assessments as published"

    def get_short_introduction(self, obj):
        return truncatewords_html(obj.introduction, 10)

    get_short_introduction.admin_order_field = "introduction"
    get_short_introduction.short_description = "Introduction"

    actions = ['make_published']
    readonly_fields = ['slug']


@admin.register(Finding)
class FindingAdmin(admin.ModelAdmin):

    '''
        Admin View for Finding
    '''
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},
    }
    # define the raw_id_fields
    raw_id_fields = ['fixed_by', ]
    # define the autocomplete_lookup_fields
    autocomplete_lookup_fields = {
        'fk': ['fixed_by'],
    }
    list_display = (
        'title', 'risk', 'assessment', 'created_at',
        'is_fixed', 'is_fix_verified', 'is_published')
    list_filter = ('assessment__name', 'risk', 'is_fixed',
                   'is_fix_verified', 'is_published')
    search_fields = ['title', 'assessment__name']

    readonly_fields = ('fix_date',)

    filter_horizontal = ('references', )

    fieldsets = (
        (None, {
            'fields': (
                ('assessment', )
            ),
        }),
        ('Vulnerability', {
            'classes': ('grp-collapse grp-closed',),
            'fields': (
                'title', 'overview',
                ('is_fixed', 'is_fix_verified', 'fixed_by', 'fix_date'),
                'is_published', 'allow_comments')
        }),
        ('Risk', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('risk', 'cvssv2', 'impact')
        }),
        ('Infected instances and URLs', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('instance', 'url')
        }),
        ("Attachment Inline", {
            "classes": ("placeholder attachment_set-group",),
            "fields": ()
        }),
        ('Recommendations', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('references', 'recommendation')
        }),
        ('Conditions', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('conditions', )
        }),
        ("Comment Inline", {
            "classes": ("placeholder comment_set-group",),
            "fields": ()
        }),
    )
    inlines = [
        AttachmentInline, CommentInline
    ]

    def make_published(self, request, queryset):
        rows_updated = queryset.update(is_published=True)
        if rows_updated == 1:
            message_bit = "1 finding was"
        else:
            message_bit = "%s findings were" % rows_updated
        self.message_user(
            request, "%s successfully marked as published." % message_bit)

    def make_fixed(self, request, queryset):
        rows_updated = 0
        for q in queryset:
            q.is_fixed = True
            q.save()
            rows_updated += 1
        # rows_updated = queryset.update(is_fixed=True)
        if rows_updated == 1:
            message_bit = "1 finding was"
        else:
            message_bit = "%s findings were" % rows_updated
        self.message_user(
            request, "%s successfully marked as fixed." % message_bit)

    make_published.short_description = "Mark selected findings as published"
    make_fixed.short_description = "Mark selected findings as fixed"
    actions = ['make_published', 'make_fixed']


@admin.register(Stakeholder)
class StakeholderAdmin(admin.ModelAdmin):
    form = StakeholderForm
    fieldsets = (
        ('User Profile', {
            'fields': (
                ('first_name', 'last_name',
                 'email', 'username', 'password',
                 ('is_active', 'is_staff',), 'last_login',
                 # 'get_assessments'
                 )
            )
        }),
    )

    inlines = [AssessmentInline, ]

    readonly_fields = ['last_login', ]

    def get_assessments(self, obj):
        assessments = []
        for p in obj.assessment_set.all():
            url = reverse('admin:app_assessment_change', args=(p.id,))
            assessments.append(
                format_html("<a href=%s>%s</a>" % (url, p.name))
            )
        return ", ".join(assessments)
    get_assessments.short_description = 'Assessments'
    get_assessments.allow_tags = True

    list_display = ('username', 'first_name', 'last_name',
                    'email', 'get_assessments', 'last_login',
                    'is_active', 'is_staff')
    list_filter = ('last_login', 'is_active', 'is_staff', 'assessment__name')
    search_fields = ['username', 'email']


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):

    '''
        Admin View for Reference
    '''
    list_display = ('name', 'url')
    list_filter = ('name',)
    search_fields = ['name']


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):

    '''
        Admin View for Attachment
    '''

    def thumbs(self, obj):
        return u'<img src="/media/%s" width=90 height=60 />' % (obj.image)
    thumbs.short_description = 'Thumbnail'
    thumbs.allow_tags = True

    def get_assessments(self, obj):
        url = reverse(
            'admin:app_assessment_change', args=(obj.finding.assessment.id,))
        return format_html(
            "<a href=%s>%s</a>" % (url, obj. finding.assessment.name))
    get_assessments.short_description = 'Assessment'
    get_assessments.allow_tags = True
    get_assessments.admin_order_field = "finding__assessment__name"

    list_display = ('title', 'finding', 'get_assessments', 'thumbs')
    list_filter = ('finding__title', 'finding__assessment__name')
    search_fields = ['title', 'finding__title', 'finding__assessment__name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    '''
        Admin View for Comment
    '''

    def get_assessments(self, obj):
        url = reverse(
            'admin:app_assessment_change', args=(obj.finding.assessment.id,))
        return format_html(
            "<a href=%s>%s</a>" % (url, obj. finding.assessment.name))
    get_assessments.short_description = 'Assessment'
    get_assessments.allow_tags = True
    get_assessments.admin_order_field = "finding__assessment__name"

    def get_short_comment(self, obj):
        return truncatewords_html(obj.comment, 10)
    get_short_comment.admin_order_field = "comment"

    list_display = ('get_short_comment', 'commenter',
                    'finding', 'get_assessments', 'created_at', 'updated_at',
                    'is_replay')
    list_filter = (
        'commenter__username', 'finding__title', 'finding__assessment__name',
        'is_replay')
    search_fields = ['comment', 'parent__comment']
