from app import create_app
from app.services.event_service import create_event, get_future_events

app = create_app('development')



with app.app_context():
    events = get_future_events()
    for future in events:
        print(f"Id: {future.id}")
        print(f"Title: {future.title}")
        print(f"Description: {future.description}")
        print(f"Start: {future.start_date}")
        print(f"Startzeit: {future.start_time}")
        print(f"EndZeit: {future.end_time}")
        print(f"Room: {future.room.location.name} {future.room.name}")
        print()
