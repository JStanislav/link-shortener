from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ShortForm(FlaskForm):
    input = StringField('Input', validators=[DataRequired()])
    submit = SubmitField('Go')