from django.shortcuts import render, redirect
from auditlog.models import LogEntry
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from commodity.models import IecMaterial, Commodity
from project.models import Sdg, PriorityArea, ProjectOutput, ProjectImplementingSite, Project
from program.models import Researcher, Stakeholder, ProgramBudget, Program
from consortium.models import CMI 
from commodity.forms import IecMaterialForm
from program.forms import ResearcherForm, StakeholderForm, ProgramBudgetForm
from project.forms import SdgForm, PriorityAreaForm, ProjectOutputForm, ProjectImplementingSiteForm
from django.http import HttpResponse
from django.template.loader import get_template
from auth_user.models import User
from xhtml2pdf import pisa


# Create your views here.
def about(request):
    return render(request, "sub/about.html")

@login_required
def manage(request):
    users = User.objects.all()
    return render(request, "sub/manage.html", {'users':users})

def home(request):
    commodities = Commodity.objects.all()
    return render(request, "sub/homepage.html", {'commodities':commodities})

def nav(request):
    cmis = CMI.objects.all() 
    return render(request, "consortium/nav.html", {'cmis':cmis})

@login_required
def audit_trail(request):
    log = LogEntry.objects.all()
    return render(request, "sub/audit_trail.html", {'log':log})

@login_required
def summary(request):
    cmis = CMI.objects.all() 
    return render(request, "sub/cmi_summary.html", {'cmis':cmis})


# indexes of sub---------------------------------------------
@login_required
def index_iec(request):  
    iecmaterials = IecMaterial.objects.all()  
    return render(request,"sub/tbl_iec.html",{'iecmaterials':iecmaterials}) 

@login_required
def index_sdg(request):  
    sdgs = Sdg.objects.all()  
    return render(request,"sub/tbl_sdg.html",{'sdgs':sdgs}) 

@login_required
def index_researcher(request):  
    researchers = Researcher.objects.all()  
    return render(request,"sub/tbl_researcher.html",{'researchers':researchers})

@login_required
def index_stakeholder(request):  
    stakeholders = Stakeholder.objects.all()  
    return render(request,"sub/tbl_stakeholder.html",{'stakeholders':stakeholders})

@login_required
def index_progbudg(request):  
    programbudgets = ProgramBudget.objects.all()  
    return render(request,"sub/tbl_programbudget.html",{'programbudgets':programbudgets})

@login_required
def index_prioarea(request):  
    priorityareas = PriorityArea.objects.all()  
    return render(request,"sub/tbl_priorityarea.html",{'priorityareas':priorityareas})

@login_required
def index_projout(request):  
    projectoutputs = ProjectOutput.objects.all()  
    return render(request,"sub/tbl_projectoutput.html",{'projectoutputs':projectoutputs})

@login_required
def index_projimp(request):  
    projectimpsites = ProjectImplementingSite.objects.all()  
    return render(request,"sub/tbl_projectimpsite.html",{'projectimpsites':projectimpsites})


# dashboard---------------------------------------------
@login_required
def dashboard(request):
    no_cmi = CMI.objects.count()
    no_prog = Program.objects.count()
    no_proj = Project.objects.count()
    no_com = Commodity.objects.count()
    cmis = CMI.objects.annotate(number_of_projects=Count('projects'),
                                              number_of_programs=Count('programs'))
    projects = Project.objects.all()
    programs = Program.objects.all()
    context = {
        'no_cmi':no_cmi, 
        'no_prog':no_prog, 
        'no_proj':no_proj, 
        'no_com':no_com,
        'cmis':cmis,
        'projects':projects,
        'programs':programs,
        # 'log':log,
    }
    return render(request, "sub/dashboard.html", context)

# details----------------------------------------------------------------------------------
@login_required
def detail_iecmaterial(request, title):
    iecmaterial = IecMaterial.objects.get(title=title)
    context = {
        'iecmaterial' : iecmaterial,
    }
    return render(request, 'sub/detail_iec.html',context)

@login_required
def detail_sdg(request, sdg_title):
    sdg = Sdg.objects.get(sdg_title=sdg_title)
    context = {
        'sdg' : sdg,
    }
    return render(request, 'sub/detail_sdg.html',context)

@login_required
def detail_researcher(request, researcher_id):
    researcher = Researcher.objects.get(researcher_id=researcher_id)
    context = {
        'researcher' : researcher,
    }
    return render(request, 'sub/detail_researcher.html',context)

@login_required
def detail_stakeholder(request, stakeholder_id):
    stakeholder = Stakeholder.objects.get(stakeholder_id=stakeholder_id)
    context = {
        'stakeholder' : stakeholder,
    }
    return render(request, 'sub/detail_stakeholder.html',context)

@login_required
def detail_prioarea(request, priority_id):
    priorityarea = PriorityArea.objects.get(priority_id=priority_id)
    context = {
        'priorityarea' : priorityarea,
    }
    return render(request, 'sub/detail_priorityarea.html',context)

@login_required
def detail_progbudg(request, progbdg_id):
    programbudget = ProgramBudget.objects.get(progbdg_id=progbdg_id)
    context = {
        'programbudget' : programbudget,
    }
    return render(request, 'sub/detail_programbudget.html',context)

@login_required
def detail_projout(request, projout_id):
    projectoutput = ProjectOutput.objects.get(projout_id=projout_id)
    context = {
        'projectoutput' : projectoutput,
    }
    return render(request, 'sub/detail_projectoutput.html',context)

@login_required
def detail_projimp(request, projimp):
    projectimp = ProjectImplementingSite.objects.get(projimp=projimp)
    context = {
        'projectimp' : projectimp,
    }
    return render(request, 'sub/detail_projectimp.html',context)

# to add---------------------------------------------------------------------------------------
@login_required
def add_iecmaterial(request):  
    if request.method == "POST":  
        form = IecMaterialForm(request.POST, request.FILES)  
        if form.is_valid():  
            try:  
                instance = form.save(commit=False)  
                instance.created_by = request.user
                instance.save()
                return redirect('/IEC_Materials')  
            except:  
                pass
    else:  
        form = IecMaterialForm()  
    return render(request,'sub/add_iec.html',{'form':form}) 

def add_sdg(request):  
    if request.method == "POST":  
        form = SdgForm(request.POST, request.FILES)  
        if form.is_valid():  
            try:  
                instance = form.save(commit=False)  
                instance.created_by = request.user
                instance.save()
                return redirect('/SDGs')  
            except:  
                pass
    else:  
        form = SdgForm()  
    return render(request,'sub/add_sdg.html',{'form':form}) 

@login_required
def add_researcher(request):  
    if request.method == "POST":  
        form = ResearcherForm(request.POST, request.FILES)  
        if form.is_valid():  
            try:  
                instance = form.save(commit=False)  
                instance.created_by = request.user
                instance.save()
                return redirect('/Researchers')  
            except:  
                pass
    else:  
        form = ResearcherForm()  
    return render(request,'sub/add_researcher.html',{'form':form}) 

@login_required
def add_stakeholder(request):  
    if request.method == "POST":  
        form = StakeholderForm(request.POST, request.FILES)  
        if form.is_valid():  
            try:  
                instance = form.save(commit=False)  
                instance.created_by = request.user
                instance.save()
                return redirect('/Stakeholders')  
            except:  
                pass
    else:  
        form = StakeholderForm()  
    return render(request,'sub/add_stakeholder.html',{'form':form}) 

@login_required
def add_progbudg(request):  
    if request.method == "POST":  
        form = ProgramBudgetForm(request.POST, request.FILES)  
        if form.is_valid():  
            try:  
                instance = form.save(commit=False)  
                instance.created_by = request.user
                instance.save()
                return redirect('/ProgramBudgets')  
            except:  
                pass
    else:  
        form = ProgramBudgetForm()  
    return render(request,'sub/add_progbudg.html',{'form':form}) 

@login_required
def add_prioarea(request):  
    if request.method == "POST":  
        form = PriorityAreaForm(request.POST, request.FILES)  
        if form.is_valid():  
            try:  
                instance = form.save(commit=False)  
                instance.created_by = request.user
                instance.save()
                return redirect('/PriorityAreas')  
            except:  
                pass
    else:  
        form = PriorityAreaForm()  
    return render(request,'sub/add_prioarea.html',{'form':form})

@login_required
def add_projout(request):  
    if request.method == "POST":  
        form = ProjectOutputForm(request.POST, request.FILES)  
        if form.is_valid():  
            try:  
                instance = form.save(commit=False)  
                instance.created_by = request.user
                instance.save()
                return redirect('/ProjectOutputs')  
            except:  
                pass
    else:  
        form = ProjectOutputForm()  
    return render(request,'sub/add_projout.html',{'form':form})

@login_required
def add_projimp(request):  
    if request.method == "POST":  
        form = ProjectImplementingSiteForm(request.POST, request.FILES)  
        if form.is_valid():  
            try:  
                instance = form.save(commit=False)  
                instance.created_by = request.user
                instance.save()
                return redirect('/ProjectImplementingSites')  
            except:  
                pass
    else:  
        form = ProjectImplementingSiteForm()  
    return render(request,'sub/add_projimp.html',{'form':form})

# to edit---------------------------------------------------------------------------------------
@login_required
def edit_iecmaterial(request, title):
    iecmaterial = IecMaterial.objects.get(title=title)
    form = IecMaterialForm(instance = iecmaterial)  
    if request.method == 'POST':
        form = IecMaterialForm(request.POST, request.FILES, instance = iecmaterial)
        if form.is_valid():  
            try:  
                instance = form.save(commit=False)  
                instance.modified_by = request.user
                instance.save()
                form.save_m2m()
                return redirect('/IEC_Materials')  
            except:  
                pass
    return render(request, 'sub/edit_iec.html', {'form':form})

@login_required
def edit_sdg(request, sdg_title):
    sdg = Sdg.objects.get(sdg_title=sdg_title)
    form = SdgForm(instance = sdg)  
    if request.method == 'POST':
        form = SdgForm(request.POST, request.FILES, instance = sdg)
        if form.is_valid():  
            try:  
                instance = form.save(commit=False)  
                instance.modified_by = request.user
                instance.save()
                form.save_m2m()
                return redirect('/SDGs')  
            except:  
                pass
    return render(request, 'sub/edit_sdg.html', {'form':form})

@login_required
def edit_researcher(request, researcher_id):
    researcher = Researcher.objects.get(researcher_id=researcher_id)
    form = ResearcherForm(instance = researcher)  
    if request.method == 'POST':
        form = ResearcherForm(request.POST, request.FILES, instance = researcher)
        if form.is_valid():  
            try:  
                instance = form.save(commit=False)  
                instance.modified_by = request.user
                instance.save()
                form.save_m2m()
                return redirect('/Researchers')  
            except:  
                pass
    return render(request, 'sub/edit_researcher.html', {'form':form})

@login_required
def edit_stakeholder(request, stakeholder_id):
    stakeholder = Stakeholder.objects.get(stakeholder_id=stakeholder_id)
    form = StakeholderForm(instance = stakeholder)  
    if request.method == 'POST':
        form = StakeholderForm(request.POST, request.FILES, instance = stakeholder)
        if form.is_valid():  
            try:  
                instance = form.save(commit=False)  
                instance.modified_by = request.user
                instance.save()
                form.save_m2m()
                return redirect('/Stakeholders')  
            except:  
                pass
    return render(request, 'sub/edit_stakeholder.html', {'form':form})

@login_required
def edit_prioarea(request, priority_id):
    priorityarea = PriorityArea.objects.get(priority_id=priority_id)
    form = PriorityAreaForm(instance = priorityarea)  
    if request.method == 'POST':
        form = PriorityAreaForm(request.POST, request.FILES, instance = priorityarea)
        if form.is_valid():  
            try:  
                instance = form.save(commit=False)  
                instance.modified_by = request.user
                instance.save()
                form.save_m2m()
                return redirect('/PriorityAreas')  
            except:  
                pass
    return render(request, 'sub/edit_priorityarea.html', {'form':form})

@login_required
def edit_progbudg(request, progbdg_id):
    programbudget = ProgramBudget.objects.get(progbdg_id=progbdg_id)
    form = ProgramBudgetForm(instance = programbudget)  
    if request.method == 'POST':
        form = ProgramBudgetForm(request.POST, request.FILES, instance = programbudget)
        if form.is_valid():  
            try:  
                instance = form.save(commit=False)  
                instance.modified_by = request.user
                instance.save()
                form.save_m2m()
                return redirect('/ProgramBudgets')  
            except:  
                pass
    return render(request, 'sub/edit_programbudget.html', {'form':form})

@login_required
def edit_projout(request, projout_id):
    projectoutput = ProjectOutput.objects.get(projout_id=projout_id)
    form = ProjectOutputForm(instance = projectoutput)  
    if request.method == 'POST':
        form = ProjectOutputForm(request.POST, request.FILES, instance = projectoutput)
        if form.is_valid():  
            try:  
                instance = form.save(commit=False)  
                instance.modified_by = request.user
                instance.save()
                form.save_m2m()
                return redirect('/ProjectOutputs')  
            except:  
                pass
    return render(request, 'sub/edit_projectoutput.html', {'form':form})

@login_required
def edit_projimp(request, projimp):
    projectimp = ProjectImplementingSite.objects.get(projimp=projimp)
    form = ProjectImplementingSiteForm(instance = projectimp)  
    if request.method == 'POST':
        form = ProjectImplementingSiteForm(request.POST, request.FILES, instance = projectimp)
        if form.is_valid():  
            try:  
                instance = form.save(commit=False)  
                instance.modified_by = request.user
                instance.save()
                form.save_m2m()
                return redirect('/ProjectImplementingSites')  
            except:  
                pass
    return render(request, 'sub/edit_projectimp.html', {'form':form})
# to delete---------------------------------------------------------------------------------------
@login_required
def delete_iecmaterial(request, title):  
    iecmaterial = IecMaterial.objects.get(title=title)  
    iecmaterial.delete()  
    return redirect("/IEC_Materials")  

@login_required
def delete_sdg(request, sdg_title):  
    sdg = Sdg.objects.get(sdg_title=sdg_title)  
    sdg.delete()  
    return redirect("/SDGs")  

@login_required
def delete_researcher(request, researcher_id):  
    researcher = Researcher.objects.get(researcher_id=researcher_id)  
    researcher.delete()  
    return redirect("/Researchers")  

@login_required
def delete_stakeholder(request, stakeholder_id):  
    stakeholder = Stakeholder.objects.get(stakeholder_id=stakeholder_id)  
    stakeholder.delete()  
    return redirect("/Stakeholders")  

@login_required
def delete_prioarea(request, priority_id):  
    priorityarea = PriorityArea.objects.get(priority_id=priority_id)  
    priorityarea.delete()  
    return redirect("/PriorityAreas") 

@login_required
def delete_progbudg(request, progbdg_id):  
    programbudget = ProgramBudget.objects.get(progbdg_id=progbdg_id)  
    programbudget.delete()  
    return redirect("/ProgramBudgets") 

@login_required
def delete_projout(request, projout_id):  
    projectoutput = ProjectOutput.objects.get(projout_id=projout_id)  
    projectoutput.delete()  
    return redirect("/ProjectOutputs")

@login_required
def delete_projimp(request, projimp):  
    projimp = ProjectImplementingSite.objects.get(projimp=projimp)  
    projimp.delete()  
    return redirect("/ProjectImplementingSites")

@login_required
def delete_user(request, username):  
    user = User.objects.get(username=username)  
    user.delete()  
    return redirect("/manage_accounts")

