# app/events/routes.py
from flask import render_template
import calendar
from datetime import datetime
from . import events
from ..services.event_service import create_event, get_future_events, get_events  # Importing your event creation service

@events.route('/create_event', methods=['POST'])
def create_event_route():
    # Here you'll handle the request to create an event
    # and call your event creation service
    return render_template('index.html')


@events.route('/future_events')
def future_events():
    events = get_future_events()
    return render_template('future_events.html', events=events)

@events.route('/calendar')
def show_calendar():
    year = datetime.now().year
    month = datetime.now().month

    # Create an instance of TextCalendar
    cal = calendar.Calendar(firstweekday=0)  # 0 = Monday, 1 = Tuesday, ...
    month_days = cal.monthdayscalendar(year, month) 
    events_by_day = get_events(year, month)

    return render_template('calendar.html', year=year, month=month, month_days=month_days, events_by_day=events_by_day)