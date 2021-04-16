from app import app, db
from app.models import School, Plan, PlanText
import time

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'School': School, 'Plan': Plan, 'PlanText': PlanText}

@app.cli.command()
def scrape_new_plans():
    """Run scheduled job."""
    print('Importing plans...')
    #I'd want to find the last year of plans, determine new school year and check for plans
    #if plans exist: 1) download PDF, 2) turn PDF into text, 3) save text, 4) index text
    #if plans don't exist, log when it was last checked
