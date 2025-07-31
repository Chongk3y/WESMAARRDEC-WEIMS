from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .filters import SecretariatFilter
from .models import Secretariat
from .forms import SecretariatForm, SecretariatEditForm
from consortium.models import CMI, Consortium
from django.http import HttpResponse
from django.db import connection
from django.core.paginator import Paginator
from django.db.models import Q
from cmscore.decorators import secretariat_required

@secretariat_required
def secretariatview(request):
    query = request.GET.get('q')
    secretariats = Secretariat.objects.all()

    if query:
        secretariats = secretariats.filter(
            Q(mname__icontains=query) |
            Q(position__icontains=query) |
            Q(fname__icontains=query) |
            Q(lname__icontains=query) |
            Q(email_add__icontains=query)
        )
    secretariats = secretariats.order_by('secretariat_id') 
    paginator = Paginator(secretariats, 10)  # Show 10 users per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title' : "Secretariat Management",
        'page_obj': page_obj,
    }

    return render(request, 'manageSecretariat.html', context)

@secretariat_required
def add_secretariat(request):
    if request.method == 'POST':
        print(request.POST)  # Print the form data
        print(request.FILES)  # Print the uploaded files
        form = SecretariatForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            secretariat = form.save(commit=False)
            secretariat.created_by = request.user
            secretariat.save()
            return redirect('secretariatview')  # Change 'secretariat_list' to your desired redirect URL
        else:
            print("Form is not valid")
            print(form.errors)  # Print the form errors
    else:
        form = SecretariatForm()
    return render(request, 'add_secretariat.html', {'form': form, 'title' : "New Secretariat"})

@secretariat_required
def delete_secretariat(request, secretariat_id):
    sect = get_object_or_404(Secretariat, pk=secretariat_id)
    if request.method == 'POST':
        sect.delete()
        return redirect('secretariatview')  # Redirect to user list after deletion
    return render(request, 'delete_sect.html', {'sect': sect, 'title' : "Delete Secretariat" })

@secretariat_required
def edit_secretariat(request, secretariat_id):
    secretariat = Secretariat.objects.get(pk=secretariat_id)
    if request.method == 'POST':
        form = SecretariatEditForm(request.POST, request.FILES, instance=secretariat)
        if form.is_valid():
            form.save()
            return redirect('secretariatview')  # Redirect to the list of secretariats
    else:
        form = SecretariatEditForm(instance=secretariat)
    return render(request, 'edit_secretariat.html', {'form': form, 'title': "Edit Secretariat"})

def secretariat_hierarchy(request):
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

    return render(request, 'secretariat_hierarchy.html', {'dost_hierarchy': dost_hierarchy, 'consortium_hierarchy': consortium_hierarchy})