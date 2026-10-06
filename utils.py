from rdflib import Namespace
from rdflib.namespace import SKOS, RDF

MECHANIC = Namespace("https://boardgames.example/mechanic/")


def get_pref_label(graph, resource, language="de"):
    labels = list(graph.objects(resource, SKOS.prefLabel))

    # Gewünschte Sprache
    for label in labels:
        if label.language == language:
            return str(label)

    # Fallback: Englisch
    for label in labels:
        if label.language == "en":
            return str(label)

    # Fallback: irgendein vorhandenes Label
    if labels:
        return str(labels[0])

    return None


def get_concept(concept_name, graph, language="de"):
    concept = MECHANIC[concept_name]

    if (concept, RDF.type, SKOS.Concept) not in graph:
        return None

    data = {
        "iri": str(concept),
        "prefLabel": get_pref_label(graph, concept, language),
        "altLabels": [],
        "hiddenLabels": [],
        "broader": [],
        "narrower": [],
        "related": [],
        "scheme": None,
    }

    for label in graph.objects(concept, SKOS.altLabel):
        data["altLabels"].append(str(label))

    for label in graph.objects(concept, SKOS.hiddenLabel):
        data["hiddenLabels"].append(str(label))

    for broader in graph.objects(concept, SKOS.broader):
        data["broader"].append({
            "iri": str(broader),
            "label": get_pref_label(graph, broader, language),
        })

    for narrower in graph.subjects(SKOS.broader, concept):
        data["narrower"].append({
            "iri": str(narrower),
            "label": get_pref_label(graph, narrower, language),
        })

    for related in graph.objects(concept, SKOS.related):
        data["related"].append({
            "iri": str(related),
            "label": get_pref_label(graph, related, language),
        })

    scheme = graph.value(concept, SKOS.inScheme)

    if scheme:
        data["scheme"] = {
            "iri": str(scheme),
            "label": get_pref_label(graph, scheme, language),
        }

    return data
