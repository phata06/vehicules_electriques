# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class VotreFormulaire(FlaskForm):
    start = StringField('Point de départ', validators=[DataRequired()])
    end = StringField('Destination', validators=[DataRequired()])
    submit = SubmitField('Envoyer')
