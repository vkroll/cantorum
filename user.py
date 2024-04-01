from app import create_app
from app.models import Login
#from app.services.event_service import create_event, get_future_events

app = create_app('development')

with app.app_context():
    user = Login(username="vkroll@allein-zu-haus.de", email="vkroll@allein-zu-haus.de")
    user.set_password('goo')
    
    print(user.password_hash)