from django.contrib import admin
from django.urls import path, include

from homepage import views as homepage_views
from account import views as account_views
from portals import views as portal_views
from members import views as members_views
from announcements import views as announcements_views
from events import views as events_views
from classes import views as classes_views

urlpatterns = [
    # System urls
    path('admin/', admin.site.urls, name='Admin'),
    path('login/', account_views.user_authentication_view, name='Login'),
    path('register/', account_views.user_registration_view, name='Register'),
    path('logout/', account_views.logout_view, name='Logout'),
    
    # Homepage urls
    path('homepage/', homepage_views.homepage_view, name='Homepage'),


    # Portal urls
    path('portals/', portal_views.portal_view, name='Portals'),
    path('portals/<str:viewed_portal_id>/', portal_views.portal_profile, name='Portal profile'),


    # Members urls
    path('users/', members_views.members_view, name='Users'),
    path('users/export_csv', members_views.members_view, name='Export CSV'),
    path('profile/<str:viewed_user_id>', members_views.profile_view, name='Profile'),

    # Announcements urls
    path('announcements/', announcements_views.announcement_views, name='Announcements'),

    # Events urls
    path('events/', events_views.event_views, name='Events'),


    # Classes urls
    path('classes/<str:viewed_portal_id>/', classes_views.classes_view, name='Classes'),
    path('classes/<str:viewed_portal_id>/<str:viewed_class_id>/', classes_views.class_profile_view, name='Class Profile'),
    path('classes/timetable/<str:viewed_portal_id>/<str:viewed_class_id>/', classes_views.class_timetable_view, name='Class Timetable'),


    # If link is empty go to Login page and redirect to dashboard if user is logged in
    path('', account_views.redirect_to_login, name='Redirect')

]
