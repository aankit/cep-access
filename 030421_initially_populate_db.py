import os
import re
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextBoxHorizontal
import spacy
from multiprocessing import Pool
import logging

from app import db
from app.models import School, Plan, PlanText
from app.utils import add_school, add_plan

# app_dir = os.path.dirname(__file__)

nlp = spacy.load('en_core_web_sm')
# RE_COMBINE_WHITESPACE = re.compile(r"\s+")


def clean_text(text):
    text = text.replace('\n', ' ').strip()
    # text = RE_COMBINE_WHITESPACE.sub(" ", element_text)
    doc = nlp(text)
    list_of_non_stop_words = [token.text for token in doc if not token.is_stop]
    text = " ".join(list_of_non_stop_words)
    return text


def get_new_plans(plan_dir):
    pdf_path = plan_dir + '/pdfs'
    plans = []
    for item in os.listdir(pdf_path):
        if not item.startswith("."):
            path = pdf_path + '/' + item
            for pdf in os.listdir(path):
                plan_data = {}
                plan_data['year'] = item
                plan_data['bn'] = pdf[:4]
                school_id = add_school(db, School, plan_data['bn'])
                plan_data['school_id'] = school_id
                plan_data['pdf_path'] = path + '/' + pdf
                plan_data['pages'] = []
                plans.append(plan_data)
    return plans


def add_new_plans(plans):
    for plan in plans:
        plan_id = add_plan(db, Plan, plan['year'], plan['school_id'])
        plan['id'] = plan_id
    return plans


def process_pages(plan):
    pdf_path = '/Users/Aankit/Documents/CEP/pdfs/{}/{}.pdf'.format(
        plan.year, plan.bn)
    print("processing plan #{} from {}".format(plan.id, pdf_path))
    plan_data = []
    pages = extract_pages(pdf_path)
    try:
        for page in pages:
            print("{} in progress".format(page.pageid))
            page_data = {
                'plan_id': plan.id,
                'page_number': page.pageid
            }
            page_data['text'] = str()
            page_text = list()
            for element in page:
                if isinstance(element, LTTextBoxHorizontal):
                    element_text = element.get_text()
                    element_text = clean_text(element_text)
                    if element_text:
                        page_text.append(element_text)
            page_data['text'] = " ".join(page_text)
            plan_data.append(page_data)
            print(
                "{}-{} added to dictionary".format(page_data['plan_id'], page_data['page_number']))
    except:
        logging.info("Plan Text {} didn't parse".format(plan.id))
    return plan_data


def add_text(plans):
    pages_to_insert = [page for plan in plans for page in plan]
    db.engine.execute(PlanText.__table__.insert(), pages_to_insert)


if __name__ == "__main__":
    # plan_dir = '/Users/Aankit/Documents/CEP'
    # plan_id = add_plan(db, Plan, school_id) #previously executed, commented out to help with debugging of text add
    # plans_data = get_new_plans(plan_dir) #previously executed, commented out to help with debugging of text add
    # plans_data = add_new_plans(plans_data) #previously executed, commented out to help with debugging of text add
    plans_with_text = db.session.query(PlanText.plan_id)
    plans_without_text = db.session.query(Plan.id, Plan.year, School.bn).join(
        School).filter(Plan.id.notin_(plans_with_text)).all()
    print("starting page processing")
    pool = Pool(4)
    plans_to_add = pool.map(process_pages, plans_without_text)
    add_text(plans_to_add)
