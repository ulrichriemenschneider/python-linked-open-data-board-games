from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD, SKOS


BG = Namespace("https://boardgames.example/")
GAME = Namespace("https://boardgames.example/game/")
PROP = Namespace("https://boardgames.example/property/")
PERSON = Namespace("https://boardgames.example/person/")
PUBLISHER = Namespace("https://boardgames.example/publisher/")
MECHANIC = Namespace("https://boardgames.example/mechanic/")
SCHEME = Namespace("https://boardgames.example/scheme/")
CATEGORY = Namespace("https://boardgames.example/category/")

def create_graph():
    graph = Graph()

    graph.bind("bg", BG)
    graph.bind("game", GAME)
    graph.bind("person", PERSON)
    graph.bind("publisher", PUBLISHER)
    graph.bind("mechanic", MECHANIC)
    graph.bind("category", CATEGORY)
    graph.bind("scheme", SCHEME)
    graph.bind("prop", PROP)
    graph.bind("rdf", RDF)
    graph.bind("rdfs", RDFS)
    graph.bind("skos", SKOS)
    graph.bind("xsd", XSD)

    add_mechanics_scheme(graph)
    add_categories_scheme(graph)

    return graph

def add_games(graph, games):
    for game in games:
        add_game(
            graph,
            game
        )

def save_graph(graph, output_file):
    graph.serialize(
        destination=output_file,
        format="turtle"
    )

def add_game(graph, game):
    game_iri = GAME[str(game["bgg_id"])]

    graph.add(
        (
            game_iri,
            RDF.type,
            BG.BoardGame
        )
    )

    graph.add(
        (
            game_iri,
            RDFS.label,
            Literal(game["name"])
        )
    )

    graph.add(
        (
            game_iri,
            PROP.yearOfPublication,
            Literal(
                game["year"],
                datatype=XSD.integer
            )
        )
    )

    graph.add(
        (
            game_iri,
            PROP.minPlayer,
            Literal(
                game["min_players"],
                datatype=XSD.integer
            )
        )
    )

    graph.add(
        (
            game_iri,
            PROP.maxPlayer,
            Literal(
                game["max_players"],
                datatype=XSD.integer
            )
        )
    )

# ---------------------------------------------------------
# Designer mit dem Spiel verbinden
# ---------------------------------------------------------
    for designer in game.get("designers", []):
        designer_iri = add_person(
            graph,
            designer
        )

        graph.add(
            (
                game_iri,
                PROP.author,
                designer_iri
            )
        )

# ---------------------------------------------------------
# Publisher mit dem Spiel verbinden
# ---------------------------------------------------------
    for publisher in game.get("publishers", []):
        publisher_iri = add_publisher(
            graph,
            publisher
        )

        graph.add(
            (
                game_iri,
                PROP.publisher,
                publisher_iri
            )
        )

# ---------------------------------------------------------
# Mechanic mit dem Spiel verbinden
# ---------------------------------------------------------
    for mechanic in game.get("mechanics", []):
        mechanic_iri = add_mechanic(
            graph,
            mechanic
        )

        graph.add(
            (
                game_iri,
                PROP.mechanic,
                mechanic_iri
            )
        )

# ---------------------------------------------------------
# Category mit dem Spiel verbinden
# ---------------------------------------------------------
    for category in game.get("categories", []):
        category_iri = add_category(
            graph,
            category
        )

        graph.add(
            (
                game_iri,
                PROP.category,
                category_iri
            )
        )

    return game_iri

def add_person(graph, person):
    person_iri = PERSON[str(person["bgg_id"])]

    graph.add(
        (
            person_iri,
            RDF.type,
            BG.Person
        )
    )

    graph.add(
        (
            person_iri,
            RDFS.label,
            Literal(person["name"])
        )
    )

    return person_iri

def add_publisher(graph, publisher):
    publisher_iri = PUBLISHER[
        str(publisher["bgg_id"])
    ]

    graph.add(
        (
            publisher_iri,
            RDF.type,
            BG.Publisher
        )
    )

    graph.add(
        (
            publisher_iri,
            RDFS.label,
            Literal(publisher["name"])
        )
    )

    return publisher_iri

def add_mechanics_scheme(graph):
    scheme_iri = SCHEME["bgg-mechanics"]

    graph.add(
        (
            scheme_iri,
            RDF.type,
            SKOS.ConceptScheme
        )
    )

    graph.add(
        (
            scheme_iri,
            SKOS.prefLabel,
            Literal(
                "BGG Board Game Mechanics",
                lang="en"
            )
        )
    )

    return scheme_iri

def add_mechanic(graph, mechanic):
    mechanic_iri = MECHANIC[
        str(mechanic["bgg_id"])
    ]

    scheme_iri = SCHEME["bgg-mechanics"]

    graph.add(
        (
            mechanic_iri,
            RDF.type,
            SKOS.Concept
        )
    )

    graph.add(
        (
            mechanic_iri,
            SKOS.prefLabel,
            Literal(
                mechanic["name"],
                lang="en"
            )
        )
    )

    graph.add(
        (
            mechanic_iri,
            SKOS.inScheme,
            scheme_iri
        )
    )

    return mechanic_iri

def add_categories_scheme(graph):
    scheme_iri = SCHEME["bgg-categories"]

    graph.add(
        (
            scheme_iri,
            RDF.type,
            SKOS.ConceptScheme
        )
    )

    graph.add(
        (
            scheme_iri,
            SKOS.prefLabel,
            Literal(
                "BGG Board Game Categories",
                lang="en"
            )
        )
    )

    return scheme_iri

def add_category(graph, category):
    category_iri = CATEGORY[
        str(category["bgg_id"])
    ]

    scheme_iri = SCHEME["bgg-categories"]

    graph.add(
        (
            category_iri,
            RDF.type,
            SKOS.Concept
        )
    )

    graph.add(
        (
            category_iri,
            SKOS.prefLabel,
            Literal(
                category["name"],
                lang="en"
            )
        )
    )

    graph.add(
        (
            category_iri,
            SKOS.inScheme,
            scheme_iri
        )
    )

    return category_iri

if __name__ == "__main__":
    add_mechanics_scheme(graph)
    add_categories_scheme(graph)

    test_game = {
        "bgg_id": 224517,
        "name": "Brass: Birmingham",
        "year": 2018,
        "min_players": 2,
        "max_players": 4,
        "designers": [
            {
                "bgg_id": 328,
                "name": "Martin Wallace"
            }
        ],
        "publishers": [
            {
                "bgg_id": 12345,
                "name": "Roxley"
            }
        ],
        "mechanics": [
        {
            "bgg_id": 2040,
            "name": "Hand Management"
        },
        {
            "bgg_id": 2004,
            "name": "Set Collection"
        }
        ],
        "mechanics": [
            {
                "bgg_id": 2040,
                "name": "Hand Management"
            },
            {
                "bgg_id": 2004,
                "name": "Set Collection"
            }
        ],
        "categories": [
            {
                "bgg_id": 1021,
                "name": "Economic"
            },
            {
                "bgg_id": 1088,
                "name": "Industry / Manufacturing"
            }
        ]
    }

    add_game(graph, test_game)

    print(
        graph.serialize(
            format="turtle"
        )
    )