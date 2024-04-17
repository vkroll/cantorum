from flask import render_template
from . import main
from app import mail

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
