from rdflib import Graph, Literal, Namespace
from pprint import pprint

MECHANIC = Namespace("https://boardgames.example/mechanic/")
GAME = Namespace("https://boardgames.example/game/")
CATEGORY = Namespace("https://boardgames.example/category/")

graph = Graph()

graph.parse(
    "data/bgg_boardgames.ttl",
    format="turtle"
)

print(f"Anzahl der Tripel: {len(graph)}")

def build_category_view_by_id(
    graph,
    category_id
):
    category_iri = CATEGORY[
        str(category_id)
    ]

    details = get_category_by_id(
        graph,
        category_id
    )

    if not details:
        return None

    detail = details[0]

    games = find_games_by_category_iri(
        graph,
        category_iri
    )

    data = {
        "iri": str(category_iri),
        "label": str(detail.categoryName),
        "scheme": {
            "iri": str(detail.scheme),
            "label": str(detail.schemeName),
        },
        "games": [],
    }

    for game in games:
        game_iri = str(game.game)

        data["games"].append(
            {
                "id": int(
                    game_iri.rsplit("/", 1)[-1]
                ),
                "iri": game_iri,
                "label": str(game.gameName),
            }
        )

    return data

def find_games_by_category_iri(
    graph,
    category_iri
):
    query = """
    PREFIX bg: <https://boardgames.example/>
    PREFIX prop: <https://boardgames.example/property/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?game ?gameName
    WHERE {
        ?game
            a bg:BoardGame ;
            rdfs:label ?gameName ;
            prop:category ?category .
    }
    ORDER BY ?gameName
    """

    return graph.query(
        query,
        initBindings={
            "category": category_iri
        }
    )

def get_category_by_id(graph, category_id):
    category_iri = CATEGORY[
        str(category_id)
    ]

    query = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT ?categoryName ?scheme ?schemeName
    WHERE {
        ?category
            a skos:Concept ;
            skos:prefLabel ?categoryName ;
            skos:inScheme ?scheme .

        ?scheme
            a skos:ConceptScheme ;
            skos:prefLabel ?schemeName .
    }
    """

    results = graph.query(
        query,
        initBindings={
            "category": category_iri
        }
    )

    return list(results)

def build_game_view_by_id(
    graph,
    game_id
):
    game_iri = GAME[
        str(game_id)
    ]

    details = get_game_by_id(
        graph,
        game_id
    )

    if not details:
        return None

    detail = details[0]

    mechanics = get_game_mechanics(
        graph,
        game_iri
    )

    categories = get_game_categories(
        graph,
        game_iri
    )

    data = {
        "iri": str(game_iri),
        "name": str(detail.name),
        "year": int(detail.year),
        "min_players": int(detail.minPlayers),
        "max_players": int(detail.maxPlayers),
        "mechanics": [],
        "categories": [],
    }

    for mechanic in mechanics:
        mechanic_iri = str(
            mechanic.mechanic
        )

        data["mechanics"].append(
            {
                "id": int(
                    mechanic_iri.rsplit("/", 1)[-1]
                ),
                "iri": mechanic_iri,
                "label": str(mechanic.label),
            }
        )

    for category in categories:
        category_iri = str(
            category.category
        )

        data["categories"].append(
            {
                "id": int(
                    category_iri.rsplit("/", 1)[-1]
                ),
                "iri": category_iri,
                "label": str(category.label),
            }
        )

    return data

def get_game_categories(graph, game_iri):
    query = """
    PREFIX prop: <https://boardgames.example/property/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT ?category ?label
    WHERE {
        ?game
            prop:category ?category .

        ?category
            a skos:Concept ;
            skos:prefLabel ?label .
    }
    ORDER BY ?label
    """

    return graph.query(
        query,
        initBindings={
            "game": game_iri
        }
    )

def get_game_mechanics(graph, game_iri):
    query = """
    PREFIX prop: <https://boardgames.example/property/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT ?mechanic ?label
    WHERE {
        ?game
            prop:mechanic ?mechanic .

        ?mechanic
            a skos:Concept ;
            skos:prefLabel ?label .
    }
    ORDER BY ?label
    """

    return graph.query(
        query,
        initBindings={
            "game": game_iri
        }
    )

def get_game_by_id(graph, game_id):
    game_iri = GAME[
        str(game_id)
    ]

    query = """
    PREFIX bg: <https://boardgames.example/>
    PREFIX prop: <https://boardgames.example/property/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?name ?year ?minPlayers ?maxPlayers
    WHERE {
        ?game
            a bg:BoardGame ;
            rdfs:label ?name ;
            prop:yearOfPublication ?year ;
            prop:minPlayer ?minPlayers ;
            prop:maxPlayer ?maxPlayers .
    }
    """

    results = graph.query(
        query,
        initBindings={
            "game": game_iri
        }
    )

    return list(results)

def get_mechanic_by_id(graph, mechanic_id):
    mechanic_iri = MECHANIC[
        str(mechanic_id)
    ]

    query = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT ?mechanicName ?scheme ?schemeName
    WHERE {
        ?mechanic
            a skos:Concept ;
            skos:prefLabel ?mechanicName ;
            skos:inScheme ?scheme .

        ?scheme
            a skos:ConceptScheme ;
            skos:prefLabel ?schemeName .
    }
    """

    results = graph.query(
        query,
        initBindings={
            "mechanic": mechanic_iri
        }
    )

    return list(results)

def find_games_by_mechanic_iri(
    graph,
    mechanic_iri
):
    query = """
    PREFIX bg: <https://boardgames.example/>
    PREFIX prop: <https://boardgames.example/property/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?game ?gameName
    WHERE {
        ?game
            a bg:BoardGame ;
            rdfs:label ?gameName ;
            prop:mechanic ?mechanic .
    }
    ORDER BY ?gameName
    """

    return graph.query(
        query,
        initBindings={
            "mechanic": mechanic_iri
        }
    )

def build_mechanic_view_by_id(graph, mechanic_id):
    mechanic_iri = MECHANIC[
        str(mechanic_id)
    ]

    details = get_mechanic_by_id(
        graph,
        mechanic_id
    )

    if not details:
        return None

    detail = details[0]

    games = find_games_by_mechanic_iri(
        graph,
        mechanic_iri
    )

    data = {
        "iri": str(mechanic_iri),
        "label": str(detail.mechanicName),
        "scheme": {
            "iri": str(detail.scheme),
            "label": str(detail.schemeName),
        },
        "games": [],
    }

    for game in games:
        game_iri = str(game.game)

        data["games"].append(
            {
                "id": int(
                    game_iri.rsplit("/", 1)[-1]
                ),
                "iri": game_iri,
                "label": str(game.gameName),
            }
        )

    return data

def list_all_games():
    query = """
    PREFIX bg: <https://boardgames.example/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?game ?name
    WHERE {
        ?game a bg:BoardGame ;
            rdfs:label ?name .
    }
    ORDER BY ?name
    """

    results = graph.query(query)

    for row in results:
        print(row.name)

def list_games_and_mechanics():
    query = """
    PREFIX bg: <https://boardgames.example/>
    PREFIX prop: <https://boardgames.example/property/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?gameName ?mechanicName
    WHERE {
        ?game a bg:BoardGame ;
            rdfs:label ?gameName ;
            prop:mechanic ?mechanic .

        ?mechanic a skos:Concept ;
                skos:prefLabel ?mechanicName .
    }
    ORDER BY ?gameName ?mechanicName
    """

    results = graph.query(query)
    
    for row in results:
        print(
            f"{row.gameName} -> "
            f"{row.mechanicName}"
        )

def find_games_by_mechanic(graph, mechanic_name):
    query = """
    PREFIX bg: <https://boardgames.example/>
    PREFIX prop: <https://boardgames.example/property/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?game ?gameName
    WHERE {
        ?game a bg:BoardGame ;
              rdfs:label ?gameName ;
              prop:mechanic ?mechanic .

        ?mechanic
            skos:prefLabel ?mechanicName .

        FILTER(
            LCASE(STR(?mechanicName)) =
            LCASE(STR(?searchName))
        )
    }
    ORDER BY ?gameName
    """

    results = graph.query(
        query,
        initBindings={
            "searchName": Literal(mechanic_name)
        }
    )

    return results

def get_mechanic_details(graph, mechanic_name):
    query = """
    PREFIX prop: <https://boardgames.example/property/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?mechanic ?mechanicName ?scheme ?schemeName
    WHERE {
        ?mechanic
            a skos:Concept ;
            skos:prefLabel ?mechanicName ;
            skos:inScheme ?scheme .

        ?scheme
            a skos:ConceptScheme ;
            skos:prefLabel ?schemeName .

        FILTER(
            LCASE(STR(?mechanicName)) =
            LCASE(STR(?searchName))
        )
    }
    """

    results = graph.query(
        query,
        initBindings={
            "searchName": Literal(mechanic_name)
        }
    )

    return list(results)

def build_mechanic_view(graph, mechanic_name):
    details = get_mechanic_details(graph, mechanic_name)

    if not details:
        return None

    detail = details[0]

    games = find_games_by_mechanic(graph, mechanic_name)

    data = {
        "iri": str(detail.mechanic),
        "label": str(detail.mechanicName),
        "scheme": {
            "iri": str(detail.scheme),
            "label": str(detail.schemeName),
        },
        "games": [],
    }

    for game in games:
        data["games"].append(
            {
                "iri": str(game.game),
                "label": str(game.gameName),
            }
        )

    return data

def main():
    print(
        f"Anzahl der Tripel: {len(graph)}"
    )

    data = build_mechanic_view("Hand Management")

    pprint(data, sort_dicts=False)


if __name__ == "__main__":
    main()