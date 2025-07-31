import mysql.connector
from django.shortcuts import render, redirect
from django.conf import settings
from commodity.models import Commodity
from consortium.models import CMI, Consortium
from project.models import Project
from program.models import Program
from cmscore.models import *
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from cmsblg.models import Fact, Post, Category
from cmscore.forms import SearchForm, SlideForm
from django.db.models import Q
from django.core.paginator import Paginator
from secretariat.models import Secretariat
from django.db.models.functions import ExtractYear
from django.db.models import Count


def index_view(request):
    title = "Home"
    commodity = Commodity.objects.all()
    events = Category.objects.get(slug='events')
    news = Category.objects.get(slug='news')
    latest_news_photos = Post.objects.filter(category=news, status=Post.ACTIVE)[:3]
    latest_event_photo = Post.objects.filter(category=events, status=Post.ACTIVE).order_by('-created_at').first()
    carousel_slides = Slide.objects.all().order_by('-created_at')
    context = {
        'title': title,
        'commodity': commodity,
        'latest_news_photos': latest_news_photos,
        'latest_event_photo': latest_event_photo,
        'carousel_slides': carousel_slides,
    }

    return render(request, 'index.html', context)


def cmi(request):
    title = "Consortium Member Institutions"
    cmilist = CMI.objects.filter(status=CMI.ACTIVE)
    context = {
        'title': title,
        'cmilist': cmilist
        }
    return render(request, 'CMI.html',  context)

def community(request):
    title = "Forum"
    category = Category.objects.all()
    events = Category.objects.get(slug='events')
    eventcount = Post.objects.filter(category=events, status=Post.ACTIVE)
    news = Category.objects.get(slug='news')
    newscount = Post.objects.filter(category=news, status=Post.ACTIVE)

    context = {
        'title':title,
        'events_count' : eventcount.count(),
        'news_count' : newscount.count(),
        'news_caption' : news.caption,
        'events_caption' : events.caption,
        'category' : category
    }
    return render(request, "forum.html", context)

def gallery(request):
    title = "Gallery"
    return render(request, "gallery.html", {'title':title})

def CMIadmin(request):
    title = "Dashboard"
    CMIs = CMI.objects.all()
    projects = Project.objects.all()
    commodites = Commodity.objects.all()
    programs = Program.objects.all()
    researchers = Researcher.objects.all()

    cmi_count = CMIs.count()
    project_count = projects.count()
    commodity_count = commodites.count()
    program_count = programs.count()

    context = {
        'researchers': researchers,
        'CMIs' : CMIs,
        'programs' : programs,
        'commodities' : commodites,
        'projects' : projects,
        'title' : title,
        'cmi_count' : cmi_count,
        'project_count' : project_count,
        'commodity_count' : commodity_count,
        'program_count' : program_count
    }
    return render(request, "CMI_admin.html", context)

def FaQ(request):
    title = "Frequently Asked Questions"
    faqs = Fact.objects.all()

    context = {
        'faqs': faqs,
        'title':title
    }
    return render(request, "faqs.html", context)

def consortium(request):
    consortiums = Consortium.objects.all()
    context = {
        'consortiums' : consortiums,
        'title' : "Consortium"
    }
    return render(request, "vision.html", context)

def consortium_data(request):
    consortia = Consortium.objects.all()
    consortia_list = [{
        'name': consortium.consortium_name,
        'lat': consortium.geolat,
        'long': consortium.geolong,
        'logo_url': consortium.consortium_logo.url,
        'description': consortium.consortium_desc,
        'id': consortium.pk,
    } for consortium in consortia]
    return JsonResponse(consortia_list, safe=False)


def cmi_data_view(request):
    cmi_data = CMI.objects.filter(status='Active')
    data = [{
            'id': cmi.agency_id,
            'name': cmi.name,
            'lat': cmi.geolat,
            'long': cmi.geolong,
            'logo_url': cmi.logo.url if cmi.logo else '',  # Handle case where logo is None
    }for cmi in cmi_data]
    return JsonResponse(data, safe=False)

def cmi_detail(request, cmi_id):
    cmi_instance = get_object_or_404(CMI, pk=cmi_id)
    related_commodities = cmi_instance.commodities.all()
    related_projects = cmi_instance.projects.all()
    related_programs = cmi_instance.programs.all()
    context = {
        'cmi_instance': cmi_instance,
        'related_commodities': related_commodities,
        'related_projects' : related_projects,
        'related_programs' : related_programs,
    }
    return render(request, "cmi_detail.html", context)


def search(request):
    form = SearchForm()
    query = request.GET.get('query')

    cmis = []
    events = []
    commodities = []
    programs = []
    projects = []

    if query:
        cmis = CMI.objects.filter(Q(name__icontains=query) | Q(agency_code__icontains=query))
        events = Post.objects.filter(title__icontains=query, status=Post.ACTIVE)
        commodities = Commodity.objects.filter(name__icontains=query)
        programs = Program.objects.filter(title__icontains=query)
        projects = Project.objects.filter(title__icontains=query)

    context = {
        'form': form,
        'query': query,
        'cmis' : cmis,
        'events': events,
        'commodities': commodities,
        'programs': programs,
        'projects': projects,
    }

    return render(request, 'search_results.html', context)

def contactus(request):
    title = "Contact Us"
    return render(request,'contactus.html',{title: 'title'})

def view_slide(request):
    slides = Slide.objects.all()

    paginator = Paginator(slides, 10)  # Show 10 sites per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': "Slides",
        'page_obj': page_obj,
    }
    return render(request, 'view_slide.html', context)

def add_slide(request):
    if request.method == 'POST':
        form = SlideForm(request.POST, request.FILES)
        if form.is_valid():
            slide = form.save(commit=False)
            slide.created_by = request.user.username
            slide.save()
            return redirect('view_slide')
    else:
        form = SlideForm()
    return render(request, 'add_slide.html', {'form': form})

def edit_slide(request, slide_id):
    slide = Slide.objects.get(pk=slide_id)
    if request.method == 'POST':
        form = SlideForm(request.POST, request.FILES, instance=slide)
        if form.is_valid():
            form.save()
            return redirect('view_slide')
    else:
        form = SlideForm(instance=slide)
    return render(request, 'edit_slide.html', {'form': form, 'slide': slide})

def delete_slide(request, slide_id):
    slide = Slide.objects.get(pk=slide_id)
    if request.method == 'POST':
        slide.delete()
        return redirect('view_slide')  # Redirect to slide list after deletion
    return render(request, 'delete_slide.html', {'slide': slide})

def organization(request):
    title = "Organization"
    dost_members = Secretariat.objects.filter(organization='DOST-PCAARD')
    consortium_members = Secretariat.objects.filter(organization='Consortium')

    # Create dictionaries to hold the hierarchies
    dost_hierarchy = {}
    consortium_hierarchy = {}

    # Function to build the hierarchy
    def build_hierarchy(member, hierarchy):
        subordinates = member.subordinates.all()
        hierarchy[member] = {}
        for subordinate in subordinates:
            build_hierarchy(subordinate, hierarchy[member])

    # Get members without managers (top-level members)
    dost_top_level_members = dost_members.filter(manager__isnull=True)
    consortium_top_level_members = consortium_members.filter(manager__isnull=True)

    for member in dost_top_level_members:
        build_hierarchy(member, dost_hierarchy)

    for member in consortium_top_level_members:
        build_hierarchy(member, consortium_hierarchy)

    return render(request, 'organization.html', {'dost_hierarchy': dost_hierarchy, 'consortium_hierarchy': consortium_hierarchy, 'title': title})

def project_status_count(request):
    completed_count = Project.objects.filter(status='Completed').count()
    ongoing_count = Project.objects.filter(status='Ongoing').count()
    data = {
        'completed': completed_count,
        'ongoing': ongoing_count
    }
    return JsonResponse(data)

from django.shortcuts import render
from django.http import JsonResponse
from .models import Program

def program_status_count(request):
    completed_count = Program.objects.filter(status=Program.COMPLETED).count()
    ongoing_count = Program.objects.filter(status=Program.ONGOING).count()
    data = {
        'completed': completed_count,
        'ongoing': ongoing_count
    }
    return JsonResponse(data)


def project_count_per_year_api(request):
    project_counts = Project.objects.annotate(year=ExtractYear('start_date')).values('year').annotate(count=Count('proj_id')).order_by('year')
    data = list(project_counts)
    return JsonResponse(data, safe=False)


def projects_per_year_data(request):
    # Query to get project counts per year
    projects_per_year = Project.objects.annotate(year=ExtractYear('start_date')).values('year').annotate(count=Count('proj_id')).order_by('year')

    # Prepare data as a dictionary
    data = {entry['year']: entry['count'] for entry in projects_per_year}

    return JsonResponse(data)

def cmi_status_count(request):
    # Query to count active and inactive CMIs
    cmi_counts = CMI.objects.values('status').annotate(count=Count('agency_id'))

    # Prepare data as a dictionary
    data = {entry['status']: entry['count'] for entry in cmi_counts}

    return JsonResponse(data)

def activity_management(request):
    return render(request, 'activity_management.html')

import mysql.connector
from django.shortcuts import render, redirect
from django.conf import settings
from commodity.models import Commodity
from consortium.models import CMI, Consortium
from project.models import Project
from program.models import Program
from cmscore.models import *
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from cmsblg.models import Fact, Post, Category
from cmscore.forms import SearchForm, SlideForm
from django.db.models import Q
from django.core.paginator import Paginator
from secretariat.models import Secretariat
from django.db.models.functions import ExtractYear
from django.db.models import Count


def index_view(request):
    title = "Home"
    commodity = Commodity.objects.all()
    events = Category.objects.get(slug='events')
    news = Category.objects.get(slug='news')
    latest_news_photos = Post.objects.filter(category=news, status=Post.ACTIVE)[:3]
    latest_event_photo = Post.objects.filter(category=events, status=Post.ACTIVE).order_by('-created_at').first()
    carousel_slides = Slide.objects.all().order_by('-created_at')
    context = {
        'title': title,
        'commodity': commodity,
        'latest_news_photos': latest_news_photos,
        'latest_event_photo': latest_event_photo,
        'carousel_slides': carousel_slides,
    }

    return render(request, 'index.html', context)


def cmi(request):
    title = "Consortium Member Institutions"
    cmilist = CMI.objects.filter(status=CMI.ACTIVE)
    context = {
        'title': title,
        'cmilist': cmilist
        }
    return render(request, 'CMI.html',  context)

def community(request):
    title = "Forum"
    category = Category.objects.all()
    events = Category.objects.get(slug='events')
    eventcount = Post.objects.filter(category=events, status=Post.ACTIVE)
    news = Category.objects.get(slug='news')
    newscount = Post.objects.filter(category=news, status=Post.ACTIVE)

    context = {
        'title':title,
        'events_count' : eventcount.count(),
        'news_count' : newscount.count(),
        'news_caption' : news.caption,
        'events_caption' : events.caption,
        'category' : category
    }
    return render(request, "forum.html", context)

def gallery(request):
    title = "Gallery"
    return render(request, "gallery.html", {'title':title})

def CMIadmin(request):
    title = "Dashboard"
    CMIs = CMI.objects.all()
    projects = Project.objects.all()
    commodites = Commodity.objects.all()
    programs = Program.objects.all()
    researchers = Researcher.objects.all()

    cmi_count = CMIs.count()
    project_count = projects.count()
    commodity_count = commodites.count()
    program_count = programs.count()

    context = {
        'researchers': researchers,
        'CMIs' : CMIs,
        'programs' : programs,
        'commodities' : commodites,
        'projects' : projects,
        'title' : title,
        'cmi_count' : cmi_count,
        'project_count' : project_count,
        'commodity_count' : commodity_count,
        'program_count' : program_count
    }
    return render(request, "CMI_admin.html", context)

def FaQ(request):
    title = "Frequently Asked Questions"
    faqs = Fact.objects.all()

    context = {
        'faqs': faqs,
        'title':title
    }
    return render(request, "faqs.html", context)

def consortium(request):
    consortiums = Consortium.objects.all()
    context = {
        'consortiums' : consortiums,
        'title' : "Consortium"
    }
    return render(request, "vision.html", context)

def consortium_data(request):
    consortia = Consortium.objects.all()
    consortia_list = [{
        'name': consortium.consortium_name,
        'lat': consortium.geolat,
        'long': consortium.geolong,
        'logo_url': consortium.consortium_logo.url,
        'description': consortium.consortium_desc,
        'id': consortium.pk,
    } for consortium in consortia]
    return JsonResponse(consortia_list, safe=False)


def cmi_data_view(request):
    cmi_data = CMI.objects.filter(status='Active')
    data = [{
            'id': cmi.agency_id,
            'name': cmi.name,
            'lat': cmi.geolat,
            'long': cmi.geolong,
            'logo_url': cmi.logo.url if cmi.logo else '',  # Handle case where logo is None
    }for cmi in cmi_data]
    return JsonResponse(data, safe=False)

def cmi_detail(request, cmi_id):
    cmi_instance = get_object_or_404(CMI, pk=cmi_id)
    related_commodities = cmi_instance.commodities.all()
    related_projects = cmi_instance.projects.all()
    related_programs = cmi_instance.programs.all()
    context = {
        'cmi_instance': cmi_instance,
        'related_commodities': related_commodities,
        'related_projects' : related_projects,
        'related_programs' : related_programs,
    }
    return render(request, "cmi_detail.html", context)


def search(request):
    form = SearchForm()
    query = request.GET.get('query')

    cmis = []
    events = []
    commodities = []
    programs = []
    projects = []

    if query:
        cmis = CMI.objects.filter(Q(name__icontains=query) | Q(agency_code__icontains=query))
        events = Post.objects.filter(title__icontains=query, status=Post.ACTIVE)
        commodities = Commodity.objects.filter(name__icontains=query)
        programs = Program.objects.filter(title__icontains=query)
        projects = Project.objects.filter(title__icontains=query)

    context = {
        'form': form,
        'query': query,
        'cmis' : cmis,
        'events': events,
        'commodities': commodities,
        'programs': programs,
        'projects': projects,
    }

    return render(request, 'search_results.html', context)

def contactus(request):
    title = "Contact Us"
    return render(request,'contactus.html',{title: 'title'})

def view_slide(request):
    slides = Slide.objects.all()

    paginator = Paginator(slides, 10)  # Show 10 sites per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': "Slides",
        'page_obj': page_obj,
    }
    return render(request, 'view_slide.html', context)

def add_slide(request):
    if request.method == 'POST':
        form = SlideForm(request.POST, request.FILES)
        if form.is_valid():
            slide = form.save(commit=False)
            slide.created_by = request.user.username
            slide.save()
            return redirect('view_slide')
    else:
        form = SlideForm()
    return render(request, 'add_slide.html', {'form': form})

def edit_slide(request, slide_id):
    slide = Slide.objects.get(pk=slide_id)
    if request.method == 'POST':
        form = SlideForm(request.POST, request.FILES, instance=slide)
        if form.is_valid():
            form.save()
            return redirect('view_slide')
    else:
        form = SlideForm(instance=slide)
    return render(request, 'edit_slide.html', {'form': form, 'slide': slide})

def delete_slide(request, slide_id):
    slide = Slide.objects.get(pk=slide_id)
    if request.method == 'POST':
        slide.delete()
        return redirect('view_slide')  # Redirect to slide list after deletion
    return render(request, 'delete_slide.html', {'slide': slide})

def organization(request):
    title = "Organization"
    dost_members = Secretariat.objects.filter(organization='DOST-PCAARD')
    consortium_members = Secretariat.objects.filter(organization='Consortium')

    # Create dictionaries to hold the hierarchies
    dost_hierarchy = {}
    consortium_hierarchy = {}

    # Function to build the hierarchy
    def build_hierarchy(member, hierarchy):
        subordinates = member.subordinates.all()
        hierarchy[member] = {}
        for subordinate in subordinates:
            build_hierarchy(subordinate, hierarchy[member])

    # Get members without managers (top-level members)
    dost_top_level_members = dost_members.filter(manager__isnull=True)
    consortium_top_level_members = consortium_members.filter(manager__isnull=True)

    for member in dost_top_level_members:
        build_hierarchy(member, dost_hierarchy)

    for member in consortium_top_level_members:
        build_hierarchy(member, consortium_hierarchy)

    return render(request, 'organization.html', {'dost_hierarchy': dost_hierarchy, 'consortium_hierarchy': consortium_hierarchy, 'title': title})

def project_status_count(request):
    completed_count = Project.objects.filter(status='Completed').count()
    ongoing_count = Project.objects.filter(status='Ongoing').count()
    data = {
        'completed': completed_count,
        'ongoing': ongoing_count
    }
    return JsonResponse(data)

from django.shortcuts import render
from django.http import JsonResponse
from .models import Program

def program_status_count(request):
    completed_count = Program.objects.filter(status=Program.COMPLETED).count()
    ongoing_count = Program.objects.filter(status=Program.ONGOING).count()
    data = {
        'completed': completed_count,
        'ongoing': ongoing_count
    }
    return JsonResponse(data)


def project_count_per_year_api(request):
    project_counts = Project.objects.annotate(year=ExtractYear('start_date')).values('year').annotate(count=Count('proj_id')).order_by('year')
    data = list(project_counts)
    return JsonResponse(data, safe=False)


def projects_per_year_data(request):
    # Query to get project counts per year
    projects_per_year = Project.objects.annotate(year=ExtractYear('start_date')).values('year').annotate(count=Count('proj_id')).order_by('year')

    # Prepare data as a dictionary
    data = {entry['year']: entry['count'] for entry in projects_per_year}

    return JsonResponse(data)

def cmi_status_count(request):
    # Query to count active and inactive CMIs
    cmi_counts = CMI.objects.values('status').annotate(count=Count('agency_id'))

    # Prepare data as a dictionary
    data = {entry['status']: entry['count'] for entry in cmi_counts}

    return JsonResponse(data)
