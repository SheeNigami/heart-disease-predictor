from application import app

@app.route('/hello')
def hello_world():
    return "<h1>Hello World</h1>"

