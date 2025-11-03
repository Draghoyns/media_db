from dataclasses import asdict
import pandas as pd
from media_classes import create_media_instance
from tqdm import tqdm


def load_csv_normalize(file_path: str, header: bool = True) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame
    and set data types for each column.

    Very manual for now.

    Parameters:
    - file_path (str): The path to the CSV file. Delimiter is assumed to be ',', and any ',' present (even between quotes) will be treated as delimiters. Be careful if your data contains commas within quoted strings.
    - delimiter (str): The delimiter used in the CSV file. Default is ','.
    - header (bool): Whether the CSV file has a header row. Default is True.

    Returns:
    - pd.DataFrame: The loaded DataFrame.
    """
    df = pd.read_csv(file_path, encoding="utf-8")

    # normalize column names
    df.columns = [col.strip().lower() for col in df.columns]

    col_types = {
        "title": "string",
        "type": "string",
        "year": "string",
        "single_duration": "Int64",
        "lang": "string",
        "seen": bool,
        "rating": "Int64",
        "last_watched": "string",
        "times_watched": "Int64",
        "comment": "string",
        "authors": "string",
        "belonging": "string",
        "anime": bool,
        "seasons": "Int64",
        "total_ep": "Int64",
        "status": "string",
    }
    for col in col_types.keys():
        if col_types[col] == "Int64":
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
        elif col_types[col] == bool:
            df[col] = (
                df[col]
                .astype(str)
                .map(
                    {
                        "no": False,
                        "yes": True,
                    }
                )
            )
        else:
            df[col] = df[col].astype(col_types[col])

    return df


def dataframe_rename(df: pd.DataFrame) -> pd.DataFrame:

    df["duration"] = df[["single_duration", "type"]].apply(
        lambda x: x["single_duration"] if x["type"] == "movie" else 0, axis=1
    )
    df["volumes"] = df[["single_duration", "type"]].apply(
        lambda x: x["single_duration"] if x["type"] == "manga" else 0, axis=1
    )
    df["pages"] = df[["single_duration", "type"]].apply(
        lambda x: x["single_duration"] if x["type"] == "book" else 0, axis=1
    )
    df["ep_duration_min"] = df[["single_duration", "type"]].apply(
        lambda x: x["single_duration"] if x["type"] in ["anime", "tvshow"] else 0,
        axis=1,
    )
    df = df.drop(columns=["single_duration"])

    df.rename(
        columns={
            "year": "release_year",
            "total_ep": "total_episodes",
            "lang": "language",
            "anime": "adapted_to_anime",
            "last_watched": "last_watch_date",
            "times_watched": "times_consumed",
        },
        inplace=True,
    )
    df["authors"] = df["authors"].apply(
        lambda x: [s.strip() for s in x.split("|") if s.strip()] if pd.notna(x) else []
    )
    return df


def media_from_row(row):
    # row to dict
    dict_row = row.to_dict()
    media_type = dict_row.get("type")
    return create_media_instance(media_type, **dict_row)


def media_list_from_dataframe(df: pd.DataFrame) -> list:
    media_list = []
    for row_index, row in tqdm(df.iterrows(), total=df.shape[0]):
        media_list.append(media_from_row(row))

    data = [asdict(media) for media in media_list]
    return data


def data_prep(csv_data: str) -> list:
    raw_db_df = load_csv_normalize(csv_data)
    clean_col_df = dataframe_rename(raw_db_df)
    media_list = media_list_from_dataframe(clean_col_df)
    return media_list


if __name__ == "__main__":
    csv_data = "./data/raw.csv"
    data = data_prep(csv_data)
    print(data)
