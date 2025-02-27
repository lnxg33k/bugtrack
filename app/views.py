from django.shortcuts import (
    render_to_response, get_object_or_404, HttpResponseRedirect)
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import Assessment, Stakeholder, Finding, Comment
from app.forms import CommentForm
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse


# Create your views here.


def profile(request):
    stakeholder = Stakeholder.objects.get(username=request.user)
    assessments = Assessment.objects.filter(
        stakeholders=stakeholder).order_by('-ends_at')
    # findings = Finding.objects.filter(assessment=assessments)
    paginator_assessments = Paginator(assessments, 10)
    # paginator_findings = Paginator(findings, 1)

    page = request.GET.get('page')
    try:
        assessments_pag = paginator_assessments.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        assessments_pag = paginator_assessments.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        assessments_pag = paginator_assessments.page(
            paginator_assessments.num_pages)
    return render_to_response(
        'profile.html', locals(), context_instance=RequestContext(request))


def view_assessment(request, slug):
    stakeholder = Stakeholder.objects.get(username=request.user)
    assessment = get_object_or_404(
        Assessment, slug=slug, stakeholders=stakeholder)
    findings = Finding.objects.filter(
        assessment=assessment).order_by('-risk')

    paginator_findings = Paginator(findings, 10)
    page = request.GET.get('fpage')
    try:
        findings_pag = paginator_findings.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        findings_pag = paginator_findings.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        findings_pag = paginator_findings.page(
            paginator_findings.num_pages)
    return render_to_response(
        'view_assessment.html', locals(),
        context_instance=RequestContext(request))


def view_finding(request, assessment_slug, slug):
    stakeholder = Stakeholder.objects.get(username=request.user)
    assessment = get_object_or_404(
        Assessment, slug=assessment_slug, stakeholders=stakeholder)
    finding = get_object_or_404(
        Finding, slug=slug, assessment=assessment
    )
    comment_form = CommentForm()
    return render_to_response(
        'view_finding.html', locals(),
        context_instance=RequestContext(request))


def add_comment(request, finding_id, parent_id=None):
    if request.method == "POST":
        stakeholder = Stakeholder.objects.get(username=request.user)
        finding = get_object_or_404(
            Finding, pk=finding_id, assessment__stakeholders=stakeholder)
        comment = Comment(
            finding=finding, commenter=stakeholder,
            parent_id=parent_id)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment was successfully added.")
        else:
            messages.error(request, form.errors.as_text())
    else:
        form = CommentForm()
    return HttpResponseRedirect(reverse(
        "finding_detail", kwargs={
            'assessment_slug': finding.assessment.slug, 'slug': finding.slug
        }
    ))

def add_fix(request, assessment_slug, finding_id):
     if request.method == "POST":
        stakeholder = Stakeholder.objects.get(username=request.user)
        finding = get_object_or_404(Finding, pk=finding_id, assessment__stakeholders=stakeholder)
        finding.is_fixed = 1
        fix_message = request.POST.get('fix_message', '')
        finding.fix_message = fix_message
        finding.fixed_by_id = stakeholder.id

        finding.save()
        messages.success(request, "The finding was marked as fixed now.")

     return HttpResponseRedirect(reverse(
        "finding_detail", kwargs={
            'assessment_slug': finding.assessment.slug, 'slug': finding.slug
        }
    ))
    


def redirect_to404(request):
    return render_to_response(
        'errors/404.html',
        {},
        context_instance=RequestContext(request)
    )


def redirect_to505(request):
    return render_to_response(
        'errors/500.html',
        {},
        context_instance=RequestContext(request)
    )
