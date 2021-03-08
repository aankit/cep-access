from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

from app import db
from app.models import School, Plan, PlanText
from app.utils import community_board_naming

community_board_numbers = [cd[0] for cd in db.session.query(
    School.community_district).distinct().all() if type(cd[0]) is int]
community_board_names = list(map(community_board_naming, community_board_numbers))
community_board_names.sort()

school_districts = [sd[0] for sd in db.session.query(
    School.school_district).distinct().all() if type(sd[0]) is int]

class SearchForm(FlaskForm):
    search_term = StringField('Search Term', validators=[DataRequired()])
    community_board = SelectField(
        'Community Board', 
        validators=[DataRequired()],
        choices=community_board_names)
    school_districts = SelectField(
        'School District',
        validators=[DataRequired()],
        choices=school_districts)
    submit = SubmitField('Search')