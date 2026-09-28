from rdflib import Graph, Namespace
from rdflib.namespace import RDFS, SKOS

graph = Graph()

graph.parse("boardgames.ttl", format="turtle")

print(f"Anzahl der Tripel: {len(graph)}")

GAME = Namespace("https://boardgames.example/game/")
PROP = Namespace("https://boardgames.example/property/")

game = GAME["auf-nach-japan"]

#for author in graph.objects(game, PROP.author):
#    label = graph.value(author, RDFS.label)
#    print(label)

MECHANIC = Namespace("https://boardgames.example/mechanic/")

concept = MECHANIC["set-collection"]

#print("\nPreferred Labels:")

#for label in graph.objects(concept, SKOS.prefLabel):
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