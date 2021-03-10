from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

from app import db
from app.models import School, Plan, PlanText
from app.utils import community_board_naming

years = [(y[0], y[0]) for y in db.session.query(Plan.year).distinct().order_by(
    Plan.year.desc()).all()]
years.insert(0, ("None", "Choose from List"))

community_board_numbers = [cd[0] for cd in db.session.query(
    School.community_district).distinct().all() if type(cd[0]) is int]
community_board_names = list(
    map(community_board_naming, community_board_numbers))
community_board_names.sort(key=lambda tup: tup[1])
community_board_names.insert(0, (-1, "Choose from list"))

school_districts = [(sd[0], sd[0]) for sd in db.session.query(
    School.school_district).distinct().all() if type(sd[0]) is int]
school_districts.insert(0, (-1, "Choose from list"))


class SearchForm(FlaskForm):
    search_term = StringField('Search Term')
    year = SelectField(
        'School Year',
        choices=years)
    community_board = SelectField(
        'Community Board',
        choices=community_board_names)
    school_district = SelectField(
        'School District',
        choices=school_districts)
    submit = SubmitField('See Plans')
