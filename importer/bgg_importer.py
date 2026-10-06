import os
from pprint import pprint
import xml.etree.ElementTree as ET


import requests
from dotenv import load_dotenv


load_dotenv()

BGG_API_URL = "https://boardgamegeek.com/xmlapi2/thing"

BGG_TOKEN = os.getenv("BGG_TOKEN")


def fetch_game(game_id):
    if not BGG_TOKEN:
        raise RuntimeError("BGG_TOKEN ist nicht gesetzt.")

    headers = {
        "Authorization": f"Bearer {BGG_TOKEN}"
    }

    params = {
        "id": game_id,
        "stats": 1,
    }

    response = requests.get(
        BGG_API_URL,
        headers=headers,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    return response.text

def fetch_games(game_ids):
    if not BGG_TOKEN:
        raise RuntimeError("BGG_TOKEN ist nicht gesetzt.")

    if not game_ids:
        raise ValueError("Es wurden keine BGG-IDs übergeben.")

    ids = ",".join(str(game_id) for game_id in game_ids)

    headers = {
        "Authorization": f"Bearer {BGG_TOKEN}"
    }

    params = {
        "id": ids,
        "stats": 1
    }

    response = requests.get(
        BGG_API_URL,
        headers=headers,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.text

def parse_game(xml):
    root = ET.fromstring(xml)

    item = root.find("item")

    if item is None:
        raise ValueError("Keine Spieldaten in der BGG-Antwort gefunden.")

    bgg_id = int(item.get("id"))

    name = None

    for name_element in item.findall("name"):
        if name_element.get("type") == "primary":
            name = name_element.get("value")
            break

    year = int(item.find("yearpublished").get("value"))
    min_players = int(item.find("minplayers").get("value"))
    max_players = int(item.find("maxplayers").get("value"))

    designers = parse_links(item, "boardgamedesigner")
    artists = parse_links(item, "boardgameartist")
    publishers = parse_links(item, "boardgamepublisher")
    categories = parse_links(item, "boardgamecategory")
    mechanics = parse_links(item, "boardgamemechanic")

    return {
        "bgg_id": bgg_id,
        "name": name,
        "year": year,
        "min_players": min_players,
        "max_players": max_players,
        "designers": designers,
        "artists": artists,
        "publishers": publishers,
        "categories": categories,
        "mechanics": mechanics,
    }

def parse_games(xml):
    root = ET.fromstring(xml)

    items = root.findall("item")

    if not items:
        raise ValueError(
            "Keine Spieldaten in der BGG-Antwort gefunden."
        )

    games = []

    for item in items:
        game = parse_game_item(item)
        games.append(game)

    return games

def parse_game_item(item):
    bgg_id = int(item.get("id"))

    name = None

    for name_element in item.findall("name"):
        if name_element.get("type") == "primary":
            name = name_element.get("value")
            break

    year = int(item.find("yearpublished").get("value"))
    min_players = int(item.find("minplayers").get("value"))
    max_players = int(item.find("maxplayers").get("value"))

    designers = parse_links(
        item,
        "boardgamedesigner"
    )

    artists = parse_links(
        item,
        "boardgameartist"
    )

    publishers = parse_links(
        item,
        "boardgamepublisher"
    )

    categories = parse_links(
        item,
        "boardgamecategory"
    )

    mechanics = parse_links(
        item,
        "boardgamemechanic"
    )

    return {
        "bgg_id": bgg_id,
        "name": name,
        "year": year,
        "min_players": min_players,
        "max_players": max_players,
        "designers": designers,
        "artists": artists,
        "publishers": publishers,
        "categories": categories,
        "mechanics": mechanics,
    }

def parse_links(item, link_type):
    results = []

    for link in item.findall("link"):
        if link.get("type") == link_type:
            results.append({
                "bgg_id": int(link.get("id")),
                "name": link.get("value"),
            })

    return results

#xml = fetch_game(224517)

#game = parse_game(xml)

#pprint(game, sort_dicts=False)

if __name__ == "__main__":
    game_ids = [
        224517,
        167791,
        342942,
    ]

    xml = fetch_games(game_ids)

    games = parse_games(xml)

    pprint(games, sort_dicts=False)