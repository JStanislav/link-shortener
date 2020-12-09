from app.main import bp
from flask import render_template, jsonify
from app.main.forms import ShortForm
import random

@bp.route('/generate_url/<string:url>')
def generate_url(url):
    result = ""
    length = 5
    for _ in range(length):
        result += chr(random.randint(65, 90))
    print(result)
    return result
    #return jsonify({'result': result})


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = ShortForm()
    if form.validate_on_submit():
        return render_template("index.html", form=form, generated=generate_url(form.input.label))
    return render_template("index.html", form=form)