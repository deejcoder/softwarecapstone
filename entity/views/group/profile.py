"""
Adds company profiles for users or guest to view
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from entity.forms import EditGroupForm
from entity.models import Member
from entity.models.group import Group


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

        return render(request, 'group/profile.html', {
            'group': group_obj,
            'members': Member.get_members(group_obj),
            'is_owner': Member.is_owner(request.user, group_obj),
            'is_editor': Member.is_editor(request.user, group_obj),
        })

    @method_decorator(login_required)
    def post(self, request, group):

        # get the group object
        try:
            group = Group.objects.get(name=group)
        except ObjectDoesNotExist:
            return HttpResponseNotFound

        # is the user an editor (or owner)?
        if not group.is_editor(request.user):
            return HttpResponseRedirect(request.path)
        
        form = EditGroupForm(instance=group, data=request.POST)

        # save company if valid
        if form.is_valid():
            form.save()
            messages.success(request, 'The company profile has successfully been updated.')
            form = EditGroupForm()

        return render(request, 'group/profile.html', {
            'group': group,
            'is_owner': Member.is_owner(request.user, group),
            'is_editor': Member.is_editor(request.user, group),
            'form': form
        })
