from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class ShortForm(FlaskForm):
    input = StringField('Input', validators=[DataRequired()])
    submit = SubmitField('Go')

class LinksetCreation(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": 'Name'})
    title = StringField('Title', validators=[DataRequired()], render_kw={"placeholder": 'Title'})
    subtitle = TextAreaField('Subtitle', validators=[Length(min=0, max=140)], render_kw={"placeholder": 'Subtitle (máximo 140)'})
    color = StringField('Background color', render_kw={"placeholder": 'Color Hexa'})
    submit = SubmitField('Create!')

