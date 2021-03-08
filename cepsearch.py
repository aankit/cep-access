from app import app, db
from app.models import School, Plan, PlanText

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'School': School, 'Plan': Plan, 'PlanText': PlanText}
