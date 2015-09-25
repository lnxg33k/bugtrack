from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.template.defaultfilters import truncatechars


class Stakeholder(User):

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "username__icontains",)

    def __init__(self, *args, **kwargs):
        self._meta.get_field_by_name('email')[0]._unique = True
        super(Stakeholder, self).__init__(*args, **kwargs)
        self._meta.get_field('email').blank = False

    # def save(self, *args, **kwargs):
    #     if self.pk is not None:
    #         orig = Stakeholder.objects.get(pk=self.pk)
    #         if orig.password != self.password:
    #             # do anything you need before saving
    #             self.set_password(self.password)
    #     super(Stakeholder, self).save(*args, **kwargs)
    #     # do anything you need after saving

    class Meta:
        proxy = True


class Assessment(models.Model):
    status_choices = (
        ("progress", "In Progress"),
        ("retesting", "Retesting"),
        ("reporting", "Reporting"),
        ("postponed", "Postponed"),
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
    )
    name = models.CharField("Assessment", max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)
    stakeholders = models.ManyToManyField(Stakeholder, blank=True)
    introduction = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    scope = models.TextField(null=True, blank=True)
    methodology = models.TextField(null=True, blank=True)
    caveats = models.TextField(null=True, blank=True)
    publish_date = models.DateField("Publish Date", null=True, blank=True)
    created_at = models.DateField("Satrt Date", null=True, blank=True)
    ends_at = models.DateField("End Date", null=True, blank=True)
    status = models.CharField(
        "Status", blank=True, max_length=50, choices=status_choices)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Assessment"
        verbose_name_plural = "Assessments"

    def __str__(self):
        return "%s" % self.name

    @models.permalink
    def get_absolute_url(self):
        return ('assessment_detail', (),
                {'slug': self.slug}
                )

    def save(self, *args, **kwargs):
        if self.pk:
            orig = Assessment.objects.get(pk=self.pk)
        if not self.slug or (orig and orig.slug != slugify(self.name)):
            self.slug = slugify(self.name)
        super(Assessment, self).save(*args, **kwargs)


class Reference(models.Model):
    name = models.CharField("Name", max_length=50)
    url = models.CharField("URL", max_length=250)

    class Meta:
        verbose_name = "Reference"
        verbose_name_plural = "References"

    def __str__(self):
        return "%s" % self.name


class Attachment(models.Model):
    finding = models.ForeignKey('Finding', null=True, blank=True)
    image = models.ImageField(
        upload_to="images/%Y/%m/%d", null=True, blank=True)
    title = models.CharField("Title", null=True, blank=True, max_length=50)

    class Meta:
        verbose_name = "POC"
        verbose_name_plural = "Proof Of Concept (Images)"

    def __str__(self):
        return "%s" % self.title


class Comment(models.Model):
    finding = models.ForeignKey('Finding')
    commenter = models.ForeignKey('Stakeholder')
    comment = models.TextField()
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='replies')
    is_replay = models.BooleanField(editable=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.parent:
            self.is_replay = True
        else:
            self.is_replay = False
        super(Comment, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return "%s" % truncatechars(self.comment, 100)


class Finding(models.Model):
    risk_choices = (
        ("0", "Informational"),
        ("1", "Low"),
        ("2", "Medium"),
        ("3", "High"),
        ("4", "Critical"),
    )
    assessment = models.ForeignKey('Assessment')
    # attachment = models.ForeignKey('Attachment', null=True, blank=True)
    references = models.ManyToManyField(Reference, blank=True)
    title = models.CharField("Finding", max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)
    risk = models.CharField("Risk", max_length=50, choices=risk_choices)
    is_fixed = models.BooleanField(default=False)
    is_fix_verified = models.BooleanField(default=False)
    fix_date = models.DateTimeField(blank=True, null=True)
    fixed_by = models.ForeignKey(Stakeholder, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    allow_comments = models.BooleanField('Allow comments', default=True)
    cvssv2 = models.CharField("CVSSv2", max_length=50, null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    conditions = models.TextField(null=True, blank=True)
    impact = models.TextField(null=True, blank=True)
    recommendation = models.TextField(null=True, blank=True)
    instance = models.TextField("Instances", null=True, blank=True)
    url = models.TextField("Demonstration URLs", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @models.permalink
    def get_absolute_url(self):
        return ('finding_detail', (),
                {'slug': self.slug}
                )

    def save(self, *args, **kwargs):
        # do anything you need before saving
        if self.is_fixed:
            if self.pk is not None:  # exists field
                orig = Finding.objects.get(pk=self.pk)
                if orig.is_fixed == self.is_fixed:  # not changed
                    self.fix_date = orig.fix_date
                else:
                    self.fix_date = timezone.now()
            else:
                self.fix_date = timezone.now()
        else:
            self.fix_date = None

        if self.pk:
            orig = Finding.objects.get(pk=self.pk)
        if not self.slug or (orig and orig.slug != slugify(self.title)):
            self.slug = slugify(self.title)

        super(Finding, self).save(*args, **kwargs)
        # do anything you need after saving

    class Meta:
        verbose_name = "Finding"
        verbose_name_plural = "Findings"

    def __str__(self):
        return "%s" % self.title
