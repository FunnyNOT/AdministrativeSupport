from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User

from members.utils.basic_context import get_basic_context
from events.utils import events, events_create, events_edit, events_delete
from events.models import Event
from members.models import Member
from portals.models import Portal


# Create objects
event_obj = Event.objects
member_obj = Member.objects
portal_obj = Portal.objects
user_obj = User.objects

@permission_required("events.can_view_event")
def event_views(request):

     # Get logged user id
    logged_user_id = request.user.id

    # Get context basic
    context_b = get_basic_context(logged_user_id, search_bar=True)


    # GET request method
    if request.method == 'GET':

        events_context = events.evevts_view(request, user_obj, event_obj, member_obj, portal_obj, logged_user_id)
    
        context = {'context_basic': context_b, 'context_events': events_context}
    
        # Render the html template with the context of announcements
        return render(request, 'events.html', context)

    elif request.method == 'POST':

        logged_user_id = request.user.id
        
        # Get the action from the POST request
        events_action = request.POST.get('events_action')

        operation_dict = {
                "create_event": lambda: events_create.event_create(request, event_obj, member_obj, logged_user_id),
                "edit_event": lambda: events_edit.event_edit(request, event_obj, member_obj, logged_user_id),
                "delete_event": lambda: events_delete.event_delete(request, event_obj, member_obj, logged_user_id),
            }

        context_operational = operation_dict.get(events_action)()
        

        return redirect('Events')
        
