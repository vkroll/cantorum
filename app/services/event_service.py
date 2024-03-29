# app/services/event_service.py
from ..extensions import db
from ..models import Event

def create_event(title, description, start_time, end_time, room_id, event_type_id):
    # Business logic to create an event
    new_event = Event(title=title, description=description, start_time=start_time,
                      end_time=end_time, room_id=room_id, event_type_id=event_type_id)
    db.session.add(new_event)
    db.session.commit()
    return new_event
