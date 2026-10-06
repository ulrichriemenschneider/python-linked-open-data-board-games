# Board Game Linked Data

A small educational project for learning and experimenting with **Linked Data, RDF, SKOS and SPARQL** using board game data.

The project uses data from [BoardGameGeek (BGG)](https://boardgamegeek.com/) and transforms it into an RDF graph. A small Flask application makes the resulting resources accessible and allows navigation between board games, mechanics and categories.

## Purpose

This project was created as a practical way to understand the concepts behind **Linked Open Data and semantic web technologies**.

Instead of working with an abstract or scientific domain, board games are used as an easier-to-understand example.

The main topics explored in this project are:

- RDF and triples
- IRIs and namespaces
- RDF resources and literals
- RDF classes and properties
- SKOS concepts and concept schemes
- SPARQL queries
- RDFLib
- Linked Data modelling
- Navigating relationships between RDF resources
- Presenting RDF data through a web application

The project also serves as preparation for working with semantic web technologies used by projects such as **VIVO/Vitro**.

---

## Current Architecture

The basic data flow is:

```text
BoardGameGeek
      │
      ▼
BGG Ranking CSV
      │
      ▼
BGG XML API
      │
      ▼
Python Importer
      │
      ▼
RDFLib
      │
      ▼
RDF Graph / Turtle
      │
      ▼
SPARQL
      │
      ▼
Python View Model
      │
      ▼
Flask + Jinja
      │
      ▼
HTML
```

---

## RDF Model

The project currently models several types of resources.

### Board Games

Board games are represented as RDF resources:

```turtle
game:224517
    rdf:type bg:BoardGame ;
    rdfs:label "Brass: Birmingham" ;
    prop:yearOfPublication 2018 ;
    prop:minPlayer 2 ;
    prop:maxPlayer 4 .
```

Board games can be connected to other resources such as:

```text
BoardGame
   │
   ├── author ───────► Person
   │
   ├── publisher ────► Publisher
   │
   ├── mechanic ─────► skos:Concept
   │
   └── category ─────► skos:Concept
```

---

## SKOS

Board game mechanics and categories are represented as **SKOS concepts** instead of simple strings.

Example:

```turtle
mechanic:2040
    rdf:type skos:Concept ;
    skos:prefLabel "Hand Management"@en ;
    skos:inScheme scheme:bgg-mechanics .
```

Mechanics and categories use separate concept schemes:

```text
scheme:bgg-mechanics
scheme:bgg-categories
```

This makes it possible to treat concepts as independent resources with their own IRIs.

A board game therefore does not simply contain the text:

```text
"Hand Management"
```

Instead, it links to the resource:

```text
https://boardgames.example/mechanic/2040
```

The label is only a property describing that resource.

---

## BoardGameGeek Import

The project uses two BGG data sources.

### Ranking Data

The official BoardGameGeek ranking dump provides basic information such as:

- BGG ID
- name
- publication year
- rank
- average rating
- Bayesian average
- number of ratings

The ranking ZIP file is downloaded manually from the BoardGameGeek data dump page and placed in:

```text
importer/data/
```

The importer extracts and processes the CSV file.

### BGG XML API

Additional information is retrieved through the BGG XML API, including:

- designers
- artists
- publishers
- mechanics
- categories
- minimum number of players
- maximum number of players

The API requires a BoardGameGeek application token.

The token is stored locally in:

```text
.env
```

Example:

```text
BGG_TOKEN=your_token_here
```

The `.env` file must **not** be committed to Git.

---

## RDF Generation

The imported BGG data is transformed into RDF using **RDFLib**.

The generated graph is currently stored as:

```text
data/bgg_boardgames.ttl
```

BGG IDs are used to create stable local resource identifiers.

Examples:

```text
https://boardgames.example/game/224517

https://boardgames.example/mechanic/2040

https://boardgames.example/category/...

https://boardgames.example/person/...

https://boardgames.example/publisher/...
```

Using IDs instead of names prevents resource identity from depending on labels.

---

## SPARQL

The RDF graph can be queried using SPARQL.

Example:

```sparql
PREFIX bg: <https://boardgames.example/>
PREFIX prop: <https://boardgames.example/property/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?gameName ?mechanicName
WHERE {
    ?game
        a bg:BoardGame ;
        rdfs:label ?gameName ;
        prop:mechanic ?mechanic .

    ?mechanic
        a skos:Concept ;
        skos:prefLabel ?mechanicName .
}
ORDER BY ?gameName ?mechanicName
```

SPARQL queries are used by the Python application to retrieve resources and their relationships from the graph.

---

## Web Application

A small **Flask** application provides a web interface for the RDF data.

The application loads:

```text
data/bgg_boardgames.ttl
```

into an RDFLib graph.

The general request flow is:

```text
Browser
   │
   ▼
Flask Route
   │
   ▼
Python Query Function
   │
   ▼
SPARQL
   │
   ▼
RDF Graph
   │
   ▼
Python Dictionary
   │
   ▼
Jinja Template
   │
   ▼
HTML
```

---

## Resource Pages

Resources are addressed by their IDs rather than their labels.

### Board Game

```text
/game/<id>
```

Example:

```text
/game/224517
```

A game page currently displays information such as:

- name
- IRI
- publication year
- player count
- mechanics
- categories

### Mechanic

```text
/mechanic/<id>
```

A mechanic is represented as a `skos:Concept`.

The page displays:

- preferred label
- IRI
- concept scheme
- board games using the mechanic

### Category

```text
/category/<id>
```

Categories are also represented as `skos:Concept` resources and belong to their own concept scheme.

The page displays:

- preferred label
- IRI
- concept scheme
- board games belonging to the category

---

## Linked Navigation

The Flask application allows navigation through relationships in the RDF graph.

For example:

```text
Board Game
    │
    ├──► Mechanic
    │       │
    │       └──► Board Games using this mechanic
    │
    └──► Category
            │
            └──► Board Games in this category
```

This demonstrates an important Linked Data principle:

> Resources are identified by IRIs and connected to other resources through explicitly defined relationships.

Labels such as `"Hand Management"` are descriptions of resources, not their identities.

---

## Project Structure

```text
python_lod/
├── .env
├── .gitignore
├── app.py
├── query_rdf.py
├── README.md
│
├── data/
│   ├── boardgames.ttl
│   ├── mechanics.ttl
│   ├── ontology.ttl
│   └── bgg_boardgames.ttl
│
├── importer/
│   ├── data/
│   │   └── boardgames_ranks.csv
│   ├── bgg_games.py
│   ├── bgg_importer.py
│   └── rdf_importer.py
│
└── templates/
    ├── game.html
    ├── mechanic.html
    └── category.html
```

---

## Technologies

- Python
- Flask
- Jinja
- RDFLib
- RDF
- RDFS
- SKOS
- OWL
- SPARQL
- Turtle
- BoardGameGeek XML API

---

## Running the Project

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the required dependencies.

Then start the Flask application:

```bash
python app.py
```

The development server is available at:

```text
http://127.0.0.1:5000
```

---

## Current Status

The project is under active development and primarily serves as a learning environment.

Currently implemented:

- BGG ranking data import
- BGG XML API integration
- conversion of board game data into RDF
- RDF resources for games, people and publishers
- SKOS concepts for mechanics
- SKOS concepts for categories
- separate SKOS concept schemes
- Turtle serialization
- SPARQL queries with RDFLib
- Flask web application
- board game detail pages
- mechanic detail pages
- category detail pages
- navigation between games and SKOS concepts

---

## Planned Next Steps

Possible next steps include:

- designer resource pages
- publisher resource pages
- improved HTML templates
- reusable template components
- additional SPARQL queries
- SKOS relationships such as `skos:broader`, `skos:narrower` and `skos:related`
- improved language handling for SKOS labels
- generic RDF resource handling
- comparison of the implementation with VIVO/Vitro concepts and templates

---

## Disclaimer

This is an educational project and is not affiliated with BoardGameGeek.

BoardGameGeek data is used as a practical dataset for learning RDF, Linked Data, SKOS and SPARQL.