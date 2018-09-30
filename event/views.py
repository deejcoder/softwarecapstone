from django.shortcuts import render
from lxml import html
import requests

# Create your views here.
def events(request):
    page = requests.get('https://techevents.nz/pnorth')
    tree = html.fromstring(page.content)
    event = tree.xpath('//div[@class="event "]')[0]
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
    return render(request, 'events/rss_feed.html'. {'tree': all_events})
