"""
Adds company profiles for users or guest to view
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from entity.forms import EditGroupForm, EditAvatarForm
from entity.models import Member, Entity
from entity.models.group import Group
from event.models import Event


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
            return HttpResponseNotFound()

        entity_obj = Entity.objects.get(group=group_obj)
        events = Event.get_events(entity=entity_obj)

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
            return HttpResponseNotFound()

        form = EditGroupForm(instance=group_obj, data=request.GET)

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
            entity = Entity.objects.get(pk=group.pk)
        except ObjectDoesNotExist:
            return HttpResponseNotFound

        # is the user an editor (or owner)?
        if not Member.is_editor(request.user, group):
            return HttpResponseRedirect(request.path)

        form = EditGroupForm(instance=group, data=request.POST)
        avatar_form = EditAvatarForm(request.POST, request.FILES, instance=entity)

        # save group if valid
        if form.is_valid():
            form.save()
            messages.success(request, 'The group profile has successfully been updated.')
            form = EditGroupForm()

        if avatar_form.is_valid():
            avatar_form.save()
            messages.success(request, "The group's avatar has been updated.")

        return HttpResponseRedirect(reverse('entity:group_profile_edit', args=[group.name]))


@method_decorator(login_required)
def group_remove(request, group):
    try:
        group_obj = Group.objects.get(name=group)
    except ObjectDoesNotExist:
        return HttpResponseNotFound

    if not Member.is_owner(request.user, group_obj):
        return HttpResponseRedirect(request.path)

    remove = get_object_or_404(Group, pk=group_obj.id)
    instance = Group.objects.get(id=group_obj.id)
    instance.delete()
    remove.delete()
    return redirect("/")    
