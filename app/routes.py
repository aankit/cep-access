from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import SearchForm

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        flash(form.search_term.data)
        return redirect('/')
    return render_template('index.html', title='Home', form=form)

# @app.route('/search', methods=['GET, POST'])
# def search():
#     return 

@app.route('/about')
def about():
    return("About this project")

