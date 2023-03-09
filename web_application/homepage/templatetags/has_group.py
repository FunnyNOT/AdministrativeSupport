from django import template

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_list):

    user_groups = user.groups.values_list('name', flat=True)

    if any(x in group_list for x in user_groups):
        return True

    return False