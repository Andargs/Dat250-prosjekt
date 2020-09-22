from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Penal Berit'}
    transaksasjoner = [
        {
            'sender': {'username': 'John'},
            'mottaker': {'username': 'Grøtta grav'}
        },
        {
            'sender': {'username': 'Susan'},
            'mottaker': {'username': 'Gromlegrau'}
        }
    ]
    return render_template('index.html', title='Home', user=user, transaksasjoner=transaksasjoner)