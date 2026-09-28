# Python Linked Open Data – Board Games

Dieses Projekt ist ein kleines Lernprojekt zum Verständnis von **Linked Open Data (LOD)**, **RDF**, **Turtle**, **SKOS** und der Verarbeitung von RDF-Daten mit Python.

Als Beispieldomäne werden **Brettspiele** verwendet. Informationen über Spiele, Autoren, Verlage und Spielmechaniken werden nicht als klassische Tabellen oder Python-Objekte gespeichert, sondern als **RDF-Graph** modelliert.

Das Projekt soll insbesondere zeigen:

- wie RDF-Daten aus **Subjekt – Prädikat – Objekt** aufgebaut sind,
- wie Ressourcen über **IRIs** eindeutig identifiziert werden,
- wie **Namespaces und Prefixes** funktionieren,
- wie RDF mit **Turtle** geschrieben werden kann,
- wie **SKOS Concepts** modelliert werden,
- wie Beziehungen zwischen Concepts dargestellt werden,
- wie Python mit **RDFLib** einen RDF-Graphen laden und durchsuchen kann.

---

## Projektstruktur

```text
python_lod/
├── boardgames.ttl
├── main.py
└── README.md
```

`boardgames.ttl` enthält den eigentlichen RDF-Graphen.

`main.py` lädt diesen Graphen mit RDFLib und liest Informationen daraus aus.

---

# boardgames.ttl

Die Datei `boardgames.ttl` enthält die RDF-Daten des Projekts im **Turtle-Format**.

## Prefixes und Namespaces

Am Anfang der Datei werden verschiedene Prefixes definiert:

```turtle
@prefix bg: <https://boardgames.example/> .
@prefix game: <https://boardgames.example/game/> .
@prefix person: <https://boardgames.example/person/> .
@prefix publisher: <https://boardgames.example/publisher/> .
@prefix mechanic: <https://boardgames.example/mechanic/> .
@prefix scheme: <https://boardgames.example/scheme/> .
@prefix prop: <https://boardgames.example/property/> .

@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
```

Die Prefixes sind Abkürzungen für vollständige IRIs.

Zum Beispiel:

```turtle
game:auf-nach-japan
```

steht für:

```text
https://boardgames.example/game/auf-nach-japan
```

Die Prefixes verändern also nicht die Identität einer Ressource. Sie machen die Turtle-Datei lediglich besser lesbar.

---

## RDF-Tripel

RDF beschreibt Informationen grundsätzlich als Tripel:

```text
Subjekt → Prädikat → Objekt
```

Beispielsweise:

```turtle
game:auf-nach-japan
    prop:publisher publisher:schwerkraft-verlag .
```

entspricht:

```text
Auf nach Japan! → publisher → Schwerkraft-Verlag
```

Das Spiel ist das **Subjekt**, `publisher` das **Prädikat** und der Verlag das **Objekt**.

---

## Das Brettspiel als Ressource

Das Spiel wird als eigene RDF-Ressource beschrieben:

```turtle
game:auf-nach-japan
    rdf:type bg:BoardGame ;
    rdfs:label "Auf nach Japan!"@de ;
    prop:author
        person:josh-wood,
        person:mark-wootton ;
    prop:publisher publisher:schwerkraft-verlag ;
    prop:yearOfPublication 2025 ;
    prop:minPlayer 1 ;
    prop:maxPlayer 4 ;
    prop:mechanic
        mechanic:set-collection,
        mechanic:hand-management .
```

Das Spiel besitzt damit unter anderem Beziehungen zu:

- Autoren
- einem Verlag
- Spielmechaniken

Andere Eigenschaften wie Erscheinungsjahr oder Spieleranzahl werden als Literale gespeichert.

Ein wichtiger Unterschied besteht deshalb zwischen **Ressourcen** und **Literalen**.

Beispiel für eine Ressource:

```turtle
prop:author person:josh-wood
```

Beispiel für ein Literal:

```turtle
prop:yearOfPublication 2025
```

---

## Personen und Verlag

Autoren und Verlag werden ebenfalls als eigenständige Ressourcen modelliert:

```turtle
person:josh-wood
    rdf:type bg:Person ;
    rdfs:label "Josh Wood" .
```

Dadurch ist Josh Wood nicht nur der Text `"Josh Wood"`, sondern eine Ressource mit einer eigenen IRI:

```text
https://boardgames.example/person/josh-wood
```

Diese Ressource könnte später um weitere Informationen ergänzt und von beliebig vielen Spielen referenziert werden.

Dasselbe Prinzip wird für den Verlag verwendet.

---

# SKOS

Für die Modellierung von Spielmechaniken wird **SKOS – Simple Knowledge Organization System** verwendet.

Eine Mechanik wird dabei als:

```turtle
rdf:type skos:Concept
```

definiert.

Beispiel:

```turtle
mechanic:set-collection
    rdf:type skos:Concept ;
    skos:prefLabel "Set Collection"@en ;
    skos:prefLabel "Set-Sammlung"@de .
```

Die Ressource

```text
https://boardgames.example/mechanic/set-collection
```

repräsentiert das eigentliche Concept.

Die Bezeichnungen `"Set Collection"` und `"Set-Sammlung"` sind lediglich sprachabhängige Labels dieses Concepts.

Dadurch kann dieselbe Ressource unterschiedliche Bezeichnungen besitzen, ohne ihre Identität zu verändern.

---

## SKOS Concept Scheme

Die Spielmechaniken gehören zu einem gemeinsamen `skos:ConceptScheme`:

```turtle
scheme:board-game-mechanics
    rdf:type skos:ConceptScheme ;
    skos:prefLabel "Board Game Mechanics"@en ;
    skos:prefLabel "Brettspielmechaniken"@de .
```

Eine Mechanik wird über:

```turtle
skos:inScheme scheme:board-game-mechanics
```

diesem Schema zugeordnet.

---

## SKOS Labels

Für die Beschreibung eines Concepts werden unterschiedliche Label-Typen verwendet.

### `skos:prefLabel`

Bevorzugte Bezeichnung:

```turtle
skos:prefLabel "Set Collection"@en ;
skos:prefLabel "Set-Sammlung"@de ;
```

Durch die Language Tags `@en` und `@de` können unterschiedliche Sprachen unterschieden werden.

### `skos:altLabel`

Alternative Bezeichnung:

```turtle
skos:altLabel "Set Collecting"@en ;
```

Alternative Labels können beispielsweise für Suche oder Autovervollständigung verwendet werden.

### `skos:hiddenLabel`

Versteckte Bezeichnung:

```turtle
skos:hiddenLabel "SetCollection"@en ;
```

Ein `hiddenLabel` kann beispielsweise für alternative Schreibweisen oder Suchbegriffe verwendet werden, die dem Benutzer normalerweise nicht als Bezeichnung angezeigt werden sollen.

---

# Beziehungen zwischen SKOS Concepts

SKOS ermöglicht es, Beziehungen zwischen Concepts zu modellieren.

## `skos:broader`

`skos:broader` beschreibt einen allgemeineren Begriff.

```turtle
mechanic:set-collection
    skos:broader mechanic:card-mechanics .
```

Damit entsteht:

```text
Set Collection
      │
      │ broader
      ↓
Card Mechanics
```

`Set Collection` ist also ein spezifischerer Begriff innerhalb der allgemeineren Kategorie `Card Mechanics`.

---

## `skos:related`

`skos:related` beschreibt eine nicht-hierarchische Beziehung zwischen zwei Concepts.

```turtle
mechanic:set-collection
    skos:related mechanic:hand-management .
```

Damit wird ausgedrückt, dass die beiden Spielmechaniken miteinander in Beziehung stehen, ohne dass eine davon Ober- oder Unterbegriff der anderen sein muss.

---

# main.py

Die Datei `main.py` verwendet die Python-Bibliothek **RDFLib**, um die Turtle-Datei einzulesen und den darin enthaltenen RDF-Graphen zu untersuchen.

Installation:

```bash
pip install rdflib
```

---

## RDF-Graph laden

Zunächst wird ein Graph erzeugt:

```python
from rdflib import Graph

graph = Graph()
```

Anschließend wird die Turtle-Datei eingelesen:

```python
graph.parse("boardgames.ttl", format="turtle")
```

RDFLib parst die Turtle-Syntax und erzeugt daraus einen RDF-Graphen.

Die Anzahl der enthaltenen Tripel kann anschließend ausgegeben werden:

```python
print(f"Anzahl der Tripel: {len(graph)}")
```

Der aktuelle Graph enthält:

```text
36 Tripel
```

---

## Alle Tripel anzeigen

Ein RDF-Graph kann direkt durchlaufen werden:

```python
for subject, predicate, object_ in graph:
    print(f"SUBJECT:   {subject}")
    print(f"PREDICATE: {predicate}")
    print(f"OBJECT:    {object_}")
```

RDFLib liefert dabei immer die drei Bestandteile eines RDF-Tripels:

```text
Subject
Predicate
Object
```

Beispielsweise:

```text
SUBJECT:
https://boardgames.example/game/auf-nach-japan

PREDICATE:
https://boardgames.example/property/author

OBJECT:
https://boardgames.example/person/josh-wood
```

Die kompakte Turtle-Schreibweise wurde beim Parsen also wieder in einzelne RDF-Tripel aufgelöst.

---

# Namespaces in Python

Auch RDFLib unterstützt Namespaces.

Beispielsweise:

```python
from rdflib import Namespace

GAME = Namespace("https://boardgames.example/game/")
PROP = Namespace("https://boardgames.example/property/")
```

Anschließend kann:

```python
GAME["auf-nach-japan"]
```

verwendet werden.

Das repräsentiert die vollständige IRI:

```text
https://boardgames.example/game/auf-nach-japan
```

---

# Informationen aus dem Graphen lesen

Mit RDFLib kann gezielt nach Tripeln gesucht werden.

Beispielsweise können alle Autoren eines Spiels ermittelt werden:

```python
game = GAME["auf-nach-japan"]

for author in graph.objects(game, PROP.author):
    print(author)
```

Die Anfrage entspricht konzeptionell:

```text
SUBJECT:   Auf nach Japan!
PREDICATE: author
OBJECT:    ?
```

RDFLib sucht also alle Objekte, die über das Prädikat `author` mit dem Spiel verbunden sind.

Das Ergebnis sind die Ressourcen:

```text
https://boardgames.example/person/josh-wood
https://boardgames.example/person/mark-wootton
```

---

# Labels von Ressourcen ermitteln

Eine IRI ist für Maschinen geeignet, für Benutzer soll jedoch normalerweise eine lesbare Bezeichnung dargestellt werden.

Die Autoren besitzen deshalb ein `rdfs:label`.

Mit:

```python
from rdflib.namespace import RDFS
```

kann dieses Label abgefragt werden:

```python
for author in graph.objects(game, PROP.author):
    label = graph.value(author, RDFS.label)
    print(label)
```

Das Ergebnis lautet:

```text
Josh Wood
Mark Wootton
```

Die Anwendung navigiert dabei durch den RDF-Graphen:

```text
Auf nach Japan!
      │
      │ author
      ↓
   Josh Wood
      │
      │ rdfs:label
      ↓
  "Josh Wood"
```

---

# SKOS mit RDFLib auslesen

RDFLib stellt auch die SKOS-Vokabel bereit:

```python
from rdflib.namespace import SKOS
```

Ein bestimmtes Concept kann beispielsweise so ausgewählt werden:

```python
MECHANIC = Namespace("https://boardgames.example/mechanic/")

concept = MECHANIC["set-collection"]
```

---

## Preferred Labels

Alle bevorzugten Labels können mit:

```python
for label in graph.objects(concept, SKOS.prefLabel):
    print(label)
```

ausgelesen werden.

Da RDF-Literale ihre Sprachinformation behalten, kann auch auf die Sprache zugegriffen werden:

```python
for label in graph.objects(concept, SKOS.prefLabel):
    print(f"Text: {label}")
    print(f"Sprache: {label.language}")
```

Damit kann beispielsweise gezielt das deutsche Label ausgewählt werden:

```python
for label in graph.objects(concept, SKOS.prefLabel):
    if label.language == "de":
        print(label)
```

---

## Übergeordnete Concepts

Die `skos:broader`-Beziehung kann ebenfalls aus dem Graphen gelesen werden:

```python
broader = graph.value(concept, SKOS.broader)
```

Dadurch erhält man zunächst die IRI des übergeordneten Concepts.

Anschließend kann dessen deutsches Label gesucht werden:

```python
for label in graph.objects(broader, SKOS.prefLabel):
    if label.language == "de":
        print(label)
```

Die Anwendung navigiert dabei über mehrere Beziehungen:

```text
Set Collection
      │
      │ skos:broader
      ↓
Card Mechanics
      │
      │ skos:prefLabel @de
      ↓
"Kartenmechaniken"
```

---

## Verwandte Concepts

Dasselbe Prinzip kann für `skos:related` verwendet werden:

```python
for related in graph.objects(concept, SKOS.related):
    for label in graph.objects(related, SKOS.prefLabel):
        if label.language == "de":
            print(label)
```

Dadurch kann beispielsweise das verwandte Concept `Hand Management` gefunden und dessen deutsches Label ausgegeben werden.

---

# Zentrale Idee des Projekts

Die Informationen werden nicht in Python fest einprogrammiert.

Python enthält beispielsweise nicht:

```python
author = "Josh Wood"
broader = "Kartenmechaniken"
related = "Handkarten-Management"
```

Stattdessen befinden sich die Informationen und Beziehungen im **RDF-Graphen**.

Python kennt lediglich die Struktur beziehungsweise die Vokabulare und fragt den Graphen ab:

```text
Ressource
   │
   ├── Predicate → Ressource
   │                  │
   │                  └── Predicate → Literal
   │
   └── Predicate → Literal
```

Dadurch entsteht ein Netzwerk miteinander verbundener Ressourcen.

Genau dieses Prinzip bildet die Grundlage von **Linked Data**.

---

# Nächste Schritte

Im weiteren Verlauf soll das Projekt um folgende Themen erweitert werden:

- Abfragen mit **SPARQL**
- weitere Brettspiele
- weitere SKOS Concepts
- hierarchische Beziehungen mit `skos:broader` und `skos:narrower`
- Navigation durch den RDF-Graphen
- Darstellung einzelner SKOS Concepts
- Aufbau einer kleinen Python-Webanwendung
- Darstellung von Beziehungen zwischen Brettspielen, Personen, Verlagen und Spielmechaniken

Das Projekt dient dabei bewusst als überschaubares Lernmodell für größere Linked-Data-Anwendungen.