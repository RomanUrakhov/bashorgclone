from app import app
from flask import render_template


@app.route('/adding')
def adding():
    return render_template('add.html')
