from django.shortcuts import get_object_or_404, render, redirect
from .forms import SignUpForm, EditUserForm
from auth_user.models import User
from django.contrib.auth import authenticate, login as auth_login  # Rename the login function
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator
from django.db.models import Q
from cmscore.decorators import secretariat_required

@secretariat_required
def registration(request):
    title = "Registration"
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accountman')
    else:
        form = SignUpForm()
    return render(request, 'registration.html', {'form': form, 'title': title})

def login(request):
    if request.method == 'POST':
        # Handle login form submission
        # Example: authenticate user
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None and user.is_active:  # Add the is_active check
            auth_login(request, user)  # Use the renamed auth_login function
            if user.secretariat:  # Check the is_secretariat field
                return redirect('CMIadmin')  # Redirect to a different template
            else:
                return redirect('index')  # Redirect to the default template
        else:
            # Handle invalid login credentials or inactive account
            return render(request, 'login.html')
    else:
        # Render login form
        return render(request, 'login.html')
        
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@secretariat_required
def accountman(request):
    query = request.GET.get('q')
    users = User.objects.all()

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    paginator = Paginator(users, 10)  # Show 10 users per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title' : "Accounts Management",
        'page_obj': page_obj,
    }

    return render(request, 'manageprofiles.html', context)

@secretariat_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = EditUserForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('accountman')  # Adjust the redirect URL as needed
    else:
        form = EditUserForm(instance=user)
    context = {
        'form': form,
        'user': user
    }
    return render(request, 'edit_user.html', context)

@secretariat_required
def delete_user(request, user_id):
    accounts = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        accounts.delete()
        return redirect('accountman')  # Redirect to user list after deletion
    return render(request, 'delete_user.html', {'accounts': accounts })

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

@secretariat_required
def reset_password(request, user_id):
  # Get the user whose password needs to be reset
    user = get_object_or_404(User, id=user_id)
    
    # Set the new default password
    default_password = 'Wesmaarrdec123!'  # Replace with your desired default password
    user.set_password(default_password)
    user.save()

    messages.success(request, f"Password for {user.username} has been reset to the default password.")
    return redirect('accountman')