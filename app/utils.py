import requests
import io
import pandas as pd
from pdfminer.high_level import extract_pages
from sqlalchemy.orm.util import class_mapper
import logging

# response = requests.get("https://data.cityofnewyork.us/api/views/3bkj-34v2/files/56813139-9b9d-44fb-b81d-068553b7a9b7?download=true&filename=LCGMS_SchoolData(additional geocoded fields added).csv")
# lcgms = pd.read_csv(io.StringIO(response.text))
lcgms = pd.read_csv(
    '/Users/Aankit/Documents/CEP-search/app/static/LCGMS_SchoolData_additional_geocoded_fields_added_.csv')
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

def community_board_naming(num):
    if type(num) is int:
        if num > 500:
            return num, "Staten Island CB {}".format(num-500)
        elif num > 400:
            return num, "Queens CB {}".format(num-400)
        elif num > 300:
            return num, "Brooklyn CB {}".format(num-300)
        elif num > 200:
            return num, "Bronx CB {}".format(num-200)
        elif num > 100:
            return num, "Manhattan CB {}".format(num-100)
        else:
            return num, "Missing"
    return num, "Not Found"


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
    return e.id


def add_plan(db, Plan, year, school_id):
    e = db.session.query(Plan).filter_by(
        year=year, school_id=school_id).first()
    if not e:
        p = Plan(
            year=year,
            school_id=school_id
        )
        db.session.add(p)
        db.session.commit()
        return p.id
    return e.id


def get_pages(plan):
    #need to add pdf file paths to plan table for this function to work
    try:
        class_mapper(plan)
        page_data = []
        pages = extract_pages(plan.pdf_path)
        for page in pages:
            page_data = {
                'plan_id': plan.id,
                'page_number': page.pageid
            }
            page_data['text'] = str()
            page_text = list()
            for element in page:
                if isinstance(element, LTTextBoxHorizontal):
                    element_text = element.get_text()
                    if element_text:
                        element_text = element_text.replace('\n', ' ').strip()
                        page_text.append(element_text)
            page_data['text'] = " ".join(page_text)
            plan_data.append(page_data)
    except:
        logging.debug("Plan {} not a DB object or didn't parse".format(plan.id))
    return page_data


def batch_add_pages(plans):
    pages_to_insert = [page for plan in plans for page in plan]
    db.engine.execute(PlanText.__table__.insert(), pages_to_insert)


def add_page(db, PlanText, plan_id, page_number, text):
    e = db.session.query(PlanText).filter_by(
        plan_id=plan_id, page_number=page_number).first()
    if not e:
        t = PlanText(
            plan_id=plan_id,
            page_number=page_number,
            text=text
        )
        db.session.add(t)
        return_value = "{} - {} added".format(t.page_number, t.text[0:15])
    else:
        return_value = "plan and page already in database"
    return return_value
