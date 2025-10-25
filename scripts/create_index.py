from elasticsearch import Elasticsearch
import json, pathlib

INDEX = "biblioteca"

def main():
    es = Elasticsearch("http://localhost:9200", request_timeout=30)
    if es.indices.exists(index=INDEX):
        es.indices.delete(index=INDEX)

    mapping_path = pathlib.Path(__file__).parent.parent / "mappings" / "biblioteca_mapping.json"
    with open(mapping_path, "r", encoding="utf-8") as f:
        body = json.load(f)

    es.indices.create(index=INDEX, body=body)
    print(f"Índice creado: {INDEX}")

if __name__ == "__main__":
    main()