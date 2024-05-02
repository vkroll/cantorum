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