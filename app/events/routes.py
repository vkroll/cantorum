# app/events/routes.py
from flask import render_template

from . import events
from ..services.event_service import create_event, get_future_events  # Importing your event creation service

@events.route('/create_event', methods=['POST'])
def create_event_route():
    # Here you'll handle the request to create an event
    # and call your event creation service
    return render_template('index.html')


@events.route('/future_events')
def future_events():
    events = get_future_events()
    return render_template('future_events.html', events=events)