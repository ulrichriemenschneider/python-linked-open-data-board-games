from flask import Flask, render_template
from rdflib import Graph
from query_rdf import build_mechanic_view, build_mechanic_view_by_id
from query_rdf import build_mechanic_view_by_id, build_game_view_by_id
from query_rdf import build_mechanic_view_by_id, build_game_view_by_id, build_category_view_by_id
from query_rdf import build_index_view, build_mechanic_view_by_id, build_game_view_by_id, build_category_view_by_id
from query_rdf import build_index_view, build_mechanic_view_by_id, build_category_view_by_id, build_game_view_by_id, build_author_view_by_id
from query_rdf import (
    build_index_view,
    build_mechanic_view_by_id,
    build_category_view_by_id,
    build_game_view_by_id,
    build_author_view_by_id,
    build_publisher_view_by_id,
)


app = Flask(__name__)

graph = Graph()

graph.parse(
    "data/bgg_boardgames.ttl",
    format="turtle"
)


@app.route("/")
def index():
    data = build_index_view(graph)

    return render_template(
        "index.html",
        data=data
    )


@app.route("/mechanic/<int:mechanic_id>")
def mechanic(mechanic_id):
    data = build_mechanic_view_by_id(
        graph,
        mechanic_id
    )

    if data is None:
        return "Mechanik nicht gefunden", 404

    return render_template(
        "mechanic.html",
        mechanic=data
    )

@app.route("/game/<int:game_id>")
def game(game_id):
    data = build_game_view_by_id(
        graph,
        game_id
    )

    if data is None:
        return "Spiel nicht gefunden", 404

    return render_template(
        "game.html",
        game=data
    )

@app.route("/category/<int:category_id>")
def category(category_id):
    data = build_category_view_by_id(
        graph,
        category_id
    )

    if data is None:
        return "Kategorie nicht gefunden", 404

    return render_template(
        "category.html",
        category=data
    )

@app.route("/author/<int:author_id>")
def author(author_id):
    data = build_author_view_by_id(
        graph,
        author_id
    )

    if data is None:
        return "Autor nicht gefunden", 404

    return render_template(
        "author.html",
        author=data
    )

@app.route("/publisher/<int:publisher_id>")
def publisher(publisher_id):
    data = build_publisher_view_by_id(
        graph,
        publisher_id
    )

    if data is None:
        return "Verlag nicht gefunden", 404

    return render_template(
        "publisher.html",
        publisher=data
    )


if __name__ == "__main__":
    app.run(debug=True)