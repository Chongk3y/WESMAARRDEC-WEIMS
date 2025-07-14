from django.shortcuts import render, redirect, get_object_or_404
from .forms import TeamForm, TeamMemberFilterForm
from .models import Team
from consortium.models import CMI
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from cmscore.decorators import secretariat_required

@secretariat_required
def add_team(request):
    title = "sign up"
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.created_by = request.user
            form.save()
            return redirect('view_team')  # Redirect to login page after successful registration
    else:
        form = TeamForm()
    return render(request, 'add_team.html', {'form': form, 'title': title})

@secretariat_required
def view_team(request):
    name_query = request.GET.get('q_name')
    team_query = request.GET.get('q_team')
    agency_filter = request.GET.get('agency')
    team_members = Team.objects.all()

    if name_query:
        team_members = team_members.filter(
            Q(fname__icontains=name_query) | 
            Q(lname__icontains=name_query)
            )
    if team_query:
        team_members = team_members.filter(
            teams__icontains=team_query
            )
    if agency_filter:
        agency = CMI.objects.get(name=agency_filter)
        team_members = team_members.filter(
            cmi=agency
            )

    paginator = Paginator(team_members, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title' : "Cluster Management",
        'page_obj': page_obj,
        'status_choices': Team.CHOICE_TEAM,
        'agencies': CMI.objects.all(),
    }
    return render(request, 'view_team.html', context)
   
@secretariat_required  
@login_required
def edit_team(request, member_id):
    team = Team.objects.get(pk=member_id)
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            return redirect('view_team')  # redirect to team list view
    else:
        form = TeamForm(instance=team)
    return render(request, 'edit_team.html', {'form': form, 'team': team})

@secretariat_required
def delete_team(request, member_id):
    team = get_object_or_404(Team, pk=member_id)
    if request.method == 'POST':
        sect.delete()
        return redirect('view_team')  # Redirect to user list after deletion
    return render(request, 'delete_team.html', {'team': team, 'title' : "Delete Member" })