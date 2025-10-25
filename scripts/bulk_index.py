from elasticsearch import Elasticsearch, helpers
import json, pathlib

INDEX = "biblioteca"

def stream_docs(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            doc = json.loads(line)
            yield {"_index": INDEX, "_source": doc}

def main():
    es = Elasticsearch("http://localhost:9200", request_timeout=60)
    data_path = pathlib.Path(__file__).parent.parent / "data" / "seed.jsonl"
    helpers.bulk(es, stream_docs(data_path))
    es.indices.refresh(index=INDEX)
    count = es.count(index=INDEX)["count"]
    print(f"Documentos indexados: {count}")

if __name__ == "__main__":
    main()