from flask import Flask, request, render_template, jsonify
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
INDEX = "biblioteca"

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search():
    q = request.args.get("q", "").strip()
    categoria = request.args.get("categoria") or None
    anio = request.args.get("anio") or None
    anio = int(anio) if anio and anio.isdigit() else None

    must = []
    if q:
        must.append({
            "multi_match": {
                "query": q,
                "fields": ["titulo^2", "descripcion", "autor"]
            }
        })

    filters = []
    if categoria:
        filters.append({"term": {"categoria": categoria}})
    if anio:
        filters.append({"term": {"anio": anio}})

    query = {"bool": {"must": must or {"match_all": {}}, "filter": filters}}
    body = {"query": query, "size": 25, "sort": ["_score"]}

    res = es.search(index=INDEX, body=body)
    hits = [{
        "titulo": h["_source"]["titulo"],
        "autor": h["_source"]["autor"],
        "categoria": h["_source"]["categoria"],
        "anio": h["_source"]["anio"],
        "descripcion": h["_source"]["descripcion"],
        "score": h["_score"]
    } for h in res["hits"]["hits"]]

    return jsonify({"results": hits, "total": res["hits"]["total"]["value"]})

@app.route("/suggest", methods=["GET"])
def suggest():
    prefix = request.args.get("prefix", "").strip()
    if not prefix:
        return jsonify({"suggestions": []})

    body = {
        "suggest": {
            "titulo-suggest": {
                "prefix": prefix,
                "completion": { "field": "titulo_suggest", "size": 8 }
            }
        }
    }
    res = es.search(index=INDEX, body=body)
    options = res["suggest"]["titulo-suggest"][0]["options"]
    suggestions = [opt["text"] for opt in options]
    return jsonify({"suggestions": suggestions})

if __name__ == "__main__":
    app.run(debug=True, port=5001)