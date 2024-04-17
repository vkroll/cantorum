# app/services/user_service.py

from ..extensions import mail
from flask_mail import Message

def send():
    msg = Message("Hello",
                  sender="cantorum@oelbergchor.de",
                  recipients=["vkroll@allein-zu-haus.de"])
    mail.send(msg)