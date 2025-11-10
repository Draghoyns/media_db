from enum import Enum
from fastapi import FastAPI, Query
import sqlite3
from typing import Annotated
from media_classes import QuickMedia, Media

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

# db connection and querying


async def connect_and_query(db_path: str, sql: str) -> list[dict]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor = cursor.execute(sql)
    fields = [d[0] for d in cursor.description]
    res = cursor.fetchall()
    conn.close()

    dic = [dict(zip(fields, row)) for row in res]
    return dic


# endpoints

## create element


### quick create -> minimal fields and other are defaulted
@app.post("/media/quick_create")
async def quick_create_media(media: QuickMedia):
    # mandatory fields: title, type, year, status

    # TODO: flexbility to assign non mandatory fields if provided
    # insert into database by creating corresponding subclass
    # use insert_media

    return media


### detailed create -> all fields necessary
@app.post("/media/full_create")
async def full_create_media(media: Media):
    # two phases ?? is that even possible ?
    # get all fields corresponding to raw data and adapt uniform fields based on media type (single_duration typically)
    return media


## table queries
@app.get("/{table_name}/count")
async def count_table(table_name: TableName):

    sql_query = f"SELECT COUNT(*) FROM {table_name.name}"
    result = await connect_and_query(DB_PATH, sql_query)

    return {"row count": result, "table": table_name.name}


@app.get("/{table_name}/full")
async def display_full_table(table_name: TableName):
    sql = f"SELECT * FROM {table_name.name}"
    res = await connect_and_query(DB_PATH, sql)
    return {"table": table_name.name, "data": res}


## media queries
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


@app.get("/media/{media_id}")
async def get_media_by_id(media_id: int):
    sql = f"SELECT type FROM media WHERE id = {media_id}"
    res = await connect_and_query(DB_PATH, sql)
    if res == []:
        return {"Error": f"media id '{media_id}' not found"}
    table = TableName(res[0]["type"])

    sql = f"""SELECT *
    FROM media 
    JOIN {table.name} ON media.id = {table.name}.media_id 
    WHERE media.id = {media_id}"""

    res = await connect_and_query(DB_PATH, sql)

    return {"data": res}
