import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.defaults import page_not_found
from geopy.geocoders import Nominatim
from lxml import html

from apps.entity.models import Member
from apps.entity.models.group import Group
from apps.event.models import Event

from .forms import CreateEventForm, EditEventForm
from .filters import EventSearch


def events(request):
    page = requests.get('https://techevents.nz/pnorth')
    tree = html.fromstring(page.content)
    event = tree.xpath('//div[contains(@class,"event")]')[0]
    event_months = event.xpath('//div[@class="date"]/strong/text()')
    event_days = event.xpath('//div[@class="date"]/big/text()')
    event_times = event.xpath('//div[@class="date"]/text()')
    event_times_new = list(filter(None, [x.strip() for x in event_times]))
    event_head = tree.xpath('//div[@class="body"]/h5/text()')
    event_head_new = list(filter(None, [x.strip() for x in event_head]))
    event_desc = tree.xpath('//div[@class="body"]/p/text()')
    event_urls = tree.xpath('//span[@class="info"]//a/@href')
    all_events = []
    for i in range(0, len(event_months)):
        new_event = {}
        new_event['day'] = event_days[i]
        new_event['month'] = event_months[i]
        new_event['time'] = event_times_new[i]
        new_event['heading'] = event_head_new[i]
        new_event['desc'] = event_desc[i]
        new_event['url'] = event_urls[2*i]
        all_events.append(new_event)

    # get all events belonging to techpalmy which have not already happened
    techpalmy_events = Event.get_events()

    event_filter = EventSearch(request.GET, queryset=techpalmy_events)
    results = event_filter.qs

    return render(request, 'events/rss_feed.html', {
        'show_sidepane': Member.is_editor_any(request.user) ^ Member.is_owner_any(request.user),
        'tree': all_events,
        'events': results,
        'filter': event_filter,
    })


class EventDetails(View):
    """
    Details page for a particular event
    """
    def get(self, request, event_title, event_id):

        try:
            event = Event.objects.get(pk=event_id)
        except ObjectDoesNotExist:
            return page_not_found(request, exception=ObjectDoesNotExist(), template_name='404.html')

        entity_obj = event.entity
        location = Nominatim.geocode(self=Nominatim(), query=event.location)

        return render(request, 'events/event_details.html', {
            'event': event,
            'is_owner': Member.is_owner(request.user, entity_obj),
            'is_editor': Member.is_editor(request.user, entity_obj),
            'lat': location.latitude,
            'lon': location.longitude
        })


class CreateEvent(View):
    """
    Allow company/group editors to create events
    using an application
    """
    @method_decorator(login_required)
    def get(self, request):

        form = CreateEventForm(data=request.GET)

        return render(request, 'events/create_event.html', {
            'form': form,
        })

    @method_decorator(login_required)
    def post(self, request):

        form = CreateEventForm(data=request.POST)

        if form.is_valid():

            # assure they own the company/group they are creating an event for
            # this also needs to be adjusted in the form
            entity = form.cleaned_data.get('entity')

            if Member.is_editor(request.user, entity):
                form.save()
                event = form.instance

                # if it's a group, send an email to all group members
                if isinstance(event.entity.group, Group):
                    group = event.entity.group

                    link = settings.SITE_DOMAIN + reverse('event:event_details', args=[event.title, event.id])
                    msg_plain = render_to_string('emails/group_event.txt', {
                        'site': settings.SITE_DOMAIN,
                        'event_title': event.title,
                        'group_name': group.name,
                        'event_link': link
                    })
                    group.email_group("Event: {0}".format(event.title), msg_plain)

                messages.success(request, 'The event has successfully been created.')
                form = CreateEventForm()
            else:
                messages.error(request, 'You must be an editor of the company or group you are creating an event for.')

        return HttpResponseRedirect(reverse('event:events_listing'))

    
class EditEvent(View):
    @method_decorator(login_required)
    def get(self, request, event_title, event_id):

        event = Event.objects.get(pk=event_id)
        form = EditEventForm(instance=event)
        entity_obj = event.entity

        try:
            event_obj = Event.objects.get(pk=event_id)
        except ObjectDoesNotExist:
            return page_not_found(request, exception=ObjectDoesNotExist(), template_name='404.html')

        return render(request, 'events/edit_event.html', {
            'form': form,
            'is_owner': Member.is_owner(request.user, entity_obj),
            'is_editor': Member.is_editor(request.user, entity_obj),
            'event': event_obj,
        })

    @method_decorator(login_required)
    def post(self, request, event_title, event_id):

        try:
            event_obj = Event.objects.get(pk=event_id)
        except ObjectDoesNotExist:
            return page_not_found(request, exception=ObjectDoesNotExist(), template_name='404.html')

        form = EditEventForm(instance=event_obj, data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'The event has successfully been updated.')
            form = EditEventForm()

        return HttpResponseRedirect(request.path)
    
    
@login_required
def remove_event(request, event_title, event_id):
    try:
        event_obj = Event.objects.get(pk=event_id)
    except ObjectDoesNotExist:
        return page_not_found(request, exception=ObjectDoesNotExist(), template_name='404.html')

    entity_obj = Event.objects.get(pk=event_id).entity

    if not Member.is_owner(request.user, entity_obj):
        return page_not_found(request, exception=None, template_name='403.html')

    remove = get_object_or_404(Event, pk=event_obj.id)
    instance = Event.objects.get(id=event_obj.id)
    instance.delete()
    remove.delete()
    return redirect("/")
