from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired, Length

class word2input(Form):

    word1 = StringField("Word Source",validators=[DataRequired(), Length(min=1, max = 71)])
    word2 = StringField("Word Target",validators=[DataRequired(), Length(min=1, max=71)])

    submit1 = SubmitField('Run Query')


class word1inputs(Form):

    word1 = StringField("Word Source",validators=[DataRequired(), Length(min=1, max = 71)])

    submit2 = SubmitField('Run Query')

