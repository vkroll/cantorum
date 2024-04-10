# app/services/event_service.py
from ..extensions import db
from ..models import Event
from datetime import date, datetime
import calendar

def create_event(title, description, 
                 start_date, end_date,
                 start_time, end_time, 
                 room_id, event_type_id):
    # Business logic to create an event
    new_event = Event(title=title, 
                      description=description, 
                      start_date=start_date,
                      end_date=end_date,
                      start_time=start_time,
                      end_time=end_time, 
                      room_id=room_id, 
                      event_type_id=event_type_id)
    db.session.add(new_event)
    db.session.commit()
    return new_event

def get_future_events():
    today = date.today()
    future_events = Event.query.filter(
        (Event.start_date >= today) 
    ).all()
    return future_events

def get_events(year, month):
    # Create an instance of TextCalendar
    cal = calendar.Calendar(firstweekday=0)  # 0 = Monday, 1 = Tuesday, ...
    month_days = cal.monthdayscalendar(year, month) 
    
    events = Event.query.filter(
        db.extract('year', Event.start_date) == year,
        db.extract('month', Event.start_date) == month
    ).all()
     # Process events to match with days
    events_by_day = {day: [] for week in month_days for day in week if day != 0}
    for event in events:
        events_by_day[event.start_date.day].append(event)

    return events_by_day