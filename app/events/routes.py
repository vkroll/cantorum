# app/events/routes.py
from flask import render_template
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta
from . import events
from ..services.event_service import create_event, get_future_events, get_events , get_stimmbildungen_full , get_event_by_id
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

    return render_template("event_detail.html", event=event,sub_events=sub_events )

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