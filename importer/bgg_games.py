import os
import zipfile
import csv
from datetime import datetime
from pathlib import Path
from pprint import pprint
from bgg_importer import fetch_game, fetch_games, parse_game, parse_game_item, parse_games
from rdf_importer import create_graph, add_games, save_graph

import requests
from dotenv import load_dotenv


load_dotenv()


DATA_DIR = Path(__file__).parent / "data"
CSV_FILE = DATA_DIR / "boardgames_ranks.csv"
TEMP_FILE = CSV_FILE.with_suffix(".tmp")

BGG_TOKEN = os.getenv("BGG_TOKEN")
BGG_CSV_URL = "https://boardgamegeek.com/data_dumps/bg_ranks"

def import_games_to_rdf(games):
    print(
        f"\nLade BGG-Detaildaten für "
        f"{len(games)} Spiele ..."
    )

    detailed_games = get_game_details(games)

    print(
        f"{len(detailed_games)} Spiele "
        f"wurden von BGG geladen."
    )

    graph = create_graph()

    add_games(
        graph,
        detailed_games
    )

    output_file = (
        Path(__file__).parent.parent
        / "data"
        / "bgg_boardgames.ttl"
    )

    save_graph(
        graph,
        output_file
    )

    print(
        f"\nRDF-Datei gespeichert:"
        f"\n{output_file}"
    )

def fetch_game_details(games):
    detailed_games = []

    for game in games:
        print(
            f"Lade Details für "
            f"{game['name']} "
            f"[BGG-ID: {game['id']}] ..."
        )

        xml = fetch_game(game["id"])
        details = parse_game(xml)

        detailed_games.append(details)

    return detailed_games

def get_ranking_zips():
    return {
        file: file.stat().st_mtime
        for file in DATA_DIR.glob("boardgames_ranks_*.zip")
    }

def find_ranking_zip():
    zip_files = list(
        DATA_DIR.glob("boardgames_ranks_*.zip")
    )

    if not zip_files:
        return None

    return max(
        zip_files,
        key=lambda file: file.stat().st_mtime
    )

def inspect_ranking_zip(zip_path):
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        print(f"\nInhalt von {zip_path.name}:")

        for file_name in zip_file.namelist():
            print(f"  {file_name}")

def find_new_ranking_zip(previous_zips):
    current_zips = get_ranking_zips()

    new_or_changed = []

    for file, modification_time in current_zips.items():
        if (
            file not in previous_zips
            or previous_zips[file] != modification_time
        ):
            new_or_changed.append(file)

    if not new_or_changed:
        return None

    return max(
        new_or_changed,
        key=lambda file: file.stat().st_mtime
    )

def import_ranking_zip(zip_path):
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        if "boardgames_ranks.csv" not in zip_file.namelist():
            raise FileNotFoundError(
                "Die ZIP-Datei enthält keine boardgames_ranks.csv."
            )

        with zip_file.open("boardgames_ranks.csv") as source:
            TEMP_FILE.write_bytes(source.read())

    if not validate_csv(TEMP_FILE):
        TEMP_FILE.unlink(missing_ok=True)
        raise ValueError(
            "Die extrahierte Datei ist keine gültige BGG-Rangliste."
        )

    TEMP_FILE.replace(CSV_FILE)

    print(f"BGG-Rangliste aktualisiert: {CSV_FILE}")

def validate_csv(csv_path):
    required_columns = {
        "id",
        "name",
        "yearpublished",
        "rank",
        "average",
        "bayesaverage",
        "usersrated",
    }

    with csv_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            return False

        existing_columns = set(reader.fieldnames)

        return required_columns.issubset(existing_columns)

def csv_exists():
    return CSV_FILE.exists()


def get_file_date():
    timestamp = CSV_FILE.stat().st_mtime
    return datetime.fromtimestamp(timestamp)


def download_csv():
    if not BGG_TOKEN:
        raise RuntimeError("BGG_TOKEN ist nicht gesetzt.")

    print("BGG-Rangliste wird heruntergeladen ...")

    headers = {
        "Authorization": f"Bearer {BGG_TOKEN}"
    }

    response = requests.get(
        BGG_CSV_URL,
        headers=headers,
        timeout=60,
    )

    response.raise_for_status()

    CSV_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    TEMP_FILE.write_bytes(response.content)

    TEMP_FILE.replace(CSV_FILE)

    print(f"BGG-Rangliste gespeichert: {CSV_FILE}")

def load_games():
    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"CSV-Datei wurde nicht gefunden: {CSV_FILE}"
        )

    with CSV_FILE.open(
        "r",
        encoding="utf-8",
        newline=""
    ) as file:
        reader = csv.DictReader(file)

        # print("Spalten der CSV-Datei:")
        # print(reader.fieldnames)

        games = list(reader)

    return games

def get_top_games(games, limit=100):
    ranked_games = [
        game
        for game in games
        if game["rank"] > 0
    ]

    ranked_games.sort(
        key=lambda game: game["rank"]
    )

    return ranked_games[:limit]

def get_game_details(games):
    game_ids = [
        game["id"]
        for game in games
    ]

    xml = fetch_games(game_ids)

    detailed_games = parse_games(xml)

    return detailed_games

def display_games(games):
    print()
    print(
        f"{'Rang':<6}"
        f"{'BGG-ID':<10}"
        f"{'Jahr':<7}"
        f"{'Rating':<9}"
        f"{'Bewertungen':<13}"
        f"Spiel"
    )

    print("-" * 90)

    for game in games:
        print(
            f"{game['rank']:<6}"
            f"{game['id']:<10}"
            f"{game['year']:<7}"
            f"{game['average']:<9.2f}"
            f"{game['users_rated']:<13}"
            f"{game['name']}"
        )

def ask_limit():
    while True:
        choice = input(
            "\nWie viele Spiele möchtest du anzeigen? "
            "[10 / 25 / 50 / 100]: "
        ).strip()

        if choice in {"10", "25", "50", "100"}:
            return int(choice)

        print("Bitte 10, 25, 50 oder 100 eingeben.")

def show_menu():
    print("\nBGG Spieleübersicht")
    print("-------------------")
    print("[1] Top-Spiele anzeigen")
    print("[2] Spiel suchen")
    print("[3] Detaildaten der Top-Spiele laden")
    print("[4] Top-Spiele als RDF importieren")
    print("[q] Beenden")

    return input("\nAuswahl: ").strip().lower()

def run_menu(games):
    while True:
        choice = show_menu()

        if choice == "1":
            limit = ask_limit()
            top_games = get_top_games(games, limit)
            display_games(top_games)

        elif choice == "2":
            search_term = input("\nName oder Teil des Spielnamens: ").strip()

            results = search_games(games, search_term)

            if results:
                display_games(results[:50])
                print(f"\n{len(results)} Treffer gefunden.")
            else:
                print("Keine Spiele gefunden.")

        elif choice == "3":
            limit = ask_limit()

            top_games = get_top_games(
                games,
                limit
            )

            print(
                f"\nDetaildaten für "
                f"{len(top_games)} Spiele werden geladen ..."
            )

            detailed_games = get_game_details(
                top_games
            )

            pprint(
                detailed_games,
                sort_dicts=False
            )

        elif choice == "4":
            limit = ask_limit()

            top_games = get_top_games(
                games,
                limit
            )

            import_games_to_rdf(
                top_games
            )

        elif choice == "q":
            print("Programm beendet.")
            break

        else:
            print("Ungültige Eingabe.")

def search_games(games, search_term):
    search_term = search_term.lower()

    results = []

    for game in games:
        if search_term in game["name"].lower():
            results.append(game)

    return results

def normalize_game(game):
    rank = game["rank"]

    if not rank.isdigit():
        return None

    rank = int(rank)

    if rank == 0:
        return None

    return {
        "id": int(game["id"]),
        "name": game["name"],
        "year": int(game["yearpublished"]),
        "rank": rank,
        "average": float(game["average"]),
        "bayes_average": float(game["bayesaverage"]),
        "users_rated": int(game["usersrated"]),
    }

def normalize_games(games):
    normalized_games = []

    for game in games:
        normalized_game = normalize_game(game)

        if normalized_game is not None:
            normalized_games.append(normalized_game)

    return normalized_games

def main():
    if csv_exists():
        file_date = get_file_date()

        print(
            f"Lokale BGG-Rangliste vom "
            f"{file_date:%d.%m.%Y um %H:%M Uhr}"
        )

        choice = input(
            "\nVorhandene Datei verwenden oder neu herunterladen? "
            "[Enter/v]orhanden / [n]eu: "
        ).strip().lower()

        if choice in {"", "v"}:
            print("Vorhandene Datei wird verwendet.")

        elif choice == "n":
            previous_zips = get_ranking_zips()

            print("\nAktuelle BGG-Rangliste herunterladen:")
            print("https://boardgamegeek.com/data_dumps/bg_ranks")

            print(
                "\nSpeichere die ZIP-Datei anschließend in:"
                f"\n{DATA_DIR}"
            )

            input(
                "\nDrücke Enter, sobald die ZIP-Datei heruntergeladen wurde ..."
            )

            zip_path = find_new_ranking_zip(previous_zips)

            if zip_path is None:
                print(
                    "\nEs wurde keine neue oder aktualisierte "
                    "BGG-ZIP gefunden."
                )
                return

            print(f"\nNeue BGG-ZIP gefunden: {zip_path.name}")

            import_ranking_zip(zip_path)

        else:
            print("Ungültige Eingabe.")
            return

    else:
        print("Keine lokale BGG-Rangliste gefunden.")
        download_csv()

    games = load_games()

    print(f"\nAnzahl der Spiele: {len(games)}")

    games = normalize_games(games)

    run_menu(games)


if __name__ == "__main__":
    main()
