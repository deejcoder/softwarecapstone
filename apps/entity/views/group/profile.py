"""
Adds company profiles for users or guest to view
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.defaults import page_not_found

from apps.entity.forms import EditGroupForm
from apps.entity.models import Member, Entity
from apps.entity.models.group import Group
from apps.event.models import Event


class Profile(View):
    """
    Lists all groups
    """

    def get(self, request, group):
        """
        User is viewing a profile
        """

        try:
            group_obj = Group.objects.get(name=group)
        except ObjectDoesNotExist:
            return page_not_found(request, exception=ObjectDoesNotExist(), template_name='404.html')

        entity_obj = Entity.objects.get(group=group_obj)
        events = Event.get_entity_events(entity=entity_obj)

        return render(request, 'group/profile.html', {
            'group': group_obj,
            'events': events,
            'members': Member.get_members(group_obj),
            'is_owner': Member.is_owner(request.user, group_obj),
            'is_editor': Member.is_editor(request.user, group_obj),
        })


class EditProfile(View):
    @method_decorator(login_required)
    def get(self, request, group):
        """
        User is viewing a profile
        """

        try:
            group_obj = Group.objects.get(name=group)
        except ObjectDoesNotExist:
            return page_not_found(request, exception=ObjectDoesNotExist(), template_name='404.html')

        form = EditGroupForm(instance=group_obj)

        return render(request, 'group/edit_profile.html', {
            'group': group_obj,
            'is_owner': Member.is_owner(request.user, group_obj),
            'is_editor': Member.is_editor(request.user, group_obj),
            'form': form,
        })

    @method_decorator(login_required)
    def post(self, request, group):

        # get the group object
        try:
            group = Group.objects.get(name=group)
        except ObjectDoesNotExist:
            return page_not_found(request, exception=ObjectDoesNotExist(), template_name='404.html')

        # is the user an editor (or owner)?
        if not Member.is_editor(request.user, group):
            return page_not_found(request, exception=None, template_name='403.html')

        form = EditGroupForm(request.POST, request.FILES or None, instance=group)

        # save group if valid
        if form.is_valid():
            form.save()
            messages.success(request, 'The group profile has successfully been updated.')
            form = EditGroupForm()

        return HttpResponseRedirect(reverse('entity:group_profile_edit', args=[group.name]))


@login_required
def group_remove(request, group):
    try:
        group_obj = Group.objects.get(name=group)
    except ObjectDoesNotExist:
        return page_not_found(request, exception=ObjectDoesNotExist(), template_name='404.html')

    if not Member.is_owner(request.user, group_obj):
        return page_not_found(request, exception=None, template_name='403.html')

    remove = get_object_or_404(Group, pk=group_obj.id)
    instance = Group.objects.get(id=group_obj.id)
    instance.delete()
    remove.delete()
    return redirect('entity:group_listing')    
