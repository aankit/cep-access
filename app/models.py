from app import db
from app.search import add_to_index, remove_from_index, query_index, filtered_query_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def filtered_search(cls, expression, filter_ids):
        ids, total = filtered_query_index(cls.__tablename__, expression, filter_ids)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(8), index=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    text_elements = db.relationship('PlanText', backref='plan', lazy='dynamic')

    def __repr__(self):
        return '<CEP {0}-{1}>'.format(self.year, self.school_id)


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bn = db.Column(db.String(4), index=True, unique=True)
    dbn = db.Column(db.String(8), index=True, unique=True)
    school_name = db.Column(db.String(100), index=True)
    school_district = db.Column(db.Integer, index=True)
    council_district = db.Column(db.Integer, index=True)
    community_district = db.Column(db.Integer, index=True)
    plans = db.relationship(Plan, backref='school', lazy='dynamic')

    def __repr__(self):
        return '<School {}>'.format(self.school_name)


class PlanText(SearchableMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'))
    page_number = db.Column(db.Integer)
    text = db.Column(db.Text)
    __searchable__ = ['text']
