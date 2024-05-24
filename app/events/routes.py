# app/events/routes.py
from flask import render_template
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta
from . import events
from ..services.event_service import create_event, get_future_events, get_events , get_stimmbildungen_full , get_event_by_id, add_attendee, remove_attendee, get_voice_counts
from flask_login import login_required, current_user
from ..models import Person, Singer, event_attendance, Voice
from ..extensions import db
from flask import jsonify, request
from ..decorators import role_required


@events.route('/create_event', methods=['POST'])
def create_event_route():
    # Here you'll handle the request to create an event
    # and call your event creation service
    return render_template('index.html')


@events.route('/detail/<int:id>')
@role_required('singer')
def detail(id):
    event = get_event_by_id(id)
    sub_events = event.sub_events
    voice_counts = get_voice_counts(id)
    # Convert to a dictionary for easy access in the template
    voice_counts_dict = {voice: count for voice, count in voice_counts}
    # Ensure all voices are present in the dictionary
    for voice in ["S1", "S2", "A1", "A2", "T1", "T2", "B1", "B2"]:
        if voice not in voice_counts_dict:
            voice_counts_dict[voice] = 0


    return render_template("event_detail.html", event=event,sub_events=sub_events,voice_counts=voice_counts_dict)

@events.route('/edit_attendees/<int:id>')
@role_required('admin', 'choir board', 'conductor')
def edit_attendees(id):
    event = get_event_by_id(id)
    singers = Singer.query.all()
    return render_template('edit_attendees.html', event=event, singers=singers)

@events.route('/future_events')
@login_required
def future_events():
    events = get_future_events()
    return render_template('future_events.html', events=events)

@events.route('/stimmbildung')
@login_required
def stimmbildung():
    stimmbildung = get_stimmbildungen_full()
    p = current_user.person
    print(p)
    singer = p.singer
    print(singer)

    return render_template('stimmbildung.html', stimmbildung=stimmbildung, singer=singer)

@events.route('/actual_calendar')
@login_required
def show_actual_calendar():
    today = datetime.now()
    year = today.year
    month = today.month
    return show_calendar(year,month)

@events.route('/adduser_to_event', methods=['POST'])
@login_required
def adduser_to_event():
    event_id = request.form.get('event_id')
    if event_id is None:
        return jsonify({'success': False, 'error': 'Event ID not provided'}), 400

    # Create a new record in the event_attendance table
    new_attendance = event_attendance.insert().values(
        event_id=event_id,
        singer_id=current_user.person.singer.id,
        attending=True  # Assuming the user is attending by default
    )
    try:
        db.session.execute(new_attendance)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

   
@events.route('/add_attendee', methods=['POST'])
@login_required
@role_required('admin', 'conductor', 'choir board')
def add_attendee_():
    # Get the JSON data from the request
    attendee = request.json
    event_id = attendee.get('event_id')
    singer_id = attendee.get('singer_id')

    add_attendee(event_id, singer_id )
    response = {'message': 'Attendee added successfully', 'event_id': event_id, 'singer_id': singer_id}
    return jsonify(response)


@events.route('/add_me', methods=['POST'])
@login_required
def add_me():
    attendee = request.json
    event_id = attendee.get('event_id')
    singer_id = current_user.person.singer.id

    add_attendee(event_id, singer_id)
    return jsonify({'added': True})

@events.route('remove_me', methods=['POST'])
@login_required
def remove_me():
    attendee = request.json
    event_id = attendee.get('event_id')
    singer_id = current_user.person.singer.id
    
    r = remove_attendee(event_id, singer_id)
    return jsonify({'success': r})

@events.route('/remove_attendee', methods=['POST'])
@login_required
@role_required('admin', 'conductor', 'choir board')
def remove_attendee_():
    data = request.json
    event_id = data.get('event_id')
    singer_id = data.get('singer_id')
    r = remove_attendee(event_id, singer_id)


    return jsonify({'success': r})



@events.route('/calendar/<int:year>/<int:month>')
@login_required
def show_calendar(year, month):
    # Create an instance of TextCalendar
    cal = calendar.Calendar(firstweekday=0)  # 0 = Monday, 1 = Tuesday, ...
    month_days = cal.monthdayscalendar(year, month) 
    m = datetime(year, month, 1)
    n = m + relativedelta(months=1)
    p = m - relativedelta(months=1)

    events_by_day = get_events(year, month)

    return render_template('calendar.html', year=year, month=month, month_days=month_days, events_by_day=events_by_day, next=n, prev=p)