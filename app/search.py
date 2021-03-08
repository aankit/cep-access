from app import app


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


def filtered_query_index(index, query, ids):
    if not app.elasticsearch:
        return [], 0
    body = {
        'query': {
            'bool': {
                'must': {
                    'bool': {
                        'should': [],
                    }
                },
                'filter': {
                    'ids': {
                        'values': ids
                    }
                }
            }
        }
    }
    for term in query:
        term_dict = {'match': {'text': term}}
        body['query']['bool']['must']['bool']['should'].append(term_dict)
    search = app.elasticsearch.search(index=index, body=body)
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']
