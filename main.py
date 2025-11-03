from enum import Enum
from fastapi import FastAPI, Query
import sqlite3
from typing import Annotated

app = FastAPI()


class TableName(Enum):
    info_movie = "movie"
    info_manga = "manga"
    info_tvshow = "tvshow"
    info_anime = "anime"
    info_book = "book"
    media = "media"
    user_activity = "user"


DB_PATH = "data/all_media.db"


@app.get("/{table_name}/count")
async def count_table(table_name: TableName):

    sql_query = f"SELECT COUNT(*) FROM {table_name.name}"
    result = await connect_and_query(DB_PATH, sql_query)

    return {"row count": result, "table": table_name.name}


async def connect_and_query(db_path: str, sql: str) -> list[dict]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor = cursor.execute(sql)
    fields = [d[0] for d in cursor.description]
    res = cursor.fetchall()
    conn.close()

    dic = [dict(zip(fields, row)) for row in res]
    return dic


# utility functions -> predefined queries


@app.get("/{table_name}/raw")
async def all_table(table_name: TableName):
    sql = f"SELECT * FROM {table_name.name}"
    res = await connect_and_query(DB_PATH, sql)
    return {"table": table_name.name, "data": res}


@app.get("/media/{media_id}")
async def get_media_by_id(media_id: int):
    sql = f"SELECT type FROM media WHERE id = {media_id}"
    res = await connect_and_query(DB_PATH, sql)
    table = TableName(res[0]["type"])

    sql = f"""SELECT *
    FROM media 
    JOIN {table.name} ON media.id = {table.name}.media_id 
    WHERE media.id = {media_id}"""

    res = await connect_and_query(DB_PATH, sql)

    return {"data": res}


@app.get("/media/search")
async def search_by_keyword(
    keyword: Annotated[
        str, Query(description="Keyword to search for in title or comment")
    ],
):
    # fuzzy match in title, comment ...
    sql = f"""SELECT *
    FROM media
    WHERE title LIKE '%{keyword}%' OR comment LIKE '%{keyword}%' 
    """
    res = await connect_and_query(DB_PATH, sql)

    return {"data": res}
