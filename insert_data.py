from media_db.data_load_parse import data_prep
import sqlite3
import json


def insert_media(data: list[dict], db_path="data/all_media.db"):
    # add media element to media table
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for item in data:
        cursor.execute(
            "INSERT INTO media (title, release_year, origin_lang, type, status, comment) VALUES (?, ?, ?, ?, ?, ?)",
            (
                item["title"],
                item["release_year"],
                item["language"],
                item["type"],
                item["status"],
                item["comment"],
            ),
        )
        id = cursor.lastrowid

        insert_type(item, cursor, id)
        insert_user(item, cursor, id)

    conn.commit()
    conn.close()


def insert_type(element: dict, cursor, media_id: int | None):
    # add media element to type specific table
    media_type = element["type"]

    if media_type == "movie":
        cursor.execute(
            "INSERT INTO info_movie (media_id, duration_min, director, status) VALUES (?, ?, ?, ?)",
            (
                media_id,
                element["duration"],
                ",".join(element["director"]),
                element["belonging"],
            ),
        )
    elif media_type == "manga":
        cursor.execute(
            "INSERT INTO info_manga (media_id, volumes, authors, adapted_anime_id) VALUES (?, ?, ?, ?)",
            (
                media_id,
                element["volumes"],
                ",".join(element["authors"]),
                json.dumps(element["adapted_to_anime"]),
            ),
        )
    elif media_type == "anime":
        cursor.execute(
            "INSERT INTO info_anime (media_id, seasons, ep_duration_min, total_episodes, status) VALUES (?, ?, ?, ?, ?)",
            (
                media_id,
                element["seasons"],
                element["ep_duration_min"],
                element["total_episodes"],
                element["belonging"],
            ),
        )
    elif media_type == "tvshow":
        cursor.execute(
            "INSERT INTO info_tvshow (media_id, seasons, ep_duration_min, total_episodes) VALUES (?, ?, ?, ?)",
            (
                media_id,
                element["seasons"],
                element["ep_duration_min"],
                element["total_episodes"],
            ),
        )
    elif media_type == "book":
        cursor.execute(
            "INSERT INTO info_book (media_id, pages, authors, status) VALUES (?, ?, ?, ?)",
            (
                media_id,
                element["pages"],
                ",".join(element["authors"]),
                element["belonging"],
            ),
        )


def insert_user(element: dict, cursor, media_id: int | None):
    # add user activity element to user_activity table

    if element.get("seen"):

        cursor.execute(
            "INSERT INTO user_activity (media_id, rating, last_watch_date, times_consumed) VALUES (?, ?, ?, ?)",
            (
                media_id,
                element.get("rating"),
                element.get("last_watch_date"),
                element.get("times_consumed", 1),
            ),
        )


if __name__ == "__main__":
    csv_data = "./data/raw.csv"
    data = data_prep(csv_data)
    insert_media(data)
