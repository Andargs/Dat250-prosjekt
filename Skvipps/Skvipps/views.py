from Skvipps import app

@app.route('/')
def index():
    return 'hello world'