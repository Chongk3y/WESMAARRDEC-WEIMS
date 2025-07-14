from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from commodity.models import Commodity
from program.models import Program
from project.models import Project
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from cmscore.decorators import secretariat_required
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

@secretariat_required
def CMI_View(request):
    query = request.GET.get('q')
    CMIs = CMI.objects.all()

    if query:
        CMIs = CMIs.filter(
            Q(agency_id__icontains=query) |
            Q(agency_code__icontains=query) |
            Q(name__icontains=query) |
            Q(address__icontains=query) |
            Q(contact_no__icontains=query) |
            Q(email__icontains=query)
        )

    paginator = Paginator(CMIs, 10)  # Show 10 users per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title' : "CMI Management",
        'page_obj': page_obj,
    }

    return render(request, 'CMI_VIEW.html', context)

@secretariat_required
@login_required
def add_CMI(request):
    if request.method == 'POST':
        form = CMIForm(request.POST, request.FILES)
        if form.is_valid():
            cmi = form.save(commit=False)
            cmi.created_by = request.user
            cmi.save()
            return redirect('CMI_View')
    else:
        form = CMIForm()
    return render(request, 'add_CMI.html', {'form': form})

@secretariat_required
@login_required
def edit_Consortium(request, consortium_id):
    consortium = Consortium.objects.first()
    if request.method == 'POST':
        form = ConsortiumForm(request.POST, request.FILES, instance=consortium)
        if form.is_valid():
            form.save()
            return redirect('CMI_View')  # redirect to a list view
    else:
        form = ConsortiumForm(instance=consortium)
    return render(request, 'edit_Consortium.html', {'form': form})

@secretariat_required
@login_required
def edit_CMI(request, agency_id):
    cmi = get_object_or_404(CMI, agency_id=agency_id)
    if request.method == 'POST':
        form = CMIForm(request.POST, request.FILES, instance=cmi)
        if form.is_valid():
            form.save()
            return redirect('CMI_View')  # redirect to a list view
    else:
        form = CMIForm(instance=cmi)
    return render(request, 'edit_CMI.html', {'form': form})

@secretariat_required
def delete_CMI(request, agency_id):
    cmi = get_object_or_404(CMI, agency_id=agency_id)
    if request.method == 'POST':
        cmi.delete()
        return redirect('CMI_View')  # Redirect to user list after deletion
    return render(request, 'delete_CMI.html', {'cmi': cmi})

def generate_cmi_report(request, agency_id):
    cmi = get_object_or_404(CMI, agency_id=agency_id)
    projects = Project.objects.filter(impl_agency=cmi)
    programs = Program.objects.filter(impl_agency=cmi)
    commodities = Commodity.objects.filter(cmi_name=cmi)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="CMI_Report_{agency_id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(A4))
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    section_style = styles['Heading2']
    table_style = ParagraphStyle(
        name='Table',
        parent=styles['BodyText'],
        fontSize=10,
        leading=12
    )

    # Title
    elements.append(Paragraph(f'CMI Report: {cmi.name}', title_style))
    elements.append(Spacer(1, 0.2 * inch))

    # Consolidated Table
    elements.append(Paragraph('Projects and Programs', section_style))
    elements.append(Spacer(1, 0.1 * inch))

    table_data = [['Name', 'Status', 'Type', 'Leader', 'Start Date', 'End Date', 'Commodity', 'Budget']]

    for project in projects:
        commodities_list = ', '.join([commodity.name for commodity in Commodity.objects.filter(proj_com=project)]) or 'N/A'
        table_data.append([
            project.title,
            project.status,
            'Project',
            f'{project.proj_leader.fname} {project.proj_leader.lname}',
            project.start_date.strftime('%Y-%m-%d') if project.start_date else 'N/A',
            project.end_date.strftime('%Y-%m-%d') if project.end_date else 'N/A',
            commodities_list,
            f'{project.approved_budget:.2f}' if project.approved_budget else 'N/A'
        ])

    for program in programs:
        commodities_list = ', '.join([commodity.name for commodity in Commodity.objects.filter(prog_com=program)]) or 'N/A'
        table_data.append([
           program.title,
            program.status,
            'Program',
            f'{program.program_leader.fname} {program.program_leader.lname}',
            program.start_date.strftime('%Y-%m-%d') if program.start_date else 'N/A',
            'N/A',  # End Date is not applicable for programs
            commodities_list,
            'N/A'  # Budget is not applicable for programs
        ])

    col_widths = [1.5 * inch, 1 * inch, 1 * inch, 2 * inch, 1 * inch, 1 * inch, 1.5 * inch, 1 * inch]
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    doc.build(elements)
    return response

