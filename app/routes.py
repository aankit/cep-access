from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import SearchForm
from app.models import School, Plan, PlanText
from collections import Counter


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        page = request.args.get('page', 1, type=int)
        subquery = db.session.query(School)
        texts = None
        stats = None
        # school filters
        if int(form.school.data) > 0:
            s = int(form.school.data)
            subquery = subquery.filter(School.id == s)
        if int(form.community_board.data) > 0:
            cb = int(form.community_board.data)
            subquery = subquery.filter(School.community_district == cb)
        if int(form.school_district.data) > 0:
            sd = int(form.school_district.data)
            subquery = subquery.filter(School.school_district == sd)
        school_ids = [s.id for s in subquery.all()]
        # pull plans for filtered schools
        plans = db.session.query(Plan).join(School).filter(
            Plan.school_id.in_(school_ids), School.school_name != None).order_by(
            Plan.year.desc(), School.school_name)
        # plan filters
        if form.year.data != "None":
            plans = plans.filter(Plan.year == form.year.data)
        if form.search_term.data:
            # search_term_data = dict.fromkeys([p.year for p in plans])
            st = form.search_term.data.split(",")
            plan_ids = [p.id for p in plans]
            # we're just going to pull everything all at once...
            texts, total = PlanText.filtered_search_all(
                st, plan_ids, page, app.config['PER_PAGE'])
            # re-route if search results will not be helpful to user
            if total == 10000:
                return render_template('search_help.html',
                                       title='Search Help',
                                       search_warning="Ten thousand or more results. Try narrowing your search.")
            if total == 0:
                return render_template('search_help.html',
                                       title='Search Help',
                                       search_warning="No results. Try another term.")

        # pull text data for display
        if texts:
            stats = dict.fromkeys([p.year for p in plans])
            for key, value in stats.items():
                stats[key] = {}
                tsq = texts.group_by(PlanText.plan_id).subquery()
                stats[key]['matched_schools'] = Plan.query.join(
                    tsq, Plan.id == tsq.c.plan_id).filter(Plan.year == key).count()
                stats[key]['total_schools'] = plans.filter(
                    Plan.year == key).distinct(School.bn).count()
                stats[key]['percent'] = round(
                    float(stats[key]['matched_schools']/stats[key]['total_schools'])*100, 1)
            texts = texts.all()
        # plan data for display
        plans = plans.all()
        return render_template('plans.html',
                               title='Plans',
                               space=app.config['SPACE_URL'],
                               plans=plans,
                               texts=texts,
                               stats=stats,
                               form=form)
    return render_template('index.html', title='Home', form=form)

# @app.route('/search', methods=['GET, POST'])
# def search():
#     return


@app.route('/about')
def about():
    return render_template('about.html')
