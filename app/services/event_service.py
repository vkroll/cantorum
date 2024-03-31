# app/services/event_service.py
from ..extensions import db
from ..models import Event
from datetime import date

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