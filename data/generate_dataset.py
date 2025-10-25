import json, random, pathlib

CATEGORIAS = ["Informática", "Ciencia", "Historia", "Matemática", "Literatura", "Salud"]
AUTORES = ["Juan Pérez", "María Gómez", "Ana Rodríguez", "Luis Hernández", "Carla Mena", "Diego Vargas"]
TITULOS = [
    "Introducción a Bases de Datos",
    "Algoritmos y Estructuras de Datos",
    "Aprendizaje Automático Práctico",
    "Historia de la Computación",
    "Minería de Datos",
    "Sistemas Distribuidos",
    "Procesamiento de Lenguaje Natural",
    "Análisis de Datos con Python",
    "Diseño de APIs",
    "Introducción a Elasticsearch"
]
DESCS = [
    "Texto sobre fundamentos y aplicaciones.",
    "Guía práctica con ejemplos.",
    "Libro sobre teoría y casos de estudio.",
    "Cobertura de conceptos avanzados y prácticas recomendadas.",
    "Enfoque en rendimiento y escalabilidad."
]

def make_record(i):
    titulo = random.choice(TITULOS)
    cat = random.choice(CATEGORIAS)
    autor = random.choice(AUTORES)
    anio = random.randint(1995, 2025)
    desc = f"{random.choice(DESCS)} Incluye temas de bases de datos relacionales y no relacionales, búsqueda por texto completo y relevancia."
    return {
        "titulo": f"{titulo} #{i}",
        "autor": autor,
        "categoria": cat,
        "descripcion": desc,
        "anio": anio,
        "titulo_suggest": {"input": [titulo, f"{titulo} #{i}"]}
    }

def main(n=300):
    out = pathlib.Path(__file__).parent / "seed.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for i in range(1, n+1):
            json.dump(make_record(i), f, ensure_ascii=False)
            f.write("\n")
    print(f"OK -> {out.resolve()}")

if __name__ == "__main__":
    main(300)