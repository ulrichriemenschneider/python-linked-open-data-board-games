# Board Game Linked Data

A small educational Linked Data application built with **Python, RDF, SKOS, SPARQL, RDFLib, and Flask**.

The project uses board game data from **BoardGameGeek (BGG)** and transforms it into an RDF graph. A Flask web application provides a simple interface for navigating the resulting Linked Data resources.

The main purpose of this project is to explore and understand technologies and concepts used in **Linked Data**, **Semantic Web applications**, and systems such as **VIVO/Vitro**.

---

## Project Goals

This project was created as a learning project for working with:

- RDF and RDF triples
- IRIs and namespaces
- RDF classes and properties
- RDFLib
- SPARQL
- SKOS concepts and concept schemes
- Linked Data relationships
- External data APIs
- RDF serialization using Turtle
- Flask
- Jinja templates
- Resource-oriented navigation

Instead of scientific publications and research data, the project uses **board games** as an easier-to-understand domain.

---

## Data Source

The project uses data from **BoardGameGeek (BGG)**.

Two different BGG data sources are used.

### BGG Ranking Data

The official BGG ranking data dump provides basic information such as:

- BGG ID
- game name
- publication year
- rank
- average rating
- Bayesian average
- number of ratings

The ranking archive must currently be downloaded manually from the BoardGameGeek data dump page and placed inside:

```text
importer/data/
```

The importer extracts and processes the ranking CSV file.

### BGG XML API2

Additional information is retrieved through the BoardGameGeek XML API2.

For each game, the importer can retrieve information including:

- game name
- publication year
- minimum number of players
- maximum number of players
- designers
- artists
- publishers
- mechanics
- categories

The BGG API requires an application token.

---

## Linked Data Model

The imported data is transformed into RDF resources.

The project currently uses the following resource types:

```text
BoardGame
Person
Publisher
SKOS Concept
```

Board game mechanics and categories are represented as **SKOS concepts**.

Example relationship:

```text
Board Game
    |
    +-- author -------> Person
    |
    +-- publisher ----> Publisher
    |
    +-- mechanic -----> SKOS Concept
    |
    +-- category -----> SKOS Concept
```

This means that mechanics, categories, authors, and publishers are not stored merely as strings.

They are independent resources with their own IRIs.

---

## Example RDF

A simplified game could be represented as:

```turtle
game:224517
    rdf:type bg:BoardGame ;
    rdfs:label "Brass: Birmingham" ;
    prop:author person:123 ;
    prop:publisher publisher:456 ;
    prop:mechanic mechanic:789 ;
    prop:category category:101 .
```

The linked resources can then contain their own information:

```turtle
person:123
    rdf:type bg:Person ;
    rdfs:label "Example Designer" .

mechanic:789
    rdf:type skos:Concept ;
    skos:prefLabel "Hand Management"@en ;
    skos:inScheme scheme:bgg-mechanics .
```

The same resource can therefore be referenced from multiple games without duplicating its identity.

---

## IRIs

Resources use local IRIs based on their BoardGameGeek IDs.

Examples:

```text
https://boardgames.example/game/224517
https://boardgames.example/person/123
https://boardgames.example/publisher/456
https://boardgames.example/mechanic/789
https://boardgames.example/category/101
```

Using BGG IDs instead of names avoids problems caused by:

- duplicate names
- renamed resources
- spelling differences
- spaces and special characters

The IRI represents the identity of a resource, while labels describe that resource.

---

## SKOS

Board game mechanics and categories are modeled using the **Simple Knowledge Organization System (SKOS)**.

Two separate concept schemes are currently used:

```text
BGG Board Game Mechanics
BGG Board Game Categories
```

Mechanics are represented as:

```turtle
mechanic:123
    rdf:type skos:Concept ;
    skos:prefLabel "Deck Building"@en ;
    skos:inScheme scheme:bgg-mechanics .
```

Categories use the same structure but belong to the category concept scheme.

The BGG import currently does **not** create artificial `skos:broader`, `skos:narrower`, or `skos:related` relationships because these relationships are not provided by the imported BGG data.

---

## SPARQL

The RDF graph can be queried using SPARQL through RDFLib.

For example, games and their mechanics can be connected through:

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

The Flask application uses similar queries to retrieve resources and their relationships from the RDF graph.

---

## Web Application

A small Flask application provides a browser-based interface for navigating the RDF data.

The application currently provides pages for:

- games
- authors/designers
- publishers
- mechanics
- categories

The index page also displays statistics about the current RDF dataset, including the number of:

- games
- authors
- publishers
- mechanics
- categories

---

## Linked Navigation

The application allows navigation between related RDF resources.

For example:

```text
Game
 |
 +--> Author
 |      |
 |      +--> Games by this author
 |
 +--> Publisher
 |      |
 |      +--> Games published by this publisher
 |
 +--> Mechanic
 |      |
 |      +--> Games using this mechanic
 |
 +--> Category
        |
        +--> Games in this category
```

This demonstrates one of the central ideas of Linked Data:

> Resources are identified individually and connected through explicit relationships.

---

## Routes

The Flask application currently uses resource-oriented routes such as:

```text
/
```

Index page and dataset overview.

```text
/game/<id>
```

Displays a board game and its relationships.

```text
/author/<id>
```

Displays an author/designer and the imported games associated with that person.

```text
/publisher/<id>
```

Displays a publisher and the imported games associated with that publisher.

```text
/mechanic/<id>
```

Displays a SKOS mechanic concept and games using that mechanic.

```text
/category/<id>
```

Displays a SKOS category concept and games belonging to that category.

The numeric IDs correspond to the IDs used in the local RDF resource IRIs.

---

## Project Structure

```text
python_lod/
├── .env
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── app.py
├── query_rdf.py
│
├── data/
│   ├── ontology.ttl
│   ├── boardgames.ttl
│   ├── mechanics.ttl
│   └── bgg_boardgames.ttl
│
├── importer/
│   ├── bgg_games.py
│   ├── bgg_importer.py
│   ├── rdf_importer.py
│   │
│   └── data/
│       └── boardgames_ranks.csv
│
├── static/
│   └── css/
│       └── style.css
│
└── templates/
    ├── base.html
    ├── index.html
    ├── game.html
    ├── author.html
    ├── publisher.html
    ├── mechanic.html
    └── category.html
```

Some generated or downloaded files may not be included in the repository depending on the `.gitignore` configuration.

---

## Requirements

The project requires:

- Python 3
- Flask
- RDFLib
- Requests
- python-dotenv

The Python dependencies are defined in:

```text
requirements.txt
```

Current direct dependencies:

```text
Flask
rdflib
requests
python-dotenv
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd python_lod
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows:

```text
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## BoardGameGeek API Token

The BoardGameGeek XML API requires an application token.

Create a `.env` file in the project root:

```text
BGG_TOKEN=your_bgg_token_here
```

The real `.env` file must **not** be committed to Git.

The repository should instead contain an example file:

```text
.env.example
```

with:

```text
BGG_TOKEN=your_bgg_token_here
```

Make sure `.env` is included in `.gitignore`.

---

## Importing BGG Ranking Data

Download the current BoardGameGeek ranking archive from the official BGG data dump page.

Place the downloaded ZIP file inside:

```text
importer/data/
```

The importer can detect and extract the ranking archive.

The ranking CSV is then used to select games, for example the BGG Top 100.

---

## Retrieving Detailed Game Data

Detailed information is retrieved from the BGG XML API2.

The importer sends multiple BGG game IDs to the API and parses the returned XML.

The resulting Python data contains information such as:

```python
{
    "bgg_id": 224517,
    "name": "Example Game",
    "year": 2020,
    "min_players": 1,
    "max_players": 4,
    "designers": [],
    "artists": [],
    "publishers": [],
    "categories": [],
    "mechanics": []
}
```

---

## Generating RDF

The BGG data can be transformed into an RDFLib graph.

The RDF importer creates resources for:

```text
BoardGame
Person
Publisher
Mechanic
Category
```

The resulting graph is serialized using the Turtle format and stored as:

```text
data/bgg_boardgames.ttl
```

The Flask application loads this RDF file and queries it using SPARQL.

---

## Running the Web Application

After installing the dependencies and generating the RDF dataset, start the Flask application:

```bash
python app.py
```

Flask will display the local development URL in the terminal.

Open that URL in a browser to access the application.

---

## Templates and Styling

The application uses Jinja template inheritance.

All pages extend:

```text
templates/base.html
```

This provides shared HTML structure and navigation.

The global stylesheet is located at:

```text
static/css/style.css
```

The current interface uses:

- black background
- white text
- pink links
- no link underlining
- consistent link colors for visited links

The frontend is intentionally kept simple because the primary focus of the project is RDF, Linked Data, SKOS, SPARQL, and backend processing.

---

## Technologies

The project currently uses:

**Backend**

- Python
- Flask

**Semantic Web / Linked Data**

- RDF
- RDFLib
- SPARQL
- SKOS
- Turtle
- RDF Schema
- XML Schema datatypes

**Data Import**

- BoardGameGeek ranking data
- BoardGameGeek XML API2
- Requests
- Python XML parsing
- CSV
- ZIP archives

**Frontend**

- HTML
- Jinja
- CSS

---

## Architecture

A simplified overview of the application:

```text
BoardGameGeek
      |
      | Ranking CSV + XML API
      v
Python Importer
      |
      v
RDFLib Graph
      |
      v
Turtle RDF
bgg_boardgames.ttl
      |
      v
RDFLib
      |
      | SPARQL
      v
Python View Data
      |
      v
Flask
      |
      v
Jinja Templates
      |
      v
Browser
```

This separates the original BGG data source from the RDF representation and the web presentation layer.

---

## Current Status

The project currently supports:

- importing BGG ranking data
- retrieving detailed game information through the BGG API
- parsing BGG XML responses
- converting BGG data into RDF
- representing games as RDF resources
- representing designers as person resources
- representing publishers as independent resources
- representing mechanics as SKOS concepts
- representing categories as SKOS concepts
- separate SKOS concept schemes for mechanics and categories
- serialization to Turtle
- querying the RDF graph with SPARQL
- Flask-based resource pages
- navigation between games and mechanics
- navigation between games and categories
- navigation between games and authors
- navigation between games and publishers
- listing games associated with an author
- listing games associated with a publisher
- displaying dataset statistics on the index page
- shared Jinja templates
- shared CSS styling

---

## Limitations

The application is an educational project and is not intended to be a complete BoardGameGeek replacement.

In particular, an author or publisher page only lists games that are present in the **locally imported RDF dataset**.

For example, if only the BGG Top 100 have been imported, an author's page only shows their games that occur within those imported games.

It does not represent the author's complete BoardGameGeek catalogue.

The imported BGG mechanics and categories also currently do not contain a SKOS hierarchy unless such relationships are explicitly added separately.

---

## Learning Context

This project was created to develop a practical understanding of technologies used in Linked Data applications.

A board game domain makes relationships easy to visualize:

```text
Game --> Designer
Game --> Publisher
Game --> Mechanic
Game --> Category
```

The same principles can be transferred to other knowledge domains such as scientific information systems:

```text
Publication --> Researcher
Publication --> Institution
Publication --> Subject
Researcher --> Organization
Subject --> SKOS Concept
```

This makes the project useful as a small-scale introduction to concepts that also appear in semantic-web systems such as VIVO/Vitro.

---

## Possible Next Steps

Possible future improvements include:

- publisher and author metadata
- artist resources
- more detailed game metadata
- multilingual labels
- additional SKOS relationships
- `skos:broader`
- `skos:narrower`
- `skos:related`
- search functionality
- pagination
- larger BGG datasets
- improved frontend styling
- RDF validation
- SHACL shapes
- content negotiation
- RDF resource endpoints
- additional SPARQL queries
- tests for the importer and query layer

---

## Disclaimer

This project is an independent educational project.

BoardGameGeek data is used as an external data source. This project is not affiliated with or endorsed by BoardGameGeek.

The `boardgames.example` IRIs used by the project are example/local identifiers for learning purposes and are not official BoardGameGeek identifiers.

---

## License

No license has currently been specified.

If this repository is intended to be publicly reusable, an appropriate open-source license should be added.