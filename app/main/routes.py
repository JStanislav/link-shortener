from app.main import bp
from app import db
from flask import render_template, jsonify
from app.main.forms import ShortForm
import random
from datetime import datetime

""" 
INSERT INTO `link` (
        name,
        description,
        url,
        date_created,
        last_entry,
        total_entries) 
        VALUES (
            'AAae',
            'some desc',
            'google.com',
            '12/12/2009',
            '12/12/2020',
            4); ''') 
            """

@bp.route('/generate_url/<string:url>')
def generate_url(url):
    """
    this is the endpoint that generate the url, verifying it doesnt exists already and
    generating a new unique random url.
    if the url received exists, it returns the shortened url.
    """
    random_url = ""
    length = 5
    cur = db.connection.cursor()
    cur.execute(''' SELECT * FROM `link` WHERE url=%s ''', (str(url),))
    data = cur.fetchone()
    if data:
        random_url = data[1]
    else:
        #first generates a random url being sure it doesnt exists previously
        while random_url=="":
            for _ in range(length):
                random_url += chr(random.randint(65, 90))
            cur.execute(''' SELECT 1 FROM link WHERE name=%s''', (random_url,))
            if (cur.fetchone()): # si existe la url generada, que vuelva al ciclo
                random_url=""

        #shortened url is created, so its saved
        now = datetime.now()
        formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
        cur.execute(''' INSERT INTO `link`(
            name, 
            description,
            url,
            date_created,
            last_entry,
            total_entries)
            VALUES(
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            ) ''', (random_url, "", url, formatted_time, formatted_time, int(0)))
        db.connection.commit()
        
    cur.close()
    return random_url


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = ShortForm()
    if form.validate_on_submit():
        return render_template("index.html", form=form, generated=generate_url(form.input.data))
    return render_template("index.html", form=form)