from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired

class chatbotform(FlaskForm):
    user_input=StringField(validators=[DataRequired()])
    send=SubmitField('Send')
