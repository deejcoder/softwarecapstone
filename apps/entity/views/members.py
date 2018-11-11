"""
Allows a group to add members to their group.
"""

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils.decorators import method_decorator

from apps.entity.models import Member, MemberRoles
from apps.entity.models.company import Company
from apps.entity.models.group import Group
from apps.user.models import User


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

    members = Member.sort_by_role(members)

    # serialize each member's data as JSON
    members_data = []
    for member in members:
        members_data.append({
            'role': member.role,
            'username': member.user.username,
            'full_name': member.user.get_full_name(),
            'avatar': member.user.avatar_url,
            'is_consultant': member.user.is_consultant()
        })

    data = {
        'members': members_data,
    }

    return JsonResponse(data)


@login_required
def remove_member(request, entity, entity_name, username):
    
    if entity == "groups":
        entity_obj = Group.objects.get(name=entity_name)
    elif entity == "companies":
        entity_obj = Company.objects.get(name=entity_name)

    user = request.user
    data = dict()
    
    if entity_obj:
        if not Member.is_owner(user, entity_obj):
            data['error'] = "403"
        
        else:
            try:
                member = User.objects.get(username=username)
                member = Member.objects.filter(entity=entity_obj).get(user=member)
                member.delete()

                data['error'] = "200"
            except ObjectDoesNotExist:
                data['error'] = "404"

    else:
        data['error'] = "404"
    
    return JsonResponse(data)


@login_required
def add_member(request, entity, entity_name, username):
    """
    Adds a new member to some entity
    """

    if entity == "groups":
        entity_obj = Group.objects.get(name=entity_name)
    elif entity == "companies":
        entity_obj = Company.objects.get(name=entity_name)

    user = request.user
    data = dict()

    if entity_obj:
        if not Member.is_owner(user, entity_obj):
            data['error'] = "403"

        else:
            try:
                new_member = User.objects.get(username=username)
                Member.objects.create(entity=entity_obj, user=new_member, role=MemberRoles.MEMBER)
                data['error'] = "200"
            except ObjectDoesNotExist:
                data['error'] = "404"

    else:
        data['error'] = "404"

    return JsonResponse(data)

