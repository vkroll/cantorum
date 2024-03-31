from app import create_app
from app.services.event_service import create_event, get_future_events

app = create_app('development')

with app.app_context():
    # Now you can safely use your service functions
    new_event = create_event(title="Choir Rehearsal", 
                             description="Regular rehearsal", 
                             start_date="2024-05-01",
                             end_date="2024-05-01",
                             start_time="20:00:00", 
                             end_time="22:00:00", 
                             event_type_id=1,
                             room_id=1)
    print(f"Created event: {new_event.title}")

with app.app_context():
    events = get_future_events()
    for future in events:
        print(f"Event: {future.title}")