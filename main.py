from rdflib import Graph, Namespace
from rdflib.namespace import RDFS, SKOS

graph = Graph()

graph.parse("boardgames.ttl", format="turtle")

print(f"Anzahl der Tripel: {len(graph)}")

GAME = Namespace("https://boardgames.example/game/")
PROP = Namespace("https://boardgames.example/property/")

game = GAME["auf-nach-japan"]

# for author in graph.objects(game, PROP.author):
#    label = graph.value(author, RDFS.label)
#    print(label)

MECHANIC = Namespace("https://boardgames.example/mechanic/")

concept = MECHANIC["set-collection"]

# print("\nPreferred Labels:")

# for label in graph.objects(concept, SKOS.prefLabel):
#    if label.language == "de":
#        print(f"Deutsches Label: {label}")

broader = graph.value(concept, SKOS.broader)

print(f"\nBroader IRI: {broader}")

broader_label = None

for label in graph.objects(broader, SKOS.prefLabel):
    if label.language == "de":
        broader_label = label
        break

print(f"Übergeordneter Begriff: {broader_label}")

print("\nVerwandte Begriffe:")

for related in graph.objects(concept, SKOS.related):

    for label in graph.objects(related, SKOS.prefLabel):
        if label.language == "de":
            print(label)

# SPARQL

print("------SPARQL------")
query = """
PREFIX game: <https://boardgames.example/game/>
PREFIX prop: <https://boardgames.example/property/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?author ?name
WHERE {
    game:auf-nach-japan prop:author ?author .
    ?author rdfs:label ?name .
}
"""

results = graph.query(query)
#+
for row in results:
    print(f"Autor: {row.author}")
    print(f"Name:  {row.name}")

print("-------------")

query = """
PREFIX mechanic: <https://boardgames.example/mechanic/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?broader ?label
WHERE {
    mechanic:set-collection skos:broader ?broader .
    ?broader skos:prefLabel ?label .

    FILTER(LANG(?label) = "de")
}
"""

results = graph.query(query)

for row in results:
    print(f"Concept: {row.broader}")
    print(f"Label:   {row.label}")

print("-------------")

query = """
PREFIX prop: <https://boardgames.example/property/>
PREFIX mechanic: <https://boardgames.example/mechanic/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?game ?label
WHERE {
    ?game prop:mechanic mechanic:set-collection .
    ?game rdfs:label ?label .
}
"""

results = graph.query(query)

for row in results:
    print(f"Spiel:  {row.game}")
    print(f"Label:  {row.label}")

print("-------------")

query = """
PREFIX prop: <https://boardgames.example/property/>
PREFIX mechanic: <https://boardgames.example/mechanic/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?game ?gameLabel ?gameMechanic ?mechanicLabel
WHERE {
    ?game prop:mechanic ?gameMechanic .

    ?gameMechanic
        skos:broader mechanic:card-mechanics ;
        skos:prefLabel ?mechanicLabel .

    ?game rdfs:label ?gameLabel .

    FILTER(LANG(?mechanicLabel) = "de")
}
"""

results = graph.query(query)

for row in results:
    print(f"Spiel:     {row.gameLabel}")
    print(f"Mechanik:  {row.mechanicLabel}")
    print()

print("-------------")

print("SPARQL Property Path + (broader+)")
query = """
PREFIX mechanic: <https://boardgames.example/mechanic/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?concept ?label
WHERE {
    ?concept skos:broader+ mechanic:card-mechanics .
    ?concept skos:prefLabel ?label .

    FILTER(LANG(?label) = "en")
}
"""

results = graph.query(query)

for row in results:
    print(f"{row.label}")

print("-------------")

query = """
PREFIX prop: <https://boardgames.example/property/>
PREFIX mechanic: <https://boardgames.example/mechanic/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?gameLabel ?mechanicLabel
WHERE {
    ?game prop:mechanic ?gameMechanic .

    ?gameMechanic
        skos:broader+ mechanic:card-mechanics ;
        skos:prefLabel ?mechanicLabel .

    ?game rdfs:label ?gameLabel .

    FILTER(LANG(?mechanicLabel) = "de")
}
"""

results = graph.query(query)

for row in results:
    print(f"{row.gameLabel}: {row.mechanicLabel}")

print("-------------")
