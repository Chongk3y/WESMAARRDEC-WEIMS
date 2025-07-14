from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Project, Sdg, PriorityArea, ProjectOutput, ProjectImplementingSite
from django.shortcuts import get_object_or_404
from consortium.models import CMI
from django.db.models import Q
from django.http import HttpResponse
from .forms import ProjectForm, SdgForm, PriorityAreaForm, ProjectOutputForm, ProjectImplementingSiteForm
from cmscore.decorators import secretariat_required
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

def project(request):
    title = "Projects"
    on_going_project_list = Project.objects.filter(status=Project.ONGOING).order_by('-modified_at')[:5]
    completed_project_list = Project.objects.filter(status=Project.COMPLETED).order_by('-modified_at')[:5]
    context = {
        'completed': completed_project_list,
        'onggoing': on_going_project_list,
        'title': title,
    }
    return render(request, 'projects.html', context)

def onproject(request):
    title = "On-Going Projects"
    project_list = Project.objects.filter(status=Project.ONGOING)
    paginator = Paginator(project_list, 5)

    page_number = request.GET.get('page')
    paginated_projects = paginator.get_page(page_number)

    context = {
        'projects': paginated_projects,
        'title': title
    }
    print(request.headers)
    return render(request, "ongoingproject.html", context)


def finproject(request):
    title = "Completed Projects"
    project_list = Project.objects.filter(status=Project.COMPLETED)
    paginator = Paginator(project_list, 5)

    page_number = request.GET.get('page')
    paginated_projects = paginator.get_page(page_number)

    context = {
        'projects': paginated_projects,
        'title': title
    }

    print(request.headers)
    return render(request, 'completedProject.html', context)


def project_detail(request, proj_id):
    project = get_object_or_404(Project, proj_id=proj_id)
    title = project.title
    context = {
        'title' : title,
        'project': project
    }
    return render(request, 'project_detail.html', context)

@secretariat_required
def project_view(request):
    types_filter = request.GET.get('types')
    status_filter = request.GET.get('status')
    agency_filter = request.GET.get('agency')
    query = request.GET.get('q')
    projects = Project.objects.all()

    if types_filter:
        projects = projects.filter(proj_type=types_filter)
    if status_filter:
        projects = projects.filter(status=status_filter)
    if agency_filter:
        agency = CMI.objects.get(name=agency_filter)
        projects = projects.filter(impl_agency=agency)
    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(proj_description__icontains=query)
        )

    paginator = Paginator(projects, 10)  # Show 10 programs per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title' : "Program Management",
        'page_obj': page_obj,
        'status_choices': Project.CHOICE_STATUS,
        'types_choices' : Project.CHOICE_TYPE,
        'agencies': CMI.objects.all(),
    }

    return render(request, 'view_project.html', context)

@secretariat_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            return redirect('project_view')  # redirect to the consortium view page
    else:
        form = ProjectForm()
    return render(request, 'add_project.html', {'form': form})

@secretariat_required
def edit_project(request, proj_id):
    project = Project.objects.get(pk=proj_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_view')  # redirect to project list view
    else:
        form =ProjectForm(instance=project)
    return render(request, 'edit_project.html', {'form': form, 'project': project})

@secretariat_required
def delete_project(request, proj_id):
    project = get_object_or_404(Project, pk=proj_id)
    if request.method == 'POST':
        project.delete()
        return redirect('project_view')  # Redirect to user list after deletion
    return render(request, 'delete_project.html', {'project': project})

def view_sdg(request):
    sdg = Sdg.objects.all()

    paginator = Paginator(sdg, 10)  # Show 10 programs per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title' : "SDG Management",
        'page_obj': page_obj,
    }

    return render(request, 'view_sdg.html', context)

def add_sdg(request):
    if request.method == 'POST':
        form = SdgForm(request.POST, request.FILES)
        if form.is_valid():
            sdg = form.save(commit=False)
            sdg.created_by = request.user
            sdg.save()
            return redirect('view_sdg')  # redirect to the consortium view page
    else:
        form = SdgForm()
    return render(request, 'add_sdg.html', {'form': form})

@secretariat_required
def edit_sdg(request, sdg_no):
    sdg = Sdg.objects.get(pk=sdg_no)
    if request.method == 'POST':
        form = SdgForm(request.POST, request.FILES, instance=sdg)
        if form.is_valid():
            form.save()
            return redirect('view_sdg')  # redirect to sdg list view
    else:
        form =SdgForm(instance=sdg)
    return render(request, 'edit_sdg.html', {'form': form, 'sdg': sdg})

@secretariat_required
def delete_sdg(request, sdg_no):
    sdg = get_object_or_404(Sdg, pk=sdg_no)
    if request.method == 'POST':
        sdg.delete()
        return redirect('view_sdg')  # Redirect to user list after deletion
    return render(request, 'delete_sdg.html', {'sdg': sdg})

@secretariat_required
def priority_area_view(request):
    area_filter = request.GET.get('area')
    query = request.GET.get('q')
    priority_areas = PriorityArea.objects.all()

    if area_filter:
        priority_areas = priority_areas.filter(area__icontains=area_filter)
    if query:
        priority_areas = priority_areas.filter(
            Q(area__icontains=query) |
            Q(description__icontains=query)
        )

    paginator = Paginator(priority_areas, 10)  # Show 10 priority areas per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': "Priority Areas",
        'page_obj': page_obj,
    }

    return render(request, 'view_PriorityAreas.html', context)

def add_priority_area(request):
    if request.method == 'POST':
        form = PriorityAreaForm(request.POST)
        if form.is_valid():
            priority_area = form.save(commit=False)
            priority_area.created_by = request.user
            priority_area.save()
            return redirect('view_priority_areas')  # redirect to the priority areas view page
    else:
        form = PriorityAreaForm()
    return render(request, 'add_priority_area.html', {'form': form})

@secretariat_required
def edit_priority_area(request, priority_area_id):
    priority_area = PriorityArea.objects.get(pk=priority_area_id)
    if request.method == 'POST':
        form = PriorityAreaForm(request.POST, instance=priority_area)
        if form.is_valid():
            form.save()
            return redirect('view_priority_areas')  # redirect to priority areas list view
    else:
        form = PriorityAreaForm(instance=priority_area)
    return render(request, 'edit_priority_area.html', {'form': form, 'priority_area': priority_area})

@secretariat_required
def delete_priority_area(request, priority_area_id):
    priority_area = get_object_or_404(PriorityArea, pk=priority_area_id)
    if request.method == 'POST':
        priority_area.delete()
        return redirect('view_priority_areas')  # Redirect to priority areas list after deletion
    return render(request, 'delete_priority_area.html', {'priority_area': priority_area})


@secretariat_required
def view_project_outputs(request):
    query = request.GET.get('q')
    project_filter = request.GET.get('project')
    output_type_filter = request.GET.get('output_type')
    project_outputs = ProjectOutput.objects.all()

    if project_filter:
        project_outputs = project_outputs.filter(proj_id__proj_id__icontains=project_filter)
    if output_type_filter:
        project_outputs = project_outputs.filter(proj_output_type=output_type_filter)
    if query:
        project_outputs = project_outputs.filter(
            Q(proj_output_desc__icontains=query) |
            Q(proj_id__proj_name__icontains=query)
        )

    paginator = Paginator(project_outputs, 10)  # Show 10 project outputs per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title' : "Project Outputs",
        'page_obj': page_obj,
        'projects': Project.objects.all(),
        'output_types': ProjectOutput.OUTPUT_TYPE,
    }

    return render(request, 'view_project_outputs.html', context)

@secretariat_required
def add_project_output(request):
    if request.method == 'POST':
        form = ProjectOutputForm(request.POST)
        if form.is_valid():
            project_output = form.save(commit=False)
            project_output.created_by = request.user
            project_output.save()
            return redirect('view_project_outputs')
    else:
        form = ProjectOutputForm()
    return render(request, 'add_project_output.html', {'form': form})

@secretariat_required
def edit_project_output(request, projout_id):
    project_output = ProjectOutput.objects.get(pk=projout_id)
    if request.method == 'POST':
        form = ProjectOutputForm(request.POST, instance=project_output)
        if form.is_valid():
            form.save()
            return redirect('view_project_outputs')
    else:
        form = ProjectOutputForm(instance=project_output)
    return render(request, 'edit_project_output.html', {'form': form, 'project_output': project_output})

@secretariat_required
def delete_project_output(request, projout_id):
    project_output = ProjectOutput.objects.get(pk=projout_id)
    if request.method == 'POST':
        project_output.delete()
        return redirect('view_project_outputs')  # Redirect to project output list after deletion
    return render(request, 'delete_project_output.html', {'project_output': project_output})

@secretariat_required
def view_project_implementing_sites(request):
    query = request.GET.get('q')
    project_filter = request.GET.get('project')
    site_implementing_sites = ProjectImplementingSite.objects.all()

    if project_filter:
        site_implementing_sites = site_implementing_sites.filter(proj_id__proj_id__icontains=project_filter)
    if query:
        site_implementing_sites = site_implementing_sites.filter(
            Q(barangay__icontains=query) |
            Q(city__icontains=query) |
            Q(province__icontains=query)
        )

    paginator = Paginator(site_implementing_sites, 10)  # Show 10 sites per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title' : "Project Implementing Sites",
        'page_obj': page_obj,
        'projects': Project.objects.all(),
    }

    return render(request, 'view_project_implementing_sites.html', context)

@secretariat_required
def add_project_implementing_site(request):
    if request.method == 'POST':
        form = ProjectImplementingSiteForm(request.POST)
        if form.is_valid():
            site = form.save(commit=False)
            site.created_by = request.user
            site.save()
            return redirect('view_project_implementing_sites')
    else:
        form = ProjectImplementingSiteForm()
    return render(request, 'add_project_implementing_site.html', {'form': form})

@secretariat_required
def edit_project_implementing_site(request, site_id):
    site = ProjectImplementingSite.objects.get(pk=site_id)
    if request.method == 'POST':
        form = ProjectImplementingSiteForm(request.POST, instance=site)
        if form.is_valid():
            form.save()
            return redirect('view_project_implementing_sites')
    else:
        form = ProjectImplementingSiteForm(instance=site)
    return render(request, 'edit_project_implementing_site.html', {'form': form, 'site': site})

@secretariat_required
def delete_project_implementing_site(request, site_id):
    site = ProjectImplementingSite.objects.get(pk=site_id)
    if request.method == 'POST':
        site.delete()
        return redirect('view_project_implementing_sites')  # Redirect to site list after deletion
    return render(request, 'delete_project_implementing_site.html', {'site': site})

def generate_project_report(request, proj_id):
    project = get_object_or_404(Project, pk=proj_id)
    project_outputs = ProjectOutput.objects.filter(proj_id=project)
    implementing_sites = ProjectImplementingSite.objects.filter(proj_id=project)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Project_Report_{proj_id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    section_style = styles['Heading2']
    normal_style = styles['BodyText']

    # Title
    elements.append(Paragraph(f'Project Report: {project.title}', title_style))
    elements.append(Spacer(1, 0.2 * inch))

    # Project Details
    elements.append(Paragraph('Project Details', section_style))
    elements.append(Spacer(1, 0.1 * inch))

    project_details = [
        ['Title', project.title],
        ['Description', project.proj_description or 'N/A'],
        ['Status', project.status],
        ['Type', project.proj_type],
        ['Project Leader', f'{project.proj_leader.fname} {project.proj_leader.lname}'],
        ['Start Date', project.start_date.strftime('%Y-%m-%d') if project.start_date else 'N/A'],
        ['End Date', project.end_date.strftime('%Y-%m-%d') if project.end_date else 'N/A'],
        ['Duration (months)', str(project.duration) if project.duration is not None else 'N/A'],
        ['Approved Budget', f'{project.approved_budget:,.2f}' if project.approved_budget else 'N/A'],
    ]

    # Dynamically adjust column widths
    col_widths = [2 * inch, 6 * inch]  # Adjust width of description column to accommodate longer text

    table = Table(project_details, colWidths=col_widths)
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
    elements.append(Spacer(1, 0.2 * inch))

    # Project Outputs
    elements.append(Paragraph('Project Outputs', section_style))
    elements.append(Spacer(1, 0.1 * inch))

    if project_outputs:
        output_data = [['Output Type', 'Description']]
        for output in project_outputs:
            output_data.append([output.proj_output_type, output.proj_output_desc or 'N/A'])
        output_table = Table(output_data, colWidths=col_widths)
        output_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(output_table)
    else:
        elements.append(Paragraph('No outputs available.', normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    # Implementing Sites
    elements.append(Paragraph('Implementing Sites', section_style))
    elements.append(Spacer(1, 0.1 * inch))

    if implementing_sites:
        site_data = [['Barangay', 'City', 'Province', 'Zipcode', 'Latitude', 'Longitude']]
        for site in implementing_sites:
            site_data.append([
                site.barangay,
                site.city,
                site.province or 'N/A',
                site.zipcode or 'N/A',
                f'{site.geolat:.6f}' if site.geolat is not None else 'N/A',
                f'{site.geolong:.6f}' if site.geolong is not None else 'N/A',
            ])
        site_table = Table(site_data, colWidths=[1.5 * inch] * 6)
        site_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(site_table)
    else:
        elements.append(Paragraph('No implementing sites available.', normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)
    return response