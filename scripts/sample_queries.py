from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
INDEX = "biblioteca"

def search_fulltext(q):
    body = {
        "query": {
            "multi_match": {
                "query": q,
                "fields": ["titulo^2", "descripcion", "autor"]
            }
        },
        "sort": ["_score"]
    }
    return es.search(index=INDEX, body=body)

def search_with_filters(q, categoria=None, anio=None):
    must = [{
        "multi_match": {
            "query": q,
            "fields": ["titulo^2", "descripcion", "autor"]
        }
    }]
    filters = []
    if categoria:
        filters.append({"term": {"categoria": categoria}})
    if anio:
        filters.append({"term": {"anio": anio}})
    body = {"query": {"bool": {"must": must, "filter": filters}}}
    return es.search(index=INDEX, body=body)

def search_fuzzy(q):
    body = {
        "query": {
            "multi_match": {
                "query": q,
                "fields": ["titulo^2", "descripcion"],
                "fuzziness": "AUTO"
            }
        }
    }
    return es.search(index=INDEX, body=body)

def autocomplete(prefix, size=5):
    body = {
        "suggest": {
            "titulo-suggest": {
                "prefix": prefix,
                "completion": {
                    "field": "titulo_suggest",
                    "size": size
                }
            }
        }
    }
    return es.search(index=INDEX, body=body)

if __name__ == "__main__":
    print("Fulltext:")
    print(search_fulltext("bases de datos")["hits"]["hits"][:2])
    print("Filtros:")
    print(search_with_filters("datos", categoria="Informática", anio=2023)["hits"]["hits"][:2])
    print("Fuzzy:")
    print(search_fuzzy("basses de datos")["hits"]["hits"][:2])
    print("Autocomplete:")
    print(autocomplete("Intro")["suggest"])