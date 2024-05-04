# app/services/event_service.py
from ..extensions import db
from ..models import Event, Singer, Person, event_attendance
from datetime import date, datetime
import calendar
from sqlalchemy import func
from sqlalchemy.orm import aliased
from sqlalchemy.orm import joinedload
from collections import defaultdict

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
def get_event_by_id(id):
    # Assuming you have a method to query the database for events by their ID
    event = Event.query.filter_by(id=id).first()
    return event

def get_future_events():
    today = date.today()
    future_events = Event.query.filter(
        (Event.start_date >= today) 
    ).all()
    return future_events

def get_stimmbildungen():
    today = date.today()
    s = Event.query.filter(
        Event.event_type_id == 6, Event.start_date >= today
    ).all()
    return s


def get_stimmbildungen_full():
    today = date.today()
    stimmbildungen = get_stimmbildungen()
    stimmbildungen_with_attendees = {}

    for s in stimmbildungen:
        count_of_attendees, attendees_list = get_attendees(s.id)
        stimmbildungen_with_attendees[s] = (count_of_attendees, attendees_list)

    return stimmbildungen_with_attendees


def get_attendees(main_event_id):
    # Query to get the count of attendees and list of persons attending the event
    query = db.session.query(
        func.count(Singer.id),
        Person
    ).join(
        event_attendance, Singer.id == event_attendance.c.singer_id
    ).join(
        Person, Singer.person_id == Person.id
    ).filter(
        event_attendance.c.event_id == main_event_id
    ).group_by(
        Person.id
    ).all()

    # Extracting count and list of attendees
    count_of_attendees = sum(count for count, _ in query)
    attendees_list = [person for _, person in query]

    return count_of_attendees, attendees_list

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

def add_attendee(event_id, singer_id):
    new_attendance = event_attendance.insert().values(
        event_id=event_id,
        singer_id=singer_id,
        attending=True  # Assuming the user is attending by default
    )
    try:
        db.session.execute(new_attendance)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False
    
def remove_attendee(event_id, singer_id):
    try:
        # Query the event and the singer
        event = Event.query.get(event_id)
        singer = Singer.query.get(singer_id)

        # Check if the event and singer exist
        if not event or not singer:
            return False  # Unable to remove attendee, event or singer not found

        # Remove the singer from the event's attendees list
        if singer in event.attendees:
            event.attendees.remove(singer)
            db.session.commit()
            return True  # Attendee removed successfully
        else:
            return False  # Attendee not found in the event's attendees list

    except Exception as e:
        # Handle any exceptions, such as database errors
        print(f"Error removing attendee: {e}")
        return False  # Unable to remove attendee due to an error