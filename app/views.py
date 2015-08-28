from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import Assessment, Stakeholder, Finding
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
        assessment=assessment).order_by('risk')

    paginator_findings = Paginator(findings, 1)
    page = request.GET.get('page')
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
