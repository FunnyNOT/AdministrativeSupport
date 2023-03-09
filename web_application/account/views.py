from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group

from account.utils.login import login_view
from account.utils.registration_checks import register_view
from members.models import Member, AnalyticsMembers
from portals.models import Portal

user_obj = User.objects
member_obj = Member.objects
analytics_members_obj = AnalyticsMembers.objects
portal_obj = Portal.objects
user_groups_obj = Group.objects

def user_authentication_view(request):
    
    if request.method == 'POST':
        context = login_view(request, user_obj, analytics_members_obj, member_obj, portal_obj)

        if context is not None:
            if context['success'] == 1:
                return redirect('Homepage') 
        
        return render(request, 'registration/login.html', context)
    
    # If request.method == 'GET'
    else:

        if request.user.is_authenticated:
            context = {}
            return redirect('Homepage')
        else:
            # Open the login page
            context = {}
            return render(request, 'registration/login.html', context)

def user_registration_view(request):
    
    if request.method == 'GET':
        context = {}
        return render(request, 'registration/register.html', context)


    elif request.method == 'POST':
        
        # Make use of the registration_checks class in order to register a user
        context = register_view(request, user_obj, member_obj, portal_obj, user_groups_obj)

        if context is not None:
            if context['success'] == 1:
                return redirect('Login')

        return render(request, 'registration/register.html', context)

def logout_view(request):

    logout(request)

    if request.user.is_authenticated:
        
            return redirect('Homepage')
    else:
        # Open the login page
        return redirect('Login')

def redirect_to_login(request):

     return redirect('Login')




