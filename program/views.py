from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from program.models import Program, HistoricalRecords, Researcher, Stakeholder, ProgramBudget
from .filters import ProgramFilter, ProgramFilterDB
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.db.models import Q
from commodity.models import Commodity
from consortium.models import CMI, Consortium
from .forms import ProgramForm, ResearcherForm, StakeholderForm, ProgramBudgetForm
from cmscore.decorators import secretariat_required
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

# Create your views here.
def program(request):
    program = Program.objects.all()
    paginator = Paginator(program, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context ={
        'title' : "program",
        'programs' : program,
        'page_obj': page_obj
    }
    return render(request, 'program.html', context)

def program_detail(request, prog_id):
    program = get_object_or_404(Program, prog_id=prog_id)
    title = program.title
    context = {
        'title' : title,
        'program': program
    }
    return render(request, 'program_detail.html', context)

@secretariat_required
def program_View(request):
    status_filter = request.GET.get('status')
    leader_filter = request.GET.get('leader')
    agency_filter = request.GET.get('agency')
    query = request.GET.get('q')
    programs = Program.objects.all()

    if status_filter:
        programs = programs.filter(status=status_filter)
    if leader_filter:
        programs = programs.filter(program_leader__researcher_id=int(leader_filter))
    if agency_filter:
        programs = programs.filter(impl_agency__name__icontains=agency_filter)
    if query:
        programs = programs.filter(
            Q(title__icontains=query) |
            Q(prog_description__icontains=query)
        )

    paginator = Paginator(programs, 10)  # Show 10 programs per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title' : "Program Management",
        'page_obj': page_obj,
        'status_choices': Program.CHOICE_STATUS,
        'leaders': Researcher.objects.all(),
        'agencies': CMI.objects.all(),
    }

    return render(request, 'view_programs.html', context)

@secretariat_required
@login_required
def add_view(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST, request.FILES)
        if form.is_valid():
            program = form.save(commit=False)
            program.created_by = request.user
            program.save()
            return redirect('program_View')  # redirect to the consortium view page
    else:
        form = ProgramForm()
    return render(request, 'add_program.html', {'form': form})

@secretariat_required
@login_required
def edit_program(request, prog_id):
    program = Program.objects.get(pk=prog_id)
    if request.method == 'POST':
        form = ProgramForm(request.POST, request.FILES, instance=program)
        if form.is_valid():
            form.save()
            return redirect('program_View')  # redirect to program list view
    else:
        form = ProgramForm(instance=program)
    return render(request, 'edit_program.html', {'form': form, 'program': program})

@secretariat_required
def delete_program(request, prog_id):
    program = get_object_or_404(Program, pk=prog_id)
    if request.method == 'POST':
        program.delete()
        return redirect('program_View')  # Redirect to user list after deletion
    return render(request, 'delete_program.html', {'program': program})

def View_researcher(request):
    query = request.GET.get('q')
    agency_filter = request.GET.get('agency')
    researchers = Researcher.objects.all()

    if agency_filter:
        researchers = researchers.filter(cmi__icontains=agency_filter)
    if query:
        researchers = researchers.filter(
            Q(fname__icontains=query) |
            Q(lname__icontains=query) |
            Q(mname__icontains=query) |
            Q(specialization__icontains=query)
        )

    paginator = Paginator(researchers, 10)  # Show 10 researchers per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title' : "Researchers",
        'page_obj': page_obj,
        'leaders': Researcher.objects.all(),
        'agencies': CMI.objects.all(),
    }

    return render(request, 'view_researchers.html', context)

@secretariat_required
@login_required
def add_researcher(request):
    if request.method == 'POST':
        form = ResearcherForm(request.POST, request.FILES)
        if form.is_valid():
            Researcher = form.save(commit=False)
            Researcher.created_by = request.user
            Researcher.save()
            return redirect('View_researcher')
    else:
        form = ResearcherForm()
    return render(request, 'add_researcher.html', {'form': form})

@secretariat_required
@login_required
def edit_researcher(request, researcher_id):
    researcher = Researcher.objects.get(pk=researcher_id)
    if request.method == 'POST':
        form = ResearcherForm(request.POST, request.FILES, instance=researcher)
        if form.is_valid():
            form.save()
            return redirect('View_researcher')
    else:
        form = ResearcherForm(instance=researcher)
    return render(request, 'edit_researcher.html', {'form': form, 'researcher': researcher})

@secretariat_required
def delete_researcher(request, researcher_id):
    researcher = Researcher.objects.get(pk=researcher_id)
    if request.method == 'POST':
        researcher.delete()
        return redirect('View_researcher')  # Redirect to user list after deletion
    return render(request, 'delete_researcher.html', {'researcher': researcher})

def View_stakeholders(request):
    query = request.GET.get('q')
    stakeholders = Stakeholder.objects.all()

    if query:
        stakeholders = stakeholders.filter(
            Q(fname__icontains=query) |
            Q(lname__icontains=query) |
            Q(mname__icontains=query)
        )

    paginator = Paginator(stakeholders, 10)  # Show 10 stakeholders per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title' : "Stakeholders",
        'page_obj': page_obj,
        'consortiums': Consortium.objects.all(),
    }

    return render(request, 'view_stakeholders.html', context)

@secretariat_required
@login_required
def add_stakeholders(request):
    if request.method == 'POST':
        form = StakeholderForm(request.POST, request.FILES)
        if form.is_valid():
            stakeholder = form.save(commit=False)
            stakeholder.created_by = request.user
            stakeholder.save()
            return redirect('View_stakeholders')
    else:
        form = StakeholderForm()
    return render(request, 'add_stakeholders.html', {'form': form})


@secretariat_required
@login_required
def edit_stakeholders(request, stakeholder_id):
    stakeholder = Stakeholder.objects.get(pk=stakeholder_id)
    if request.method == 'POST':
        form = StakeholderForm(request.POST, request.FILES, instance=stakeholder)
        if form.is_valid():
            form.save()
            return redirect('View_stakeholders')
    else:
        form = StakeholderForm(instance=stakeholder)
    return render(request, 'edit_stakeholders.html', {'form': form, 'takeholder': stakeholder})

@secretariat_required
def delete_stakeholders(request, stakeholder_id):
    stakeholder = Stakeholder.objects.get(pk=stakeholder_id)
    if request.method == 'POST':
        stakeholder.delete()
        return redirect('View_stakeholder')  # Redirect to stakeholder list after deletion
    return render(request, 'delete_stakeholders.html', {'stakeholder': stakeholder})


@login_required
@secretariat_required
def view_program_budget(request):
    query = request.GET.get('q')
    program_filter = request.GET.get('program')
    fund_source_filter = request.GET.get('fund_source')
    program_budgets = ProgramBudget.objects.all()

    if program_filter:
        program_budgets = program_budgets.filter(prog_id__prog_id__icontains=program_filter)
    if fund_source_filter:
        program_budgets = program_budgets.filter(fund_source__name__icontains=fund_source_filter)
    if query:
        program_budgets = program_budgets.filter(
            Q(prog_id__prog_name__icontains=query) |
            Q(yr__icontains=query) |
            Q(fund_source__cmi_name__icontains=query)
        )

    paginator = Paginator(program_budgets, 10)  # Show 10 program budgets per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title' : "Program Budgets",
        'page_obj': page_obj,
        'programs': Program.objects.all(),
        'fund_sources': CMI.objects.all(),
    }

    return render(request, 'view_program_budget.html', context)

@login_required
@secretariat_required
def add_program_budget(request):
    if request.method == 'POST':
        form = ProgramBudgetForm(request.POST)
        if form.is_valid():
            program_budget = form.save(commit=False)
            program_budget.created_by = request.user
            program_budget.save()
            return redirect('view_program_budget')
    else:
        form = ProgramBudgetForm()
    return render(request, 'add_program_budget.html', {'form': form})

@login_required
@secretariat_required
def edit_program_budget(request, progbdg_id):
    program_budget = ProgramBudget.objects.get(pk=progbdg_id)
    if request.method == 'POST':
        form = ProgramBudgetForm(request.POST, instance=program_budget)
        if form.is_valid():
            form.save()
            return redirect('view_program_budget')
    else:
        form = ProgramBudgetForm(instance=program_budget)
    return render(request, 'edit_program_budget.html', {'form': form, 'program_budget': program_budget})

@login_required
@secretariat_required
def delete_program_budget(request, progbdg_id):
    program_budget = ProgramBudget.objects.get(pk=progbdg_id)
    if request.method == 'POST':
        program_budget.delete()
        return redirect('view_program_budget')  # Redirect to program budget list after deletion
    return render(request, 'delete_program_budget.html', {'program_budget': program_budget})


def generate_pdf_report(request, program_id):
    # Fetch the program and its related projects
    program = get_object_or_404(Program, pk=program_id)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="program_report_{program_id}.pdf"'

    # Create the PDF object, using the response object as its "file."
    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()

    # Define custom styles for black and white design
    custom_styles = {
        'Title': ParagraphStyle(
            name='Title',
            parent=styles['Title'],
            fontName='Helvetica-Bold',
            fontSize=18,
            textColor=colors.black,
        ),
        'Normal': ParagraphStyle(
            name='Normal',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            textColor=colors.black,
        ),
    }

    # Elements to build the PDF
    elements = []

    # Add program details
    elements.append(Paragraph(f"Program Title: {program.title}", custom_styles['Title']))
    elements.append(Paragraph(f"Status: {program.get_status_display()}", custom_styles['Normal']))
    elements.append(Paragraph(f"Description: {program.prog_description or 'N/A'}", custom_styles['Normal']))
    elements.append(Paragraph(f"Program Lead: {program.program_leader}", custom_styles['Normal']))

    # Add commodities if they exist
    if program.commodity.exists():
        commodities_list = ", ".join(commodity.name for commodity in program.commodity.all())
        elements.append(Paragraph(f"Program Commodity: {commodities_list}", custom_styles['Normal']))
    else:
        elements.append(Paragraph("Program Commodity: N/A", custom_styles['Normal']))

    elements.append(Spacer(1, 12))

    # Add budget details
    budgets = ProgramBudget.objects.filter(prog_id=program)
    ps_total = sum(budget.ps for budget in budgets)
    mooe_total = sum(budget.mooe for budget in budgets)
    eo_total = sum(budget.eo for budget in budgets)
    total_total = sum(budget.get_total for budget in budgets)

    budget_data = [["Year", "Fund Source", "PS (PHP)", "MOOE (PHP)", "EO (PHP)", "Total (PHP)"]]
    for budget in budgets:
        budget_data.append([
            str(budget.yr),  # Ensure year is a string
            budget.fund_source.name if budget.fund_source else 'N/A',  # Ensure fund_source name is a string
            f'{budget.ps:,.2f}',  # Format as string with commas and two decimal places
            f'{budget.mooe:,.2f}',  # Format as string with commas and two decimal places
            f'{budget.eo:,.2f}',  # Format as string with commas and two decimal places
            f'{budget.get_total:,.2f}'  # Format as string with commas and two decimal places
        ])

    # Add total row
    total_row = ["", "Total", f'{ps_total:,.2f}', f'{mooe_total:,.2f}', f'{eo_total:,.2f}', f'{total_total:,.2f}']
    budget_data.append(total_row)

    table = Table(budget_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Adjust to white background
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Build the PDF
    doc.build(elements)
    return response
