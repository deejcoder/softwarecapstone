"""
Allows a group to add members to their group.
"""

from django.http import JsonResponse
from django.views import View

from entity.models import Member
from entity.models.group import Group
from entity.models.company import Company


def get_members(request, entity, entity_name):

    # which entity type is the user requesting members for?
    if entity == "groups":
        entity_obj = Group.objects.get(name=entity_name)
    elif entity == "companies":
        entity_obj = Company.objects.get(name=entity_name)

    # get the members belonging to this entity
    if entity_obj:
        members = Member.get_members(entity_obj)
    else:
        members = ""
    
    # serialize each member's data as JSON
    members_data = []
    for member in members:
        members_data.append({
            'role': member.role,
            'username': member.user.username,
            'full_name': member.user.full_name,
            'avatar': member.user.avatar_url,
            'is_consultant': member.user.is_consultant(),
        })
    data = {
        'members': members_data
    }
    print(data)
    return JsonResponse(data)


    