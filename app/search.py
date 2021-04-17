from app import app
import pprint

pp = pprint.PrettyPrinter(indent=4)


def add_to_index(index, model):
    if not app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    app.elasticsearch.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
    if not app.elasticsearch:
        return
    app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
    if not app.elasticsearch:
        return [], 0
    search = app.elasticsearch.search(
        index=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
              'from': (page - 1) * per_page, 'size': per_page})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']


def filtered_query_index(index, terms, plan_ids, page, per_page):
    if not app.elasticsearch:
        return [], 0
    # filter_body = {'query': { 'bool': { 'must': [{ 'match': { 'text': 'cs4all'}},{'terms': {'plan_id': plan_ids}}]}}}
    # body = {
    #     'query': {
    #         'bool': {
    #             'must': [],
    #         }
    #     },
    #     'from': (page-1) * per_page,
    #     'size': per_page
    # }
    body = {
        'query': {
            'bool': {
                'filter': {
                    'terms': {
                        'plan_id': plan_ids
                    }
                },
                'should': [],
                'minimum_should_match': 1
            }
        },
        'from': (page-1) * per_page,
        'size': per_page
    }
    for term in terms:
        if " " in term:
            term_dict = {
                'match_phrase': {
                    'text': {
                        'query': term,
                        'analyzer': 'stop'
                    }
                }
            }
        else:
            term_dict = {'match': {'text': term}}
        body['query']['bool']['should'].append(term_dict)
    # if len(plan_ids) > 0:
    #     body['query']['bool']['must'].append({'terms': {'plan_id': plan_ids}})
    search = app.elasticsearch.search(index=index, body=body)
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']

def filtered_query_count(index, terms, plan_ids):
    body = {
        'query': {
            'bool': {
                'filter': {
                    'terms': {
                        'plan_id': plan_ids
                    }
                },
                'should': [],
                'minimum_should_match': 1
            }
        }
    }
    for term in terms:
        if " " in term:
            term_dict = {
                'match_phrase': {
                    'text': {
                        'query': term,
                        'analyzer': 'stop'
                    }
                }
            }
        else:
            term_dict = {'match': {'text': term}}
        body['query']['bool']['should'].append(term_dict)
    count = app.elasticsearch.count(index=index, body=body)
    return count
