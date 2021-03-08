import requests
import io
import pandas as pd

# response = requests.get("https://data.cityofnewyork.us/api/views/3bkj-34v2/files/56813139-9b9d-44fb-b81d-068553b7a9b7?download=true&filename=LCGMS_SchoolData(additional geocoded fields added).csv")
# lcgms = pd.read_csv(io.StringIO(response.text))
lcgms = pd.read_csv(
    '/Users/Aankit/Documents/CEP-search/app/static/LCGMS_SchoolData_additional_geocoded_fields_added_.csv')


def community_board_naming(num):
    if type(num) is int:
        if num > 500:
            return "Staten Island CB {}".format(num-500)
        elif num > 400:
            return "Queens CB {}".format(num-400)
        elif num > 300:
            return "Brooklyn CB {}".format(num-300)
        elif num > 200:
            return "Bronx CB {}".format(num-200)
        elif num > 100:
            return "Manhattan CB {}".format(num-100)
        else:
            return "Missing"
    return "Not Found"

def add_school(db, School, bn):
    school = lcgms.loc[lcgms['Location Code'] == bn]
    if not school.empty:
        dbn = school['ATS System Code'].values[0]
        school_name = school['Location Name'].values[0]
        school_district = school['Administrative District Code'].values[0]
        council_district = school['Council District'].values[0]
    else:
        dbn = None
        school_name = None
        school_district = None
        council_district = None
    e = db.session.query(School).filter_by(bn=bn).first()
    if not e:
        s = School(
            bn=bn,
            dbn=dbn,
            school_name=school_name,
            school_district=school_district,
            council_district=council_district
        )
        db.session.add(s)
        db.session.commit()
        return(s.id)
    db.session.commit()
    return e.id


def add_plan(db, Plan, year, school_id):
    e = db.session.query(Plan).filter_by(year=year, school_id=school_id).first()
    if not e:
        p = Plan(
            year=year,
            school_id=school_id
        )
        db.session.add(p)
        db.session.commit()
        return p.id
    return e.id


def does_page_exist(db, PlanText, plan_id, page_number):
    e = db.session.query(PlanText).filter_by(plan_id=plan_id, page_number=page_number).first()
    if e:
        return True

def add_page(db, PlanText, plan_id, page_number, text):
    e = db.session.query(PlanText).filter_by(plan_id=plan_id, page_number=page_number).first()
    if not e:
        t = PlanText(
            plan_id=plan_id,
            page_number=page_number,
            text=text
        )
        db.session.add(t)
        db.session.commit()
        return_value = "{} - {} added".format(t.page_number, t.text[0:15])
    else:
        return_value = "plan and page already in database"
    return return_value
