from app.main import bp
from app import db
from flask import render_template, jsonify, redirect, url_for
from app.main.forms import ShortForm
import random
from datetime import datetime

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
    return url_for('main.redirecting', url=random_url, _external=True, _scheme="")

@bp.route('/<string:url>')
def redirecting(url):
    """
    where the redirect actually happens
    updates the last entry and total entries values in the db 
    and if it doesn't have the http:// at the begining of the url, it appends it to be redirected correctly
    """
    cur = db.connection.cursor()
    cur.execute(''' SELECT * FROM link WHERE name=%s''', (url,))
    data = cur.fetchone()
    now = datetime.now()
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
    if data:
        cur.execute('''UPDATE link SET last_entry=%s WHERE id=%s''', (now, data[0]))
        cur.execute('''UPDATE link SET total_entries=%s WHERE id=%s''', (data[6]+1, data[0]))
        db.connection.commit()
        cur.close()
        short_url = data[3]
        if short_url.startswith("https://") or short_url.startswith("http://"):
            return redirect(short_url, code=302)
        else:
            return redirect("http://" + short_url, code=302)
    else:
        return "no existe"

@bp.route('/', methods=['GET', 'POST'])
def index():
    """
    main view to generate the short url
    """
    form = ShortForm()
    if form.validate_on_submit():
        return render_template("index.html", form=form, generated=generate_url(form.input.data))
    return render_template("index.html", form=form)